# Installation & Setup Guide

AgentBroko can be added to any project workspace to empower AI coding agents with Video Forge and PDF Playbook capabilities.

---

## 1. Quick Setup in Any Workspace (Recommended)

### Option A: Install All Skills
Run directly in your project root:
```bash
npx agentbroko init
```

### Option B: Install a Specific Skill
```bash
# Add Video Forge (video editing, voiceovers, captions)
npx agentbroko add video-forge

# Add PDF Playbook (20-page developer handbook synthesis)
npx agentbroko add pdf-playbook

# Add Offline PDF Tools
npx agentbroko add pdf
```

### Option C: Clone Full Starter Repo
```bash
npx agentbroko clone my-agent-workspace
```

This automatically configures:
- `.agents/skills/<skill>/SKILL.md` (Skill definitions & contracts)
- `.agents/skills/<skill>/examples/` (Sample specs & templates)
- `.agents/AGENTS.md`, `.cursorrules`, and `CLAUDE.md` (Agent instructions + 🆘 emergency recovery guide)

---

## 2. Diagnose Your Environment

Run the doctor command to verify all required dependencies (FFmpeg, Python, ReportLab, TTS):
```bash
npx agentbroko doctor
```

---

## 3. Package Installation Options

### Global NPM CLI:
```bash
npm install -g agentbroko
agentbroko init
```

### Local Project Dependency:
```bash
npm install -D agentbroko
```

### Python Package Install:
```bash
git clone https://github.com/sajidhossain8272/agentbroko.git
cd agentbroko
pip install -e .
```

---

## 4. Prerequisites & Installation Commands

- **Python 3.10+** (standard requirement)
- **FFmpeg & FFprobe** (required for Video Forge video rendering):
  - **Windows**: `winget install Gyan.FFmpeg` or `choco install ffmpeg`
  - **macOS**: `brew install ffmpeg`
  - **Ubuntu/Debian**: `sudo apt install ffmpeg`
- **ReportLab** (required for PDF Playbook):
  - `python -m pip install reportlab`
