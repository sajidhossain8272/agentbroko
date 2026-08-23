from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

from . import __version__
from .captions import text_to_srt
from .errors import VideoForgeError
from .project import load_project, validate_project
from .render import render_project
from .tts import available_engines, synthesize
from ._ffmpeg import ffmpeg_bin, ffprobe_bin

# Starter procedural spec template
STARTER_PROCEDURAL = {
    "brand": {
        "name": "MyProduct",
        "accent": "#3B5BFF",
        "url": "https://myproduct.app"
    },
    "video": {
        "width": 1920,
        "height": 1080,
        "fps": 30,
        "target_seconds": 30,
        "supersample": 1.5
    },
    "voice": {
        "backend": "edge",
        "voice": "en-US-ChristopherNeural",
        "rate": 0
    },
    "music": {
        "file": None,
        "gain_db": -19.0,
        "duck_db": -11.0
    },
    "scenes": [
        {
            "type": "cold_open",
            "act": "light",
            "glyph": "play",
            "label": "INTRODUCING",
            "vo": "Introducing MyProduct. Fast, reliable, and built for autonomous execution."
        },
        {
            "type": "statement",
            "act": "dark",
            "kicker": "THE ADVANTAGE",
            "lines": [
                {"text": "Production quality without limits.", "color": "ink"},
                {"text": "Render 10x faster locally.", "color": "accent"}
            ],
            "vo": "Experience extreme performance and broadcast visuals straight from your machine."
        },
        {
            "type": "pill_list",
            "act": "light",
            "items": ["100% Local-First", "High Retention", "Kinetic Motion", "Zero Cloud APIs"],
            "vo": "Engineered with four core principles: local execution, raw performance, open architecture, and instant delivery."
        },
        {
            "type": "cta",
            "act": "dark",
            "lines": [
                {"text": "Get Started Today", "color": "ink"},
                {"text": "Free and Open Source", "color": "accent"}
            ],
            "button": "Download Now",
            "url": "myproduct.app",
            "vo": "Get started today and bring your ideas to life with AgentBroko Video Forge."
        },
        {
            "type": "logo_reveal",
            "act": "light",
            "wordmark": "MyProduct",
            "url": "https://myproduct.app",
            "mark": "play",
            "vo": "MyProduct. Built for creators and autonomous agents."
        }
    ]
}

