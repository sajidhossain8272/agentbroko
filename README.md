# AgentBroko

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://python.org)
[![NPM Version](https://img.shields.io/npm/v/agentbroko.svg)](https://www.npmjs.com/package/agentbroko)
[![Vercel Deployment](https://img.shields.io/badge/Vercel-Deployed-black.svg)](https://vercel.com)

> **AgentBroko** is an autonomous AI executive operating system and local-first skills hub for developers, coding agents, and creative tools. Built on an authoritative master runtime with a live Vercel serverless dashboard, AgentBroko observes its environment, reasons about opportunities, executes software tasks, and powers developer skills including **Video Forge** and **PDF Playbook**.

---

## 🚀 Quick Start

### 1. NPM Package Launcher
```bash
npx agentbroko skills
# or install globally
npm install -g agentbroko
agentbroko skills
```

### 2. Python Package & CLI
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -e .
agentbroko skills
```

### 3. Vercel Live Deployment
AgentBroko includes a full serverless web dashboard and JSON API for Vercel:
- **Web Dashboard**: Interactive real-time Control Center UI (`/`)
- **Health Check**: `/api/health`
- **Agent Status**: `/api/agent/status`
- **Skills Registry**: `/api/skills`
- **Goals & Tasks**: `/api/goals`, `/api/tasks`

---

## 🛠️ Built-in Skills

### 1. Video Forge (Offline Video Automation)
```bash
agentbroko video-forge doctor
agentbroko video-forge init my-video
agentbroko video-forge validate my-video/project.json
agentbroko video-forge render my-video/project.json
agentbroko video-forge speak --file my-video/script.txt --output my-video/audio/narration.wav
agentbroko video-forge captions --file my-video/script.txt --output my-video/captions/subtitles.srt
```

### 2. PDF Playbook & Local PDF Utilities
```bash
agentbroko pdf-playbook --output my-guide.pdf
agentbroko pdf info document.pdf
agentbroko pdf text document.pdf --output document.txt
agentbroko pdf render document.pdf --output rendered-pages
```

---

## 🏛️ System Architecture

```text
                               AgentRuntime (Singleton Lock)
                                             |
                                             v
                                      ExecutiveBrain
                                             |
        +------------------+-----------------+------------------+
        |                  |                 |                  |
SituationAnalyzer     GoalManager    OpportunityEngine    ExperimentEngine
        |                  |                 |                  |
        +------------------+-----------------+------------------+
                                             |
                                             v
                                     Capability Router
              (Moltbook, GitHub, Business, Wallet, Video Forge, PDF Playbook)
                                             |
                                             v
                        VERIFY -> LEARN -> MEMORY (9 Categories)
                                             |
                                             v
                             AgentEventBus & RevenueEngine
                                             |
                                             v
                   VERCEL SERVERLESS CONTROL CENTER WEB DASHBOARD (api/index.py)
```

---

## 📁 Repository Structure

```
.
├── api/
│   └── index.py                    # Vercel Serverless Function & Live Dashboard entrypoint
├── bin/
│   └── agentbroko.js               # Node.js / NPM CLI executable
├── src/
│   ├── agentbroko/                 # Master CLI & skill registry
│   ├── video_forge/                # Video Forge video engine
│   └── pdf_playbook/               # PDF handbook generator
├── static/
│   └── control_center.html         # Interactive web control center UI
├── docs/                           # Complete documentation suite
├── package.json                    # NPM package configuration
├── pyproject.toml                  # Python package & Vercel entrypoint specification
├── vercel.json                     # Vercel Serverless routing configuration
└── requirements.txt                # Python runtime dependencies
```

---

## 📖 Documentation

- [Installation](docs/INSTALL.md) and [Quickstart](docs/QUICKSTART.md)
- [Complete Usage Guide](docs/USAGE.md)
- [Architecture](docs/ARCHITECTURE.md) and [Tech Stack](docs/TECH_STACK.md)
- [Video Forge Guide](docs/PROJECT.md) and [Offline TTS](docs/TTS.md)
- [PDF Skill](docs/PDF.md) and [PDF Playbook](docs/PDF_PLAYBOOK.md)
- [Contributing](CONTRIBUTING.md) and [Adding a Skill](docs/ADDING_A_SKILL.md)
- [Security](SECURITY.md), [Privacy](PRIVACY.md), and [License](LICENSE)
