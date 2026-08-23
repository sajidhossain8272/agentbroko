from __future__ import annotations
import argparse
import os
from pathlib import Path
from .generator import generate_playbook

def _ask(prompt: str, default: str = "") -> str:
    value = input(f"{prompt}{f' [{default}]' if default else ''}: ").strip()
    return value or default

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="agentbroko pdf-playbook",
        description="Generate a publication-ready 20-page developer or custom topic playbook PDF"
    )
    parser.add_argument("--output", default="agentbroko-playbook.pdf", help="Output PDF file path")
    parser.add_argument("--title", default="The Modern AI Engineering Playbook", help="Playbook or guide title")
    parser.add_argument("--audience", default="Developers & Engineers", help="Target audience")
    parser.add_argument("--topic", default="Step-by-step practical guide to mastering your workflow", help="Core promise / topic")
    parser.add_argument("--api-key", default=None, help="Optional Gemini or OpenAI API Key for AI deep generation (default: uses built-in smart engine)")
    parser.add_argument("--remove-branding", action="store_true", help="Reserved for a future premium edition")
    parser.add_argument("--non-interactive", action="store_true", help="Run in headless non-interactive mode")
    
    args = parser.parse_args(argv)
    answers = {
        "title": args.title,
        "audience": args.audience,
        "topic": args.topic,
        "api_key": args.api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY") or os.environ.get("OPENAI_API_KEY")
    }

    if not args.non_interactive:
        print("AgentBroko PDF Playbook Generator")
        answers["title"] = _ask("Guide title", args.title)
        answers["audience"] = _ask("Primary audience", args.audience)
        answers["topic"] = _ask("Core promise / topic", args.topic)
        if not answers["api_key"]:
            ai_choice = _ask("AI API Key for deep generation (Gemini/OpenAI, or press Enter for built-in smart engine)", "")
            if ai_choice:
                answers["api_key"] = ai_choice

    try:
        path = generate_playbook(
            Path(args.output),
            answers,
            remove_branding=args.remove_branding,
            api_key=answers.get("api_key")
        )
    except ValueError as exc:
        parser.error(str(exc))

    print(f"Created branded AgentBroko PDF: {path.resolve()}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
