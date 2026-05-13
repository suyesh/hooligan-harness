import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import install


class HooliganInstallerTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.source_dir = self.root / "source"
        self.home = self.root / "home"
        self.source_dir.mkdir()
        self.home.mkdir()

        (self.source_dir / ".harness").mkdir()
        (self.source_dir / "personas").mkdir()
        for file_name in ["SKILL.md", "README.md", "INSTALL.md", "install.py"]:
            (self.source_dir / file_name).write_text(file_name, encoding="utf-8")
        for persona_name in install.CLAUDE_PERSONAS:
            (self.source_dir / "personas" / persona_name).write_text(persona_name, encoding="utf-8")

        (self.home / ".claude" / "skills").mkdir(parents=True)
        (self.home / ".claude" / "agents").mkdir(parents=True)
        (self.home / ".codex" / "skills").mkdir(parents=True)

        self.installer = install.HooliganInstaller(source_dir=self.source_dir, home=self.home)

    def tearDown(self):
        self.tempdir.cleanup()

    def test_doctor_removes_duplicate_directories_and_dedupes_registry(self):
        canonical = self.home / ".claude" / "skills" / install.SKILL_NAME
        duplicate = self.home / ".claude" / "skills" / f"{install.SKILL_NAME}.backup.20260513"
        canonical.mkdir(parents=True)
        duplicate.mkdir(parents=True)
        for name in install.CLAUDE_REQUIRED_FILES:
            path = canonical / name
            if name in {".harness", "personas"}:
                path.mkdir()
            else:
                path.write_text(name, encoding="utf-8")

        registry_file = self.home / ".claude" / "skills.json"
        registry_file.write_text(
            json.dumps(
                {
                    "skills": [
                        {"name": install.SKILL_NAME, "path": "one"},
                        {"name": install.SKILL_NAME, "path": "two"},
                    ]
                }
            ),
            encoding="utf-8",
        )

        self.installer.install_targets = ["claude"]
        self.assertTrue(self.installer.doctor(apply_fixes=True))
        self.assertFalse(duplicate.exists())

        registry = json.loads(registry_file.read_text(encoding="utf-8"))
        entries = [entry for entry in registry["skills"] if entry["name"] == install.SKILL_NAME]
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["path"], str(self.installer.claude_path["global_skills"]))

    def test_install_copies_maintenance_assets_and_manifest(self):
        (self.source_dir / ".git").mkdir()
        self.installer.install_targets = ["claude"]

        self.assertTrue(self.installer.install_files())

        skill_dir = self.installer.claude_path["global_skills"]
        self.assertTrue((skill_dir / "install.py").exists())
        self.assertTrue((skill_dir / "INSTALL.md").exists())
        self.assertTrue((skill_dir / "personas" / "Planner.md").exists())

        manifest = json.loads((skill_dir / install.INSTALL_MANIFEST_PATH).read_text(encoding="utf-8"))
        self.assertEqual(manifest["target"], "claude")
        self.assertEqual(Path(manifest["source_checkout"]).resolve(), self.source_dir.resolve())

    def test_doctor_check_mode_reports_without_fixing(self):
        duplicate = self.home / ".codex" / "skills" / f"{install.SKILL_NAME}.backup.20260513"
        duplicate.mkdir(parents=True)

        self.installer.install_targets = ["codex"]
        self.assertFalse(self.installer.doctor(apply_fixes=False))
        self.assertTrue(duplicate.exists())

    def test_update_refuses_dirty_checkout_without_force(self):
        (self.source_dir / ".git").mkdir()

        def fake_output(command):
            if command == ["git", "branch", "--show-current"]:
                return "main\n"
            if command == ["git", "status", "--porcelain"]:
                return " M install.py\n"
            raise AssertionError(command)

        self.installer._git_output = fake_output
        self.installer._run_git = lambda command: None

        with self.assertRaises(RuntimeError) as ctx:
            self.installer.update_installation(force=False)
        self.assertIn("Working tree has local changes", str(ctx.exception))

    def test_update_delegates_when_run_from_installed_skill_copy(self):
        canonical_checkout = self.root / "canonical-checkout"
        canonical_checkout.mkdir()
        (canonical_checkout / "install.py").write_text("print('installer')", encoding="utf-8")
        manifest_path = self.source_dir / install.INSTALL_MANIFEST_PATH
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(
            json.dumps({"source_checkout": str(canonical_checkout)}),
            encoding="utf-8",
        )

        with patch("install.subprocess.run", autospec=True) as run_subprocess:
            run_subprocess.return_value.returncode = 0
            run_subprocess.return_value.stdout = "delegated update\n"
            run_subprocess.return_value.stderr = ""

            self.assertTrue(self.installer.update_installation(force=True))

        run_subprocess.assert_called_once_with(
            [sys.executable, str(canonical_checkout / "install.py"), "update", "--ref", "main", "--force"],
            text=True,
            capture_output=True,
        )

    def test_update_runs_git_refresh_when_forced(self):
        (self.source_dir / ".git").mkdir()
        commands = []

        def fake_output(command):
            if command == ["git", "branch", "--show-current"]:
                return "feature-branch\n"
            if command == ["git", "status", "--porcelain"]:
                return " M install.py\n"
            raise AssertionError(command)

        def fake_run(command):
            commands.append(command)

        self.installer._git_output = fake_output
        self.installer._run_git = fake_run
        self.installer.install_targets = []

        with patch.object(self.installer, "choose_install_targets", autospec=True) as choose_targets:
            with patch.object(self.installer, "install_files", autospec=True) as install_files:
                choose_targets.side_effect = lambda: setattr(self.installer, "install_targets", ["codex"])
                install_files.return_value = True
                self.assertTrue(self.installer.update_installation(force=True))

        self.assertEqual(
            commands,
            [
                ["git", "fetch", "origin", "main"],
                ["git", "checkout", "main"],
                ["git", "pull", "--ff-only", "origin", "main"],
            ],
        )


if __name__ == "__main__":
    unittest.main()
