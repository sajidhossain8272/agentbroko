"""
Installer that provisions standard .agents/skills/ for coding agents (Antigravity, Cursor, Cline, Roo, Windsurf).
"""
import os
from pathlib import Path

VIDEO_FORGE_SKILL_MD = """---
name: video-forge
description: Local video editing, procedural timeline assembly, speech narration, and synchronized caption rendering via FFmpeg. Use whenever the user asks to generate, edit, or produce short/long videos, speech voiceovers, or subtitles.
---

# Video Forge Skill Guide

Use Video Forge to build broadcast-quality MP4 videos, vertical shorts (9:16), or landscape ads (16:9) entirely on your local machine with zero external cloud dependencies.

## Standard Workflow for Coding Agents

### 1. Initialize a Video Project
When the user asks to create a video:
```bash
npx agentbroko video-forge init <project-folder>
```
This generates:
- `<project-folder>/project.json`: Timeline, clips, audio, and subtitle specifications.
- `<project-folder>/script.txt`: Spoken voiceover narration script.
- `<project-folder>/audio/`: Folder for generated speech `.wav` and background music.
- `<project-folder>/captions/`: Folder for generated `.srt` subtitles.
- `<project-folder>/media/`: Folder for input clips or images.
- `<project-folder>/outputs/`: Target folder for the rendered `final.mp4`.

### 2. Synthesize Speech & Subtitles
Write the voiceover script to `<project-folder>/script.txt` and run:
```bash
# Generate offline speech narration
npx agentbroko video-forge speak --file <project-folder>/script.txt --output <project-folder>/audio/narration.wav

# Generate synchronized SRT subtitles
npx agentbroko video-forge captions --file <project-folder>/script.txt --output <project-folder>/captions/subtitles.srt
```

### 3. Assemble and Validate `project.json`
Define the scenes, clips, aspect ratio, and transitions in `project.json`:
```json
{
  "output": "outputs/final.mp4",
  "title": "My Product Launch Video",
  "video": { "width": 1080, "height": 1920, "fps": 60 },
  "clips": [
    { "source": "media/clip-01.mp4", "start": 0, "duration": 5, "speed": 1, "volume": 1 }
  ],
  "audio": {
    "narration": "audio/narration.wav",
    "music": "audio/bed.mp3",
    "music_volume": 0.12
  },
  "subtitles": "captions/subtitles.srt"
}
```
Validate the schema before rendering:
```bash
npx agentbroko video-forge validate <project-folder>/project.json
```

### 4. Render the Final MP4
```bash
npx agentbroko video-forge render <project-folder>/project.json
```
"""

PDF_PLAYBOOK_SKILL_MD = """---
name: pdf-playbook
description: Publication-grade 20-page developer handbook and technical documentation PDF generation using ReportLab. Use whenever the user asks to generate a guide, book, playbook, handbook, or multi-page documentation PDF.
---

# PDF Playbook Skill Guide

Use PDF Playbook to generate styled, multi-page, publication-ready A4 developer handbooks with custom typography, structured tables, checklists, and code snippets.

## Standard Workflow for Coding Agents

### Option 1: Generate via Custom AI Blueprint (Recommended for Agents)
As an AI coding agent, write a structured JSON specification `playbook_spec.json`:
```json
{
  "title": "Production AI Agent Architecture",
  "audience": "Senior Software Engineers",
  "topic": "Master deterministic agent loops, model routing, and local skills",
  "chapters": [
    {
      "title": "Chapter 1: The Local-First Architecture",
      "lead": "Why local skills outperform brittle cloud webhooks.",
      "items": [
        ["Core Principle", "Run execution loops locally with zero cloud telemetry."],
        ["Deterministic Contracts", "Use strict JSON schemas and standard exit codes."],
        ["Cost Control", "Route heavy reasoning only when deterministic code is insufficient."]
      ]
    }
  ]
}
```
Then compile the 20-page PDF with ReportLab:
```bash
npx agentbroko pdf-playbook --spec playbook_spec.json --output playbook.pdf
```

### Option 2: Automated AI Generation
If a Gemini / OpenAI API key or local Ollama is available:
```bash
npx agentbroko pdf-playbook --non-interactive --title "My Title" --audience "My Audience" --topic "Core Promise" --output playbook.pdf
```
"""

PDF_TOOLS_SKILL_MD = """---
name: pdf
description: Offline local PDF inspection, text extraction, and page rendering with zero cloud upload.
---

# PDF Tools Skill Guide

Use local PDF tools to inspect metadata, extract text, and render pages offline:

```bash
# 1. Inspect metadata & page count
npx agentbroko pdf info document.pdf

# 2. Extract clean UTF-8 text to file
npx agentbroko pdf text document.pdf --output extracted.txt

# 3. Render all pages as high-resolution PNG images
npx agentbroko pdf render document.pdf --output rendered-pages/
```
"""

AGENTS_MD = """# AgentBroko Skills in This Workspace

This workspace is equipped with **AgentBroko Local AI Skills**. Whenever the user asks you to produce or edit media, use the installed skills:

1. **🎬 Video Forge (`.agents/skills/video-forge/SKILL.md`)**:
   - Create 9:16 vertical shorts, reels, or landscape videos.
   - Synthesize offline speech voiceover (`npx agentbroko video-forge speak`).
   - Extract auto-timed SRT subtitles (`npx agentbroko video-forge captions`).
   - Render multi-track MP4 videos (`npx agentbroko video-forge render project.json`).

2. **📄 PDF Playbook (`.agents/skills/pdf-playbook/SKILL.md`)**:
   - Generate structured 20-page developer handbooks, guides, and documentation.
   - Write structured `spec.json` and compile via `npx agentbroko pdf-playbook --spec spec.json --output out.pdf`.

3. **📑 PDF Tools (`.agents/skills/pdf/SKILL.md`)**:
   - Inspect PDF metadata, extract text, and render page images offline.
"""


def install_skills(target_dir: str | Path = ".") -> list[str]:
    """Provisions .agents/skills/ in the target directory."""
    root = Path(target_dir).resolve()
    skills_dir = root / ".agents" / "skills"
    
    created_files = []

    # 1. Video Forge Skill
    vf_dir = skills_dir / "video-forge"
    vf_dir.mkdir(parents=True, exist_ok=True)
    vf_path = vf_dir / "SKILL.md"
    vf_path.write_text(VIDEO_FORGE_SKILL_MD.strip(), encoding="utf-8")
    created_files.append(str(vf_path))

    # 2. PDF Playbook Skill
    pdf_dir = skills_dir / "pdf-playbook"
    pdf_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = pdf_dir / "SKILL.md"
    pdf_path.write_text(PDF_PLAYBOOK_SKILL_MD.strip(), encoding="utf-8")
    created_files.append(str(pdf_path))

    # 3. PDF Tools Skill
    tools_dir = skills_dir / "pdf"
    tools_dir.mkdir(parents=True, exist_ok=True)
    tools_path = tools_dir / "SKILL.md"
    tools_path.write_text(PDF_TOOLS_SKILL_MD.strip(), encoding="utf-8")
    created_files.append(str(tools_path))

    # 4. Workspace AGENTS.md
    agents_md_path = root / ".agents" / "AGENTS.md"
    agents_md_path.write_text(AGENTS_MD.strip(), encoding="utf-8")
    created_files.append(str(agents_md_path))

    # 5. Cursor rules compatibility
    cursor_rules_path = root / ".cursorrules"
    if not cursor_rules_path.exists():
        cursor_rules_path.write_text(AGENTS_MD.strip(), encoding="utf-8")
        created_files.append(str(cursor_rules_path))

    return created_files
