from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from . import __version__
from .captions import text_to_srt
from .errors import VideoForgeError
from .project import load_project, validate_project
from .render import render_project
from .tts import available_engines, synthesize


STARTER = {
    "output": "outputs/final.mp4",
    "title": "My Video",
    "video": {"width": 1920, "height": 1080, "fps": 30},
    "clips": [{"source": "media/clip-01.mp4", "start": 0, "duration": 5, "speed": 1, "volume": 1}],
    "audio": {"narration": "audio/narration.wav", "music": None, "music_volume": 0.12},
    "subtitles": "captions/subtitles.srt",
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="video-forge", description="Local-first video editing for humans and coding agents")
    parser.add_argument("--version", action="version", version=__version__)
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("doctor", help="Check local tools")
    init = sub.add_parser("init", help="Create a starter project")
    init.add_argument("directory", nargs="?", default="my-video")

    validate = sub.add_parser("validate", help="Validate a project without rendering")
    validate.add_argument("project", type=Path)

    render = sub.add_parser("render", help="Render a project")
    render.add_argument("project", type=Path)
    render.add_argument("--keep-temp", action="store_true")

    speak = sub.add_parser("speak", help="Generate speech using a local engine")
    source = speak.add_mutually_exclusive_group(required=True)
    source.add_argument("--text")
    source.add_argument("--file", type=Path)
    speak.add_argument("--output", "-o", type=Path, default=Path("narration.wav"))
    speak.add_argument("--engine", choices=["auto", "piper", "espeak", "windows", "say"], default="auto")
    speak.add_argument("--voice", type=Path, help="Piper .onnx voice model")
    speak.add_argument("--rate", type=int, default=175)

    captions = sub.add_parser("captions", help="Create evenly timed SRT captions from text")
    source = captions.add_mutually_exclusive_group(required=True)
    source.add_argument("--text")
    source.add_argument("--file", type=Path)
    captions.add_argument("--output", "-o", type=Path, default=Path("subtitles.srt"))
    captions.add_argument("--words", type=int, default=8)
    captions.add_argument("--seconds", type=float, default=3.0)
    return parser


def _read_text(args: argparse.Namespace) -> str:
    return args.text if args.text is not None else args.file.read_text(encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "doctor":
            print(f"FFmpeg: {'found' if shutil.which('ffmpeg') else 'missing'}")
            print(f"FFprobe: {'found' if shutil.which('ffprobe') else 'missing'}")
            engines = available_engines()
            print("Offline TTS:", ", ".join(engines) if engines else "none found")
            return 0 if shutil.which("ffmpeg") and shutil.which("ffprobe") else 1
        if args.command == "init":
            root = Path(args.directory)
            for child in ("media", "audio", "captions", "outputs"):
                (root / child).mkdir(parents=True, exist_ok=True)
            (root / "project.json").write_text(json.dumps(STARTER, indent=2) + "\n", encoding="utf-8")
            (root / "script.txt").write_text("Write your narration here.\n", encoding="utf-8")
            print(f"Created {root.resolve()}")
        elif args.command == "validate":
            problems = validate_project(load_project(args.project))
            if problems:
                print("\n".join(f"ERROR: {item}" for item in problems))
                return 1
            print("Project is valid.")
        elif args.command == "render":
            print(f"Rendered {render_project(load_project(args.project), keep_temp=args.keep_temp)}")
        elif args.command == "speak":
            engine = synthesize(_read_text(args), args.output, engine=args.engine, voice=args.voice, rate=args.rate)
            print(f"Created {args.output} with {engine}")
        elif args.command == "captions":
            text_to_srt(_read_text(args), args.output, words_per_caption=args.words, seconds_per_caption=args.seconds)
            print(f"Created {args.output}")
        return 0
    except (VideoForgeError, OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

