from __future__ import annotations
import argparse
import shutil
import sys
from pathlib import Path
from video_forge.cli import main as video_forge_main
from .pdf_skill import main as pdf_main
from .skills_installer import install_skills, clone_repository, SKILL_REGISTRY
from . import __version__

SKILLS = {
    "video-forge": "Local video editing, offline narration, subtitles, and FFmpeg assembly",
    "pdf-playbook": "Premium branded 20-page developer handbook PDF generation with ReportLab",
    "pdf": "Offline local PDF metadata inspection, text extraction, and page rendering",
}

AGENT_GUIDE_TEXT = """
╔══════════════════════════════════════════════════════════════════════════╗
║               AGENTBROKO AI AGENT INSTRUCTION & RECOVERY GUIDE          ║
╚══════════════════════════════════════════════════════════════════════════╝

► Core Philosophy:
  AgentBroko empowers AI Coding Agents (Google Antigravity, Cursor, Cline,
  Roo, Windsurf, Claude Code) to build production media locally without
  cloud API keys or third-party webhooks.

► Available Skills:
  1. video-forge   - Video editing, speech voiceovers, captions, and FFmpeg renders.
  2. pdf-playbook  - 20-page developer handbook synthesis with ReportLab.
  3. pdf           - Local PDF metadata, text extraction, and page rendering.

► Adding Skills to a Project:
  - Install all skills:     npx agentbroko init
  - Install single skill:   npx agentbroko add video-forge
  - Install PDF Playbook:   npx agentbroko add pdf-playbook

► 🆘 What to Do if an Agent is Stuck / Facing Errors:
  1. Missing Local Tools (FFmpeg/FFprobe):
     - Run: npx agentbroko doctor
     - Windows: winget install Gyan.FFmpeg
     - macOS:   brew install ffmpeg
     - Linux:   sudo apt install ffmpeg

  2. Missing ReportLab for PDF Playbook:
     - Run: python -m pip install reportlab

  3. Video Rendering Fails:
     - Always run: npx agentbroko video-forge validate <project.json>
     - Verify media paths and file formats before calling render.

  4. Audio Narration Fails or is Silent:
     - Run test synthesis: npx agentbroko video-forge speak --text "Test" -o test.wav
     - Inspect audio waveform: ffprobe audio/narration.wav

  5. Inspect Media Specs Locally:
     - Run: ffprobe -v error -show_entries stream=width,height,duration -of default=noprint_wrappers=1 <file>
"""

