# 🚀 hooliGAN-harness Installation Guide

## Quick Start

### macOS / Linux
```bash
./setup.sh
```

### Windows
```batch
setup.bat
```

### Manual Installation with Python
```bash
# Install dependencies
pip install rich

# Run installer
python install.py
```

## What Gets Installed

The installer will add the following components to your Claude Code and/or Codex installation:

### Skills Directory
- `~/.claude/skills/hooliGAN-harness/` or `~/.codex/skills/hooliGAN-harness/`
  - `SKILL.md` - Main skill definition
  - `README.md` - Documentation
  - `.harness/` - Configuration and knowledge base
    - `knowledge/` - Failure patterns and confidence scoring
    - `evolution/` - Cross-session learning patterns
    - `rollback/` - Rollback strategies
    - `collaboration/` - Multi-generator configuration
    - `integrations/` - External tool integrations
    - `documentation/` - Living documentation config

### Agent Personas
- `~/.claude/agents/` or `~/.codex/agents/`
  - `harness-planner.md` - Plans tasks and creates YAML roadmaps
  - `harness-architect.md` - Reviews plans for architectural impacts
  - `harness-generator.md` - Implements code following best practices
  - `harness-evaluator.md` - Adversarial functional evaluation
  - `harness-security-evaluator.md` - Parallel security scanning

## Installation Options

The installer provides three modes:

1. **Claude Code Only** - Installs to `~/.claude/`
2. **Codex Only** - Installs to `~/.codex/`
3. **Both** - Installs to both environments

## Features

### 🧠 Intelligence Layer
- **Failure Pattern Memory**: Learns from past failures to prevent recurrence
- **Confidence Scoring**: Adapts validation rigor (0-100% confidence)
- **Cross-Session Learning**: Discovers and refines patterns over time

### 🛡️ Reliability Layer
- **Architect Review**: Pre-implementation design validation
- **Automatic Rollback**: Snapshots and recovery on critical failures
- **Parallel Evaluation**: Security and functional checks run simultaneously

### 🚀 Scale Layer
- **Multi-Generator Mode**: Specialized generators work in parallel
- **Enterprise Integrations**: GitHub Actions, Jenkins, SonarQube, Datadog
- **Living Documentation**: Auto-generated API specs and diagrams

## System Requirements

- **Python**: 3.8 or higher
- **Claude Code** or **Codex**: At least one must be installed
- **Dependencies**: Automatically installed by setup scripts
  - `rich` - Beautiful terminal UI
  - `uv` (optional) - Fast Python package manager

## Usage

After installation, use the harness in your Claude Code or Codex session:

```bash
/harness "Add user authentication with JWT and rate limiting"
```

The framework will:
1. Create a structured YAML plan
2. Review architecture before coding
3. Generate implementation with tests
4. Run parallel security & functional evaluation
5. Learn from any failures
6. Auto-generate documentation

## Advanced Configuration

### Enable Multi-Generator Mode
Edit `.harness/collaboration/multi-generator.yaml`:
```yaml
multi_generator_configuration:
  enabled: true  # Set to true
  max_parallel_generators: 3
```

### Configure External Integrations
Edit `.harness/integrations/external-tools.yaml` to enable:
- CI/CD pipelines (GitHub Actions, Jenkins, GitLab CI)
- Monitoring (Datadog, Sentry, Prometheus)
- Security scanning (Snyk, SonarQube, Veracode)
- Documentation (Confluence, Notion, Docusaurus)

### Adjust Confidence Thresholds
Edit `.harness/knowledge/confidence-scoring.yaml` to customize validation levels.

## Uninstallation

To remove hooliGAN-harness:

```bash
# Run the installer and select 'uninstall'
python install.py
```

Or manually remove:
- `~/.claude/skills/hooliGAN-harness/`
- `~/.codex/skills/hooliGAN-harness/`
- Agent files from `~/.claude/agents/harness-*.md`
- Agent files from `~/.codex/agents/harness-*.md`

## Troubleshooting

### "No Claude Code or Codex installation detected"
- Ensure Claude Code or Codex is installed
- Check that `~/.claude/` or `~/.codex/` directories exist

### "Permission denied" errors
- On macOS/Linux: `chmod +x setup.sh`
- Run with appropriate permissions

### "uv not found"
- The installer will attempt to install uv automatically
- Manual installation: https://github.com/astral-sh/uv

### "Python version too old"
- Upgrade to Python 3.8 or higher
- Check version: `python --version` or `python3 --version`

## Support

- **Repository**: https://github.com/aditikilledar/hooligan-harness
- **Issues**: https://github.com/aditikilledar/hooligan-harness/issues
- **Documentation**: See README.md for framework details

## License

MIT License - See LICENSE file for details