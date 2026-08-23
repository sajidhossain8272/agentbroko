"""build: orchestrate spec -> (VO durations) -> video -> (audio mix) -> mp4.

Phase 1 (silent proof render):
    py -m video_engine.build ads/demo/spec.json --silent

With audio (VO + music bed; falls back to silent if the audio stage is
unavailable or produces nothing):
    py -m video_engine.build ads/demo/spec.json
"""

import argparse
import os
import shutil
import sys

from .render_video import render_silent
from .spec import load_spec
from .timeline import Timeline


def _out_dir(spec_path):
    d = os.path.dirname(os.path.abspath(spec_path))
    os.makedirs(d, exist_ok=True)
    return d


def build(spec_path, silent=False, out=None, crf=18, preset="medium"):
    spec = load_spec(spec_path)
    out_dir = _out_dir(spec_path)

    if silent:
        timeline = Timeline(spec)
        target = out or os.path.join(out_dir, "video.mp4")
        return render_silent(timeline, target, crf=crf, preset=preset)

    # --- audio path (Phase 2) --------------------------------------------
    audio = None
    try:
        from . import audio as audio  # noqa: PLC0414
    except ImportError:
        print("[build] audio stage unavailable -> rendering silent.",
              file=sys.stderr)

    vo = None
    durations = None
    if audio is not None:
        try:
            vo = audio.synth_vo(spec, out_dir)
            durations = audio.scene_durations(spec, vo)
        except Exception as e:  # TTS/env problem: keep the video, drop timing
            print(f"[build] VO synthesis failed ({e}) -> default timing.",
                  file=sys.stderr)
            vo = None

    timeline = Timeline(spec, durations=durations)
    target = out or os.path.join(out_dir, "final.mp4")
    silent_path = os.path.join(out_dir, "_video_silent.mp4")
    render_silent(timeline, silent_path, crf=crf, preset=preset)

    mixed = None
    if audio is not None:
        try:
            mixed = audio.build_mix(spec, out_dir, timeline, vo)
        except Exception as e:
            print(f"[build] audio mix failed ({e}) -> silent output.",
                  file=sys.stderr)

    if mixed:
        audio.mux(silent_path, mixed, target)
        try:
            os.remove(silent_path)
        except OSError:
            pass
    else:
        shutil.move(silent_path, target)
    return target


def main(argv=None):
    ap = argparse.ArgumentParser(description="Render an ad spec to mp4.")
    ap.add_argument("spec", help="path to spec.json")
    ap.add_argument("--silent", action="store_true",
                    help="render video only (no TTS / music)")
    ap.add_argument("--out", default=None, help="output mp4 path")
    ap.add_argument("--crf", type=int, default=18, help="x264 CRF (lower=better)")
    ap.add_argument("--preset", default="medium", help="x264 preset")
    args = ap.parse_args(argv)
    path = build(args.spec, silent=args.silent, out=args.out,
                 crf=args.crf, preset=args.preset)
    print(path)


if __name__ == "__main__":
    main()
