"""
AgentBroko Skills Installer & Workspace Provisioner.
Provisions .agents/skills/, .agents/AGENTS.md, .cursorrules, and CLAUDE.md for AI coding agents
(Google Antigravity, Cursor, Cline, Roo Code, Windsurf, Claude Code, GitHub Copilot).
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

GITHUB_REPO_RAW = "https://raw.githubusercontent.com/sajidhossain8272/agentbroko/main"

VIDEO_FORGE_SKILL_MD = """---
name: video-forge
description: 10/10 Procedural and cinematic video engine, prompt-to-video generation, vertical shorts/reels synthesis, neural VO narration, and FFmpeg assembly. Use whenever the user asks to generate, edit, or produce marketing ads, storytelling shorts, voiceovers, or kinetic subtitles.
---

# Video Forge Skill Guide

Use Video Forge to build broadcast-quality MP4 videos, 9:16 vertical shorts, or 16:9 landscape product ads entirely on your local machine with zero external cloud dependencies.

## Key Capabilities

1. **Prompt-to-Video Generator**:
   Transform a natural language brief into a finished procedural ad video:
   ```bash
   npx agentbroko video-forge generate "60s ad for MyProduct, an autonomous developer OS" --name myproduct --accent "#3B5BFF" --seconds 30
   ```

2. **9:16 Vertical Storytelling Shorts & Reels Engine**:
   Generate cinematic vertical shorts with atmospheric sandstone ridges, 3D parallax dunes, volumetric god rays, particle physics, and kinetic subtitles:
   ```bash
   npx agentbroko video-forge short --type story --theme golden -o outputs/story_short.mp4
   ```

3. **10/10 Procedural Motion Graphics (`spec.json`)**:
   Render multi-scene declarative specs with PIL + NumPy + FFmpeg rawvideo pipe:
   - 13+ Scene modules: `cold_open`, `statement`, `pill_list`, `message`, `node_stack`, `orbit`, `waveform`, `feature_grid`, `stat`, `split_compare`, `cta`, `logo_reveal`, `screenshot`.
   - Dynamic speech-driven scene duration solver.
   - Real-time audio ducking, loudness envelope detection, and peak limiting (-1.5 dBFS).
   - Render command:
     ```bash
     npx agentbroko video-forge render ads/demo/spec.json
     ```

4. **High-Fidelity Neural & Offline TTS (`speak`)**:
   ```bash
   # Neural Edge-TTS voice (high-fidelity, 100% free)
   npx agentbroko video-forge speak --text "Welcome to AgentBroko." --output audio/vo.wav --engine edge --voice en-US-ChristopherNeural

   # Native Windows SAPI, macOS say, or Linux espeak
   npx agentbroko video-forge speak --text "Welcome to AgentBroko." --output audio/vo.wav --engine auto
   ```

5. **Clip Timeline Assembly (`project.json`)**:
   ```bash
   npx agentbroko video-forge init my-video --template clips
   npx agentbroko video-forge render my-video/project.json
   ```

---

## 🆘 Agent Stuck / Troubleshooting Guide

If you encounter errors during video generation:
1. **FFmpeg / FFprobe Missing or Not Found**:
   - Run `npx agentbroko doctor` to diagnose.
   - Windows: `winget install Gyan.FFmpeg`
   - macOS: `brew install ffmpeg`
   - Linux: `sudo apt install ffmpeg`
2. **Missing Python Modules**:
   - `python -m pip install Pillow numpy reportlab`
   - Optional neural TTS: `python -m pip install edge-tts`
3. **Spec or Project Validation Fails**:
   - Run `npx agentbroko video-forge validate <file>` to view exact schema errors.
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
Then compile the PDF with ReportLab:
```bash
npx agentbroko pdf-playbook --spec playbook_spec.json --output playbook.pdf
```

### Option 2: Automated AI Generation
If a Gemini / OpenAI API key or local Ollama is available:
```bash
npx agentbroko pdf-playbook --non-interactive --title "My Title" --audience "My Audience" --topic "Core Promise" --output playbook.pdf
```

---

## 🆘 Agent Stuck / Troubleshooting Guide

If you encounter errors during PDF generation:
1. **ModuleNotFoundError: No module named 'reportlab'**:
   - Install ReportLab: `python -m pip install reportlab`
2. **Custom Spec JSON Validation Error**:
   - Ensure `playbook_spec.json` has top-level keys `"title"`, `"audience"`, `"topic"`, and a `"chapters"` array.
   - Each chapter requires `"title"`, `"lead"`, and `"items"` (array of `[title, description]` tuples).
3. **Layout or Overflow Issues**:
   - PDF Playbook automatically paginate tables and callout boxes across pages.
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

---

## 🆘 Agent Stuck / Troubleshooting Guide

If you encounter errors during PDF inspection or rendering:
1. **Password Protected PDFs**:
   - Offline PDF tools will report protected files. Ensure the PDF is unlocked.
