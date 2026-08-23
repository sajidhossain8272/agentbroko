"""render_video: pipe a Timeline's frames into ffmpeg as a silent H.264 mp4.

Frames are produced at full 1920x1080 (the Canvas already supersamples and
downscales internally), written as raw rgb24 to ffmpeg's stdin, and encoded with
libx264 / yuv420p / CRF for a clean, widely-compatible file.
"""

import subprocess
import sys

from ._ffmpeg import ffmpeg_bin


def render_silent(timeline, out_path, crf=18, preset="medium", progress=True):
    """Render `timeline` to a silent mp4 at `out_path`. Returns out_path."""
    W, H = timeline.theme.W, timeline.theme.H
    fps = timeline.fps
    n = timeline.frame_count()
    cmd = [
        ffmpeg_bin(), "-hide_banner", "-loglevel", "error", "-y",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(fps),
        "-i", "-",
        "-an",
        "-c:v", "libx264", "-preset", preset, "-crf", str(crf),
        "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        out_path,
    ]
    if progress:
        print(f"Rendering {n} frames ({timeline.total_seconds():.1f}s @ {fps}fps)"
              f" -> {out_path}", flush=True)
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    try:
        for i in range(n):
            img = timeline.frame_at(i / fps)
            if img.mode != "RGB":
                img = img.convert("RGB")
            proc.stdin.write(img.tobytes())
            if progress and i % 60 == 0:
                pct = 100.0 * i / n
                print(f"  {i:4d}/{n}  {pct:5.1f}%", flush=True)
    finally:
        proc.stdin.close()
    rc = proc.wait()
    if rc != 0:
        print(f"ffmpeg exited {rc}", file=sys.stderr)
        raise SystemExit(rc)
    if progress:
        print("Done:", out_path, flush=True)
    return out_path
