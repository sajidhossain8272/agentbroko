from __future__ import annotations
import argparse
from video_forge.cli import main as video_forge_main
from .pdf_skill import main as pdf_main
from . import __version__

SKILLS = {
    "video-forge": "Local video editing, offline narration, and captions",
    "pdf": "Local PDF inspection, text extraction, and page rendering",
    "pdf-playbook": "Premium branded developer handbook PDF generation",
}

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="agentbroko", description="AgentBroko local skills hub")
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument("command", nargs="?", choices=["skills", "doctor", "video-forge", "pdf", "pdf-playbook"], default="skills")
    args, rest = parser.parse_known_args(argv)
    if args.command in ("skills", None):
        print("AgentBroko skills")
        for name, description in SKILLS.items(): print(f"  {name:<14} {description}")
        print("\nUse: agentbroko <skill> <command> [options]")
        return 0
    if args.command == "video-forge": return video_forge_main(rest)
    if args.command == "pdf": return pdf_main(rest)
    if args.command == "pdf-playbook":
        try:
            from pdf_playbook.cli import main as pdf_playbook_main
        except ModuleNotFoundError as exc:
            if exc.name == "reportlab":
                print("PDF Playbook requires ReportLab. Install it with: python -m pip install reportlab")
                return 2
            raise
        return pdf_playbook_main(rest)
    print("AgentBroko: ready\nInstalled skills:")
    for name, description in SKILLS.items(): print(f"  {name}: {description}")
    return video_forge_main(["doctor"])

if __name__ == "__main__": raise SystemExit(main())