def print_skills_menu() -> None:
    print("\n╔══════════════════════════════════════════════════════════════════╗")
    print("║            AgentBroko Autonomous AI Skills Hub                   ║")
    print("╚══════════════════════════════════════════════════════════════════╝\n")
    print("Available Skills:")
    for name, meta in SKILL_REGISTRY.items():
        print(f"  • {name:<14} : {meta['description']}")
    print("\nWorkspace Setup Commands:")
    print("  agentbroko init                  Provision all skills (.agents/skills/) in workspace")
    print("  agentbroko init <skill>          Provision a single skill (e.g. agentbroko init video-forge)")
    print("  agentbroko add <skill>           Add a specific skill to workspace (video-forge, pdf-playbook, pdf)")
    print("  agentbroko clone [dir]           Clone full AgentBroko starter repository")
    print("  agentbroko doctor                Diagnose local FFmpeg, Python, ReportLab, and TTS engines")
    print("  agentbroko guide                 Show complete AI coding agent execution and stuck recovery guide")
    print("\nDirect Skill Commands:")
    print("  agentbroko video-forge ...       Execute Video Forge CLI")
    print("  agentbroko pdf-playbook ...      Execute PDF Playbook CLI")
    print("  agentbroko pdf ...               Execute PDF Tools CLI")
    print("\nDocumentation: https://agentbroko.vercel.app | GitHub: https://github.com/sajidhossain8272/agentbroko\n")


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    # Fast route for version
    if "--version" in argv or "-v" in argv:
        print(f"agentbroko {__version__}")
        return 0

    if not argv or argv[0] in ("skills", "list", "help", "--help", "-h"):
        print_skills_menu()
        return 0

    command = argv[0]
    rest = argv[1:]

    # 1. Guide / Agent recovery command
    if command in ("guide", "agent-rules", "troubleshooting", "stuck"):
        print(AGENT_GUIDE_TEXT)
        return 0

    # 2. Doctor command
    if command == "doctor":
        print("AgentBroko System Diagnostics:")
        print(f"  • Python:   {sys.version.split()[0]} ({sys.executable})")
        print(f"  • FFmpeg:   {'✓ found' if shutil.which('ffmpeg') else '✗ missing (run: winget install Gyan.FFmpeg or brew install ffmpeg)'}")
        print(f"  • FFprobe:  {'✓ found' if shutil.which('ffprobe') else '✗ missing'}")
        
        try:
            import reportlab
            print(f"  • ReportLab: ✓ found (v{reportlab.__version__})")
        except ImportError:
            print("  • ReportLab: ✗ missing (run: python -m pip install reportlab)")

        # Run Video Forge engine check
        print("\nVideo Forge Speech Engines:")
        return video_forge_main(["doctor"])

    # 3. Clone command
    if command == "clone":
        target = rest[0] if rest else "agentbroko"
        try:
            dest = clone_repository(target)
            print(f"✓ Successfully cloned AgentBroko repository to: {dest}")
            created = install_skills(dest)
            print(f"✓ Provisioned {len(created)} skill blueprints in {dest / '.agents'}")
            return 0
        except Exception as exc:
            print(f"Error cloning repository: {exc}", file=sys.stderr)
            return 1

    # 4. Add single skill command
    if command == "add":
        if not rest:
            print("Usage: agentbroko add <skill-name> [target-directory]")
            print(f"Available skills: {', '.join(SKILL_REGISTRY.keys())}")
            return 1
        
        skill_name = rest[0]
        target_dir = rest[1] if len(rest) > 1 else "."
        fetch_remote = "--remote" in rest or "--fetch" in rest
        
        try:
            created = install_skills(target_dir=target_dir, skill_name=skill_name, fetch_remote=fetch_remote)
            print(f"\n✓ Successfully added skill '{skill_name}' to workspace ({Path(target_dir).resolve()}):")
            for f in created:
                print(f"  + {f}")
            print("\nYour AI Coding Agent (Antigravity, Cursor, Cline, Roo) can now use this skill directly from your prompt!")
            return 0
        except Exception as exc:
            print(f"Error adding skill: {exc}", file=sys.stderr)
            return 1

    # 5. Init command (supports all skills or specific skill)
    if command in ("init", "install-skills"):
        # Check if first arg in rest is a skill name or directory
        skill_name = None
        target_dir = "."
        fetch_remote = "--remote" in rest or "--fetch" in rest

        filtered_rest = [arg for arg in rest if not arg.startswith("--")]

        if filtered_rest:
            if filtered_rest[0] in SKILL_REGISTRY or filtered_rest[0] == "all":
                skill_name = filtered_rest[0]
                if len(filtered_rest) > 1:
                    target_dir = filtered_rest[1]
            else:
                target_dir = filtered_rest[0]
                if len(filtered_rest) > 1 and filtered_rest[1] in SKILL_REGISTRY:
                    skill_name = filtered_rest[1]

        # Handle --skill flag
        if "--skill" in rest:
            idx = rest.index("--skill")
            if idx + 1 < len(rest):
                skill_name = rest[idx + 1]

        # Handle --clone flag
        if "--clone" in rest:
            try:
                dest = clone_repository(target_dir if target_dir != "." else "agentbroko")
                target_dir = str(dest)
            except Exception as exc:
                print(f"Error cloning repository: {exc}", file=sys.stderr)
                return 1

        try:
            created = install_skills(target_dir=target_dir, skill_name=skill_name, fetch_remote=fetch_remote)
            installed_label = f"'{skill_name}'" if skill_name and skill_name != "all" else "all skills"
            print(f"\n✓ Successfully initialized AgentBroko ({installed_label}) in workspace ({Path(target_dir).resolve()}):")
            for f in created:
                print(f"  + {f}")
            print("\nYour AI Coding Agent (Antigravity, Cursor, Cline, Roo, Windsurf) can now use AgentBroko skills directly from your prompt!")
            return 0
        except Exception as exc:
            print(f"Error during workspace initialization: {exc}", file=sys.stderr)
            return 1

    # 6. Video Forge execution
    if command == "video-forge":
        return video_forge_main(rest)

    # 7. PDF Tools execution
    if command == "pdf":
        return pdf_main(rest)

    # 8. PDF Playbook execution
    if command == "pdf-playbook":
        try:
            from pdf_playbook.cli import main as pdf_playbook_main
        except ModuleNotFoundError as exc:
            if exc.name == "reportlab":
                print("PDF Playbook requires ReportLab. Install it with: python -m pip install reportlab")
                return 2
            raise
        return pdf_playbook_main(rest)

    print(f"Unknown command: '{command}'")
    print_skills_menu()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