STARTER_CLIPS = {
    "output": "outputs/final.mp4",
    "title": "My Video",
    "video": {"width": 1920, "height": 1080, "fps": 30},
    "clips": [{"source": "media/clip-01.mp4", "start": 0, "duration": 5, "speed": 1, "volume": 1}],
    "audio": {"narration": "audio/narration.wav", "music": None, "music_volume": 0.12},
    "subtitles": "captions/subtitles.srt",
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="video-forge",
        description="AgentBroko Video Forge: 10/10 Procedural, Cinematic & Storytelling Video Engine for Humans and Coding Agents"
    )
    parser.add_argument("--version", action="version", version=f"video-forge {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    # 1. Doctor
    sub.add_parser("doctor", help="Check local tools, libraries, and speech engines")

    # 2. Init
    init = sub.add_parser("init", help="Create a starter project (procedural spec or clip timeline)")
    init.add_argument("directory", nargs="?", default="my-video")
    init.add_argument("--template", choices=["procedural", "ad", "short", "clips"], default="procedural",
                      help="Template type: procedural ad or classic clips")

    # 3. Generate (Brief -> spec -> video)
    gen = sub.add_parser("generate", help="Generate a finished video from a natural language brief")
    gen.add_argument("brief", help="Plain-English description of the video or product")
    gen.add_argument("--name", default="promo", help="Project output folder name")
    gen.add_argument("--accent", default=None, help="Hex brand accent color (e.g. #3B5BFF)")
    gen.add_argument("--url", default=None, help="Brand website URL")
    gen.add_argument("--seconds", type=int, default=30, help="Target duration in seconds")
    gen.add_argument("--scenes", type=int, default=7, help="Target scene count")
    gen.add_argument("--no-render", action="store_true", help="Generate spec.json only without rendering")
    gen.add_argument("--silent", action="store_true", help="Render without audio track")

    # 4. Render
    render = sub.add_parser("render", help="Render a spec.json or project.json video")
    render.add_argument("project", type=Path, help="Path to spec.json or project.json")
    render.add_argument("--silent", action="store_true", help="Render without audio (procedural specs)")
    render.add_argument("--keep-temp", action="store_true", help="Keep temporary frames (clip projects)")

    # 5. Short (Vertical 9:16 storytelling / reels / viral short generator)
    short = sub.add_parser("short", help="Generate a 9:16 vertical storytelling short or reel")
    short.add_argument("--type", choices=["story", "romantic", "tech"], default="story", help="Short template archetype")
    short.add_argument("--theme", choices=["golden", "sunset", "desert"], default="golden", help="Visual color palette")
    short.add_argument("--output", "-o", type=Path, default=Path("outputs/short_9x16.mp4"), help="Target MP4 file")
    short.add_argument("--fps", type=int, default=30, help="FPS (30 or 60)")

    # 6. Validate
    validate = sub.add_parser("validate", help="Validate a project or spec without rendering")
    validate.add_argument("project", type=Path)

    # 7. Speak
    speak = sub.add_parser("speak", help="Generate high-fidelity speech using neural or local offline engines")
    source = speak.add_mutually_exclusive_group(required=True)
    source.add_argument("--text")
    source.add_argument("--file", type=Path)
    speak.add_argument("--output", "-o", type=Path, default=Path("narration.wav"))
    speak.add_argument("--engine", choices=["auto", "edge", "windows", "say", "espeak", "piper", "elevenlabs", "openai"], default="auto")
    speak.add_argument("--voice", type=str, default="en-US-ChristopherNeural", help="Voice model or neural voice identifier")
    speak.add_argument("--rate", type=int, default=0, help="Rate adjustment percentage (-50 to +50)")

    # 8. Captions
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
        # 1. Doctor command
        if args.command == "doctor":
            print("Video Forge System Diagnostics:")
            ffmpeg = ffmpeg_bin()
            ffprobe = ffprobe_bin()
            print(f"  • FFmpeg:  {'✓ ' + ffmpeg if shutil.which(ffmpeg) or os.path.exists(ffmpeg) else '✗ missing (run: winget install Gyan.FFmpeg or brew install ffmpeg)'}")
            print(f"  • FFprobe: {'✓ ' + ffprobe if shutil.which(ffprobe) or os.path.exists(ffprobe) else '✗ missing'}")
            
            try:
                import PIL
                print(f"  • Pillow (PIL): ✓ found (v{PIL.__version__})")
            except ImportError:
                print("  • Pillow (PIL): ✗ missing (run: pip install Pillow)")

            try:
                import numpy
                print(f"  • NumPy:        ✓ found (v{numpy.__version__})")
            except ImportError:
                print("  • NumPy:        ✗ missing (run: pip install numpy)")

            try:
                import edge_tts
                print("  • Neural TTS:   ✓ edge-tts found")
            except ImportError:
                print("  • Neural TTS:   ○ edge-tts optional (install with: pip install edge-tts)")

            engines = available_engines()
            print("  • Offline TTS: ", ", ".join(engines) if engines else "none found")
            return 0

        # 2. Init command
        if args.command == "init":
            root = Path(args.directory)
            root.mkdir(parents=True, exist_ok=True)
            if args.template in ("procedural", "ad"):
                (root / "spec.json").write_text(json.dumps(STARTER_PROCEDURAL, indent=2) + "\n", encoding="utf-8")
                print(f"✓ Created procedural video project at: {root.resolve()}")
                print(f"  Run 'video-forge render {root}/spec.json' to build master MP4.")
            else:
                for child in ("media", "audio", "captions", "outputs"):
                    (root / child).mkdir(parents=True, exist_ok=True)
                (root / "project.json").write_text(json.dumps(STARTER_CLIPS, indent=2) + "\n", encoding="utf-8")
                (root / "script.txt").write_text("Write your narration here.\n", encoding="utf-8")
                print(f"✓ Created clip-timeline video project at: {root.resolve()}")
            return 0

        # 3. Generate command (Brief -> spec -> video)
        if args.command == "generate":
            from .generator import generate_spec_from_brief
            from .build import build as build_procedural

            out_dir = Path("ads") / args.name
            out_dir.mkdir(parents=True, exist_ok=True)
            spec_path = out_dir / "spec.json"

            print(f"[video-forge] Synthesizing video spec for: '{args.brief}'...")
            spec = generate_spec_from_brief(
                brief=args.brief,
                name=args.name,
                accent=args.accent,
                url=args.url,
                seconds=args.seconds,
                scenes=args.scenes,
            )
            spec_path.write_text(json.dumps(spec, indent=2) + "\n", encoding="utf-8")
            print(f"[video-forge] Saved spec to: {spec_path.resolve()}")

            if args.no_render:
                return 0

            print("[video-forge] Rendering procedural video...")
            final_mp4 = build_procedural(str(spec_path), silent=args.silent)
            print(f"✓ Successfully rendered video: {final_mp4}")
            return 0

        # 4. Render command
        if args.command == "render":
            p = Path(args.project)
            if not p.exists():
                raise FileNotFoundError(f"Project file not found: {p}")

            # Check if it's a procedural spec or classic project
            with open(p, "r", encoding="utf-8") as fh:
                data = json.load(fh)

            if "scenes" in data:
                from .build import build as build_procedural
                print(f"[video-forge] Detected procedural scene spec ({len(data['scenes'])} scenes). Rendering with 10/10 engine...")
                final_mp4 = build_procedural(str(p), silent=args.silent)
                print(f"✓ Rendered: {final_mp4}")
            else:
                print(f"[video-forge] Detected clip timeline project. Rendering...")
                final_mp4 = render_project(load_project(p), keep_temp=args.keep_temp)
                print(f"✓ Rendered: {final_mp4}")
            return 0

        # 5. Short command (Vertical 9:16)
        if args.command == "short":
            from .shorts.story_engine import render_vertical_story
            sample_story_scenes = [
                {
                    "duration": 4.0,
                    "pose": "walk_rear",
                    "text": "Three men were walking across the desert as the storm approached.",
                    "vo": "Three men were walking across the desert as the storm approached."
                },
                {
                    "duration": 4.5,
                    "pose": "push_rock",
                    "text": "A massive falling rock sealed them inside a dark cave.",
                    "vo": "A massive falling rock sealed them inside a dark cave."
                },
                {
                    "duration": 4.5,
                    "pose": "dua_kneel",
                    "text": "They called upon their Creator with their most sincere righteous deeds.",
                    "vo": "They called upon their Creator with their most sincere righteous deeds."
                },
                {
                    "duration": 4.0,
                    "pose": "walk_rear",
                    "text": "With every supplication, the stone moved until they walked out into the light.",
                    "vo": "With every supplication, the stone moved until they walked out into the light."
                }
            ]
            print(f"[video-forge] Rendering 9:16 vertical storytelling short ({args.fps} FPS, {args.theme} theme)...")
            out_file = str(Path(args.output).resolve())
            render_vertical_story(
                scenes=sample_story_scenes,
                output_path=out_file,
                fps=args.fps,
                theme=args.theme,
                include_particles=True,
                mastering=True
            )
            print(f"✓ Rendered vertical short: {out_file}")
            return 0

        # 6. Validate command
        if args.command == "validate":
            p = Path(args.project)
            with open(p, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            if "scenes" in data:
                from .spec import normalize
                normalize(data)
                print("✓ Procedural spec is valid.")
            else:
                problems = validate_project(load_project(p))
                if problems:
                    print("\n".join(f"ERROR: {item}" for item in problems))
                    return 1
                print("✓ Clip project is valid.")
            return 0

        # 7. Speak command
        if args.command == "speak":
            text = _read_text(args)
            if args.engine in ("edge", "auto"):
                try:
                    from .audio import _tts_edge
                    out = _tts_edge(text, str(args.output), voice=args.voice, rate=args.rate)
                    print(f"✓ Synthesized high-fidelity neural voice audio to: {args.output} (edge-tts)")
                    return 0
                except Exception as exc:
                    print(f"[video-forge] Neural TTS failed ({exc}), falling back to local system TTS.", file=sys.stderr)

            engine = synthesize(text, args.output, engine=args.engine, voice=Path(args.voice) if os.path.exists(args.voice) else None, rate=175)
            print(f"✓ Created {args.output} with {engine}")
            return 0

        # 8. Captions command
        if args.command == "captions":
            text_to_srt(_read_text(args), args.output, words_per_caption=args.words, seconds_per_caption=args.seconds)
            print(f"✓ Created {args.output}")
            return 0

        return 0
    except (VideoForgeError, OSError, ValueError, RuntimeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