2. **Missing Rendering Backend (pdftoppm / PyMuPDF)**:
   - Text extraction works out-of-the-box. For high-resolution image rasterization, ensure `pdftoppm` (poppler-utils) or `pymupdf` is installed.
"""

SAMPLE_PROJECT_JSON = {
    "output": "outputs/final.mp4",
    "title": "AgentBroko Demo Project",
    "video": {"width": 1080, "height": 1920, "fps": 60},
    "clips": [
        {"source": "media/clip-01.mp4", "start": 0, "duration": 5, "speed": 1, "volume": 1}
    ],
    "audio": {
        "narration": "audio/narration.wav",
        "music": "audio/bed.mp3",
        "music_volume": 0.12
    },
    "subtitles": "captions/subtitles.srt"
}

SAMPLE_PLAYBOOK_SPEC = {
    "title": "Autonomous Agent Playbook",
    "audience": "AI Engineers & Developers",
    "topic": "Deterministic local agent architecture and multi-modal synthesis",
    "chapters": [
        {
            "title": "Chapter 1: Local-First Foundations",
            "lead": "Building resilient agents that operate deterministically without cloud bottlenecks.",
            "items": [
                ["Local Runtime", "Execute tools, media synthesis, and PDF engines on the local host."],
                ["Zero Cloud Telemetry", "Never leak source media or private documents to third-party endpoints."],
                ["Structured Blueprints", "Validate JSON schemas before triggering expensive rendering passes."]
            ]
        }
    ]
}

SKILL_REGISTRY = {
    "video-forge": {
        "title": "🎬 Video Forge",
        "description": "10/10 Procedural video engine, prompt-to-video, vertical shorts, and neural speech",
        "skill_md": VIDEO_FORGE_SKILL_MD,
        "sample_file": ("examples/sample_project.json", json.dumps(SAMPLE_PROJECT_JSON, indent=2)),
        "command_hint": "npx agentbroko video-forge generate 'Brief' --seconds 30",
        "capabilities": ["video-generation", "reels-and-shorts", "subtitles", "narration", "ffmpeg-rendering"],
    },
    "pdf-playbook": {
        "title": "📄 PDF Playbook",
        "description": "Publication-grade 20-page developer handbook and technical documentation PDF generation",
        "skill_md": PDF_PLAYBOOK_SKILL_MD,
        "sample_file": ("examples/sample_spec.json", json.dumps(SAMPLE_PLAYBOOK_SPEC, indent=2)),
        "command_hint": "npx agentbroko pdf-playbook --spec playbook_spec.json --output out.pdf",
        "capabilities": ["pdf-generation", "playbooks", "documentation"],
    },
    "pdf": {
        "title": "📑 PDF Tools",
        "description": "Offline local PDF inspection, text extraction, and page rendering with zero cloud upload",
        "skill_md": PDF_TOOLS_SKILL_MD,
        "sample_file": None,
        "command_hint": "npx agentbroko pdf info document.pdf",
        "capabilities": ["pdf-inspection", "text-extraction", "page-rendering"],
    }
}


def search_skills(query: str | None = None) -> list[tuple[str, dict[str, object]]]:
    """Return a list of skills matching a search query. A blank query returns all skills."""
    query_tokens = (query or "").strip().lower().split()
    matches: list[tuple[str, dict[str, object]]] = []

    for name, meta in SKILL_REGISTRY.items():
        haystack = " ".join([
            name,
            str(meta.get("description", "")),
            *[str(item) for item in meta.get("capabilities", [])],
        ]).lower()
        if not query_tokens or all(token in haystack for token in query_tokens):
            matches.append((name, meta))

    return matches


def build_agents_md(installed_skills: list[str]) -> str:
    """Generates the master AGENTS.md document tailored to installed skills with deep agent instructions."""
    lines = [
        "# AgentBroko Skills in This Workspace",
        "",
        "This workspace is configured with **AgentBroko Local-First AI Skills**. Whenever the user asks you to produce, edit, inspect media, or build documentation, use the installed skills below:",
        ""
    ]

    for key in installed_skills:
        if key in SKILL_REGISTRY:
            meta = SKILL_REGISTRY[key]
            lines.append(f"### {meta['title']} (`.agents/skills/{key}/SKILL.md`)")
            lines.append(f"- **Purpose**: {meta['description']}")
            lines.append(f"- **Primary Command**: `{meta['command_hint']}`")
            lines.append("")

    lines.extend([
        "---",
        "",
        "## 🛠️ Mandatory Protocol for AI Coding Agents",
        "",
        "1. **Local-First Only**: Never send media files or sensitive PDFs to cloud APIs. Always process locally using the tools provided.",
        "2. **Validate Before Execution**: Always validate project JSON files using `npx agentbroko video-forge validate <path>` or verify spec schema before rendering.",
        "3. **Zero Hallucination of Flags**: Stick strictly to documented CLI arguments in `.agents/skills/<skill>/SKILL.md`.",
        "",
        "---",
        "",
        "## 🆘 Agent Stuck / Self-Recovery Protocol",
        "",
        "If you encounter a failure while executing tools:",
        "- **Missing FFmpeg**: Check with `npx agentbroko doctor`. On Windows run `winget install Gyan.FFmpeg`; on macOS run `brew install ffmpeg`.",
        "- **Missing ReportLab**: Run `python -m pip install reportlab`.",
        "- **TTS Audio Silent**: Check audio files with `ffprobe audio/narration.wav` or use `npx agentbroko video-forge speak --text \"...\" --output out.wav`.",
        "- **Schema Error**: Review the error output from `npx agentbroko video-forge validate project.json` and fix mismatched keys.",
        "- **Media Inspection**: Inspect resolution and duration locally using `ffprobe` before putting clips into `project.json`."
    ])

    return "\n".join(lines) + "\n"


def install_skills(
    target_dir: str | Path = ".",
    skill_name: str | None = None,
    fetch_remote: bool = False
) -> list[str]:
    """
    Provisions .agents/skills/ in the target directory.
    If skill_name is provided (e.g. 'video-forge', 'pdf-playbook', 'pdf'), only that skill is installed.
    If skill_name is None or 'all', all skills are installed.
    """
    root = Path(target_dir).resolve()
    skills_dir = root / ".agents" / "skills"
    
    if skill_name and skill_name != "all":
        target_keys = [skill_name.lower().strip()]
        if target_keys[0] not in SKILL_REGISTRY:
            valid_skills = ", ".join(SKILL_REGISTRY.keys())
            raise ValueError(f"Unknown skill '{skill_name}'. Valid skills are: {valid_skills}, all")
    else:
        target_keys = list(SKILL_REGISTRY.keys())

    created_files = []

    for key in target_keys:
        meta = SKILL_REGISTRY[key]
        dest_dir = skills_dir / key
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        skill_content = meta["skill_md"]
        
        # Optional remote fetch from GitHub if requested
        if fetch_remote:
            try:
                url = f"{GITHUB_REPO_RAW}/.agents/skills/{key}/SKILL.md"
                req = urllib.request.Request(url, headers={"User-Agent": "AgentBroko-Installer"})
                with urllib.request.urlopen(req, timeout=3.0) as resp:
                    if resp.status == 200:
                        skill_content = resp.read().decode("utf-8")
            except Exception:
                # Fallback directly to bundled content
                pass
                
        skill_path = dest_dir / "SKILL.md"
        skill_path.write_text(skill_content.strip() + "\n", encoding="utf-8")
        created_files.append(str(skill_path))

        # Sample template file if available
        if meta.get("sample_file"):
            rel_sample_path, sample_data = meta["sample_file"]
            sample_full_path = dest_dir / rel_sample_path
            sample_full_path.parent.mkdir(parents=True, exist_ok=True)
            if not sample_full_path.exists():
                sample_full_path.write_text(sample_data.strip() + "\n", encoding="utf-8")
                created_files.append(str(sample_full_path))

    # Detect existing installed skills in .agents/skills to keep AGENTS.md complete
    currently_installed = set(target_keys)
    if skills_dir.exists():
        for child in skills_dir.iterdir():
            if child.is_dir() and (child / "SKILL.md").exists():
                currently_installed.add(child.name)

    agents_md_content = build_agents_md(sorted(list(currently_installed)))

    # Master AGENTS.md
    agents_md_path = root / ".agents" / "AGENTS.md"
    agents_md_path.parent.mkdir(parents=True, exist_ok=True)
    agents_md_path.write_text(agents_md_content, encoding="utf-8")
    created_files.append(str(agents_md_path))

    # Cursor rules compatibility
    cursor_rules_path = root / ".cursorrules"
    cursor_rules_path.write_text(agents_md_content, encoding="utf-8")
    created_files.append(str(cursor_rules_path))

    # CLAUDE.md compatibility
    claude_md_path = root / "CLAUDE.md"
    if not claude_md_path.exists():
        claude_md_path.write_text(agents_md_content, encoding="utf-8")
        created_files.append(str(claude_md_path))

    return created_files


def clone_repository(target_dir: str | Path = "agentbroko") -> Path:
    """Clones the full AgentBroko repository into the target directory."""
    dest = Path(target_dir).resolve()
    repo_url = "https://github.com/sajidhossain8272/agentbroko.git"
    
    if dest.exists() and any(dest.iterdir()):
        raise RuntimeError(f"Target directory '{dest}' already exists and is not empty.")
        
    git_bin = shutil.which("git")
    if not git_bin:
        raise RuntimeError("Git is not found on your system. Please install Git or run 'agentbroko init' instead.")
        
    subprocess.run([git_bin, "clone", repo_url, str(dest)], check=True)
    return dest
