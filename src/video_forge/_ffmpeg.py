"""Locate the ffmpeg / ffprobe binaries.

Prefers an explicit env var, then the winget install path used on this machine,
then whatever is on PATH. Shared by render_video (video) and audio (mux)."""

import os
import shutil

_WINGET = os.path.join(
    os.environ.get("LOCALAPPDATA", ""),
    "Microsoft", "WinGet", "Packages",
    "Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe",
    "ffmpeg-9.0-full_build", "bin",
)


def _find(name, env):
    p = os.environ.get(env)
    if p and os.path.exists(p):
        return p
    cand = os.path.join(_WINGET, name + ".exe")
    if os.path.exists(cand):
        return cand
    found = shutil.which(name)
    return found or name


def ffmpeg_bin():
    return _find("ffmpeg", "FFMPEG")


def ffprobe_bin():
    return _find("ffprobe", "FFPROBE")
