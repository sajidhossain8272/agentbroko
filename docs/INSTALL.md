# Installation & Setup Guide

AgentBroko can be added to any project workspace to empower AI coding agents with Video Forge and PDF Playbook capabilities.

## 1. Quick Setup in Any Workspace (Recommended)

Run directly in your project root:
```bash
npx agentbroko init
```

This automatically configures:
- `.agents/skills/video-forge/SKILL.md` (Video Forge skill contract)
- `.agents/skills/pdf-playbook/SKILL.md` (PDF Playbook skill contract)
- `.agents/skills/pdf/SKILL.md` (Offline PDF tools)
- `.agents/AGENTS.md` and `.cursorrules` (IDE agent instructions)

---

## 2. NPM Package Installation

### Local Development Dependency:
```bash
npm install -D agentbroko
```

### Global Terminal CLI:
```bash
npm install -g agentbroko
```

---

## 3. Python Package Installation

```bash
git clone https://github.com/sajidhossain8272/agentbroko.git
cd agentbroko
pip install -e .
```

---

## 4. Prerequisites for Video Rendering

- **Python 3.10+**
- **FFmpeg & FFprobe**: Ensure `ffmpeg` is available on your system `PATH`.
  - Windows: `winget install Gyan.FFmpeg` or `choco install ffmpeg`
  - macOS: `brew install ffmpeg`
  - Ubuntu/Debian: `sudo apt install ffmpeg`
