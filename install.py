#!/usr/bin/env python3
"""
hooliGAN-harness Installer
Beautiful CLI installer for Claude Code
"""

import os
import sys
import shutil
import json
import subprocess
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

# Try to import rich, if not available, prompt to install
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
    from rich.prompt import Prompt, Confirm
    from rich.table import Table
    from rich.syntax import Syntax
    from rich.markdown import Markdown
    from rich.layout import Layout
    from rich.align import Align
    from rich import box
    from rich.tree import Tree
except ImportError:
    print("📦 Installing required dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], check=True)
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
    from rich.prompt import Prompt, Confirm
    from rich.table import Table
    from rich.syntax import Syntax
    from rich.markdown import Markdown
    from rich.layout import Layout
    from rich.align import Align
    from rich import box
    from rich.tree import Tree

console = Console()

class HooliganInstaller:
    """Modern installer for hooliGAN-harness"""

    def __init__(self):
        self.console = Console()
        self.source_dir = Path(__file__).parent
        self.claude_path = self._get_claude_path()
        self.installed_files: List[Path] = []

    def _get_claude_path(self) -> Dict[str, Path]:
        """Detect Claude Code installation path"""
        home = Path.home()
        return {
            "global_skills": home / ".claude" / "skills" / "hooliGAN-harness",
            "global_agents": home / ".claude" / "agents",
            "config": home / ".claude"
        }

    def show_banner(self):
        """Display beautiful welcome banner"""
        banner = Panel.fit(
            "[bold magenta]hooliGAN-harness[/bold magenta] [cyan]v1.3.0[/cyan]\n\n"
            "[italic]High-reliability engineering framework for AI code generation[/italic]\n"
            "[dim]Inspired by GAN architectures[/dim]",
            border_style="bright_blue",
            box=box.DOUBLE_EDGE,
            title="[bold yellow]⚡ Installation Wizard ⚡[/bold yellow]",
            title_align="center"
        )
        self.console.print(banner)
        self.console.print()

    def detect_claude(self) -> bool:
        """Detect if Claude Code is installed"""
        return self.claude_path["config"].exists()

    def show_environment_status(self):
        """Display detected environment"""
        claude_installed = self.detect_claude()

        table = Table(
            title="[bold cyan]🔍 Environment Detection[/bold cyan]",
            box=box.ROUNDED,
            show_header=True,
            header_style="bold magenta"
        )

        table.add_column("Environment", style="cyan", width=15)
        table.add_column("Status", width=20)
        table.add_column("Path", style="dim")

        # Claude status
        claude_status = "✅ Installed" if claude_installed else "❌ Not Found"
        claude_style = "green" if claude_installed else "red"
        table.add_row(
            "Claude Code",
            f"[{claude_style}]{claude_status}[/{claude_style}]",
            str(self.claude_path["config"])
        )

        self.console.print(table)
        self.console.print()

        if not claude_installed:
            self.console.print("[bold red]⚠️  Claude Code installation not detected![/bold red]")
            self.console.print("[yellow]Please install Claude Code first.[/yellow]")
            self.console.print("[dim]Expected location: ~/.claude/[/dim]")
            sys.exit(1)

    def show_features(self):
        """Display feature overview"""
        features_panel = Panel(
            "[bold green]✨ Features to Install:[/bold green]\n\n"
            "• [cyan]5 Personas[/cyan]: Planner, Architect, Generator, Evaluator, Security Evaluator\n"
            "• [cyan]Failure Pattern Memory[/cyan]: Learning from past mistakes\n"
            "• [cyan]Confidence Scoring[/cyan]: Adaptive validation levels\n"
            "• [cyan]Rollback Mechanisms[/cyan]: Automatic recovery from failures\n"
            "• [cyan]Cross-Session Learning[/cyan]: Pattern evolution system\n"
            "• [cyan]Multi-Generator Mode[/cyan]: Parallel specialized generators\n"
            "• [cyan]Enterprise Integrations[/cyan]: CI/CD, monitoring, security tools\n"
            "• [cyan]Living Documentation[/cyan]: Auto-generated and maintained docs",
            border_style="green",
            box=box.ROUNDED
        )
        self.console.print(features_panel)
        self.console.print()

    def create_backup(self, target_path: Path) -> Optional[Path]:
        """Create backup of existing installation"""
        if target_path.exists():
            backup_path = target_path.parent / f"{target_path.name}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            self.console.print(f"[yellow]📦 Creating backup at {backup_path}[/yellow]")
            shutil.copytree(target_path, backup_path)
            return backup_path
        return None

    def install_files(self) -> bool:
        """Install files with progress bar"""
        self.console.print(f"\n[bold cyan]🚀 Installing to Claude Code...[/bold cyan]")

        # Create directories
        skills_dir = self.claude_path["global_skills"]
        agents_dir = self.claude_path["global_agents"]

        skills_dir.mkdir(parents=True, exist_ok=True)
        agents_dir.mkdir(parents=True, exist_ok=True)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=self.console
        ) as progress:

            # Files to copy
            files_to_copy = [
                ("SKILL.md", skills_dir / "SKILL.md"),
                ("README.md", skills_dir / "README.md"),
                (".harness", skills_dir / ".harness"),
                ("personas/Planner.md", agents_dir / "harness-planner.md"),
                ("personas/Architect.md", agents_dir / "harness-architect.md"),
                ("personas/Generator.md", agents_dir / "harness-generator.md"),
                ("personas/Evaluator.md", agents_dir / "harness-evaluator.md"),
                ("personas/SecurityEvaluator.md", agents_dir / "harness-security-evaluator.md"),
            ]

            task = progress.add_task("[green]Installing files...", total=len(files_to_copy))

            for source, dest in files_to_copy:
                source_path = self.source_dir / source

                if source_path.is_dir():
                    if dest.exists():
                        shutil.rmtree(dest)
                    shutil.copytree(source_path, dest)
                else:
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source_path, dest)

                self.installed_files.append(dest)
                progress.update(task, advance=1)

        # Update skill registry
        self._update_skill_registry()

        return True

    def _update_skill_registry(self):
        """Update skill registry for Claude Code"""
        registry_file = self.claude_path["config"] / "skills.json"

        if registry_file.exists():
            with open(registry_file, 'r') as f:
                registry = json.load(f)
        else:
            registry = {"skills": []}

        # Add hooliGAN-harness if not already present
        skill_entry = {
            "name": "hooliGAN-harness",
            "path": str(self.claude_path["global_skills"]),
            "version": "1.3.0",
            "description": "High-reliability engineering framework with adversarial evaluation"
        }

        # Remove old entry if exists
        registry["skills"] = [s for s in registry.get("skills", []) if s.get("name") != "hooliGAN-harness"]
        registry["skills"].append(skill_entry)

        with open(registry_file, 'w') as f:
            json.dump(registry, f, indent=2)

    def show_installation_tree(self):
        """Display installed files as a tree"""
        tree = Tree("[bold green]📁 Installed Files[/bold green]")

        # Group files by directory
        file_groups = {}
        for file_path in self.installed_files:
            parent = str(file_path.parent)
            if parent not in file_groups:
                file_groups[parent] = []
            file_groups[parent].append(file_path.name)

        for directory, files in file_groups.items():
            dir_branch = tree.add(f"[cyan]{directory}[/cyan]")
            for file in files:
                if file.endswith('.md'):
                    dir_branch.add(f"[green]📄 {file}[/green]")
                elif file.endswith('.yaml'):
                    dir_branch.add(f"[yellow]⚙️ {file}[/yellow]")
                else:
                    dir_branch.add(f"[blue]📁 {file}[/blue]")

        self.console.print(tree)

    def show_usage_instructions(self):
        """Display usage instructions"""
        instructions = Panel(
            "[bold green]✅ Installation Complete![/bold green]\n\n"
            "[bold cyan]To use hooliGAN-harness:[/bold cyan]\n\n"
            "1. Start Claude Code\n"
            "2. Invoke the harness with:\n"
            "   [yellow]/harness \"Your feature request\"[/yellow]\n\n"
            "[bold cyan]Example:[/bold cyan]\n"
            "   [yellow]/harness \"Add user authentication with JWT\"[/yellow]\n\n"
            "[bold cyan]The framework will:[/bold cyan]\n"
            "• Create a structured plan\n"
            "• Review architecture before coding\n"
            "• Generate implementation\n"
            "• Run parallel security & functional evaluation\n"
            "• Learn from any failures\n"
            "• Auto-generate documentation",
            border_style="green",
            box=box.DOUBLE,
            title="[bold]🎉 Success![/bold]",
            title_align="center"
        )
        self.console.print(instructions)

    def uninstall(self) -> bool:
        """Uninstall hooliGAN-harness"""
        self.console.print("[bold red]🗑️  Uninstalling hooliGAN-harness...[/bold red]")

        skills_dir = self.claude_path["global_skills"]
        agents_dir = self.claude_path["global_agents"]

        # Remove persona files
        persona_files = [
            "harness-planner.md",
            "harness-architect.md",
            "harness-generator.md",
            "harness-evaluator.md",
            "harness-security-evaluator.md"
        ]

        for persona in persona_files:
            persona_path = agents_dir / persona
            if persona_path.exists():
                persona_path.unlink()
                self.console.print(f"[red]Removed {persona}[/red]")

        # Remove skills directory
        if skills_dir.exists():
            shutil.rmtree(skills_dir)
            self.console.print(f"[red]Removed {skills_dir}[/red]")

        # Update registry
        registry_file = self.claude_path["config"] / "skills.json"
        if registry_file.exists():
            with open(registry_file, 'r') as f:
                registry = json.load(f)
            registry["skills"] = [s for s in registry.get("skills", []) if s.get("name") != "hooliGAN-harness"]
            with open(registry_file, 'w') as f:
                json.dump(registry, f, indent=2)

        self.console.print("[green]✅ Uninstallation complete![/green]")
        return True

    def run(self):
        """Main installation flow"""
        try:
            # Welcome
            self.show_banner()

            # Detect environment
            self.show_environment_status()

            # Check if already installed
            already_installed = (self.claude_path["global_skills"] / "SKILL.md").exists()

            if already_installed:
                self.console.print(f"[yellow]⚠️  hooliGAN-harness is already installed[/yellow]")

                action = Prompt.ask(
                    "\nWhat would you like to do?",
                    choices=["reinstall", "uninstall", "cancel"],
                    default="cancel"
                )

                if action == "cancel":
                    self.console.print("[yellow]Installation cancelled.[/yellow]")
                    return
                elif action == "uninstall":
                    self.uninstall()
                    return
                elif action == "reinstall":
                    # Create backup before reinstalling
                    self.create_backup(self.claude_path["global_skills"])

            # Show features
            self.show_features()

            # Confirm installation
            if not Confirm.ask(f"\n[bold cyan]Proceed with installation?[/bold cyan]", default=True):
                self.console.print("[yellow]Installation cancelled.[/yellow]")
                return

            # Install
            if self.install_files():
                self.console.print("\n[bold green]✨ Installation successful![/bold green]")
                self.show_installation_tree()
                self.show_usage_instructions()
            else:
                self.console.print("[bold red]❌ Installation failed![/bold red]")
                sys.exit(1)

        except KeyboardInterrupt:
            self.console.print("\n[yellow]Installation cancelled by user.[/yellow]")
            sys.exit(0)
        except Exception as e:
            self.console.print(f"\n[bold red]❌ Error: {e}[/bold red]")
            sys.exit(1)

def main():
    """Entry point"""
    installer = HooliganInstaller()
    installer.run()

if __name__ == "__main__":
    main()