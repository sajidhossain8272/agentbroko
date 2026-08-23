from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def _need(command: str) -> str:
    path = shutil.which(command)
    if not path:
        raise RuntimeError(f"Missing '{command}'. Install Poppler or Python PDF tools.")
    return path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="agentbroko pdf", description="Local PDF utilities")
    sub = parser.add_subparsers(dest="command", required=True)
    info = sub.add_parser("info"); info.add_argument("pdf", type=Path)
    text = sub.add_parser("text"); text.add_argument("pdf", type=Path); text.add_argument("-o", "--output", type=Path)
    render = sub.add_parser("render"); render.add_argument("pdf", type=Path); render.add_argument("-o", "--output", type=Path, default=Path("pdf-pages")); render.add_argument("--dpi", type=int, default=150)
    args = parser.parse_args(argv)
    try:
        if args.command == "info":
            pdfinfo = _need("pdfinfo")
            subprocess.run([pdfinfo, str(args.pdf)], check=True)
        elif args.command == "render":
            pdftoppm = _need("pdftoppm")
            args.output.mkdir(parents=True, exist_ok=True)
            prefix = args.output / args.pdf.stem
            subprocess.run([pdftoppm, "-png", "-r", str(args.dpi), str(args.pdf), str(prefix)], check=True)
            print(f"Rendered pages to {args.output.resolve()}")
        elif args.command == "text":
            try:
                from pypdf import PdfReader
            except ImportError as exc:
                raise RuntimeError("Install pypdf with: python -m pip install pypdf") from exc
            content = "\n\n".join(page.extract_text() or "" for page in PdfReader(str(args.pdf)).pages)
            if args.output:
                args.output.write_text(content, encoding="utf-8")
                print(f"Wrote {args.output}")
            else:
                print(content)
        return 0
    except (OSError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
