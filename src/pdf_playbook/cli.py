from __future__ import annotations
import argparse
from pathlib import Path
from .generator import generate_playbook

def _ask(prompt: str, default: str = "") -> str:
    value = input(f"{prompt}{f' [{default}]' if default else ''}: ").strip()
    return value or default

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="agentbroko pdf-playbook", description="Generate a branded AgentBroko developer playbook PDF")
    parser.add_argument("--output", default="agentbroko-playbook.pdf")
    parser.add_argument("--title", default="AgentRouter + Cline AI Credits Developer Playbook")
    parser.add_argument("--audience", default="Developers new to AgentRouter and Cline")
    parser.add_argument("--topic", default="Claim AI credits, connect Cline, and improve coding workflow")
    parser.add_argument("--extra-question", action="append", default=[])
    parser.add_argument("--remove-branding", action="store_true", help="Reserved for a future premium edition")
    parser.add_argument("--non-interactive", action="store_true")
    args = parser.parse_args(argv)
    answers = {"title": args.title, "audience": args.audience, "topic": args.topic}
    if not args.non_interactive:
        print("AgentBroko PDF Playbook setup")
        answers["title"] = _ask("Guide title", args.title)
        answers["audience"] = _ask("Primary audience", args.audience)
        answers["topic"] = _ask("Core promise", args.topic)
        for question in args.extra_question:
            answers[question] = _ask(question)
    try:
        path = generate_playbook(Path(args.output), answers, remove_branding=args.remove_branding)
    except ValueError as exc:
        parser.error(str(exc))
    print(f"Created branded AgentBroko PDF: {path.resolve()}")
    return 0

if __name__ == "__main__": raise SystemExit(main())
