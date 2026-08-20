from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .errors import VideoForgeError


@dataclass(frozen=True)
class Clip:
    source: Path
    start: float = 0.0
    duration: float | None = None
    speed: float = 1.0
    volume: float = 1.0
    transition: str = "none"
    transition_duration: float = 0.5


@dataclass(frozen=True)
class Project:
    path: Path
    output: Path
    width: int
    height: int
    fps: int
    clips: list[Clip]
    narration: Path | None
    music: Path | None
    music_volume: float
    subtitles: Path | None
    title: str | None


def _resolve(base: Path, value: str | None) -> Path | None:
    if not value:
        return None
    path = Path(value).expanduser()
    return path if path.is_absolute() else (base / path).resolve()


def load_project(path: Path) -> Project:
    try:
        data: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise VideoForgeError(f"Cannot read project file {path}: {exc}") from exc

    base = path.resolve().parent
    video = data.get("video", {})
    audio = data.get("audio", {})
    raw_clips = data.get("clips", [])
    if not raw_clips:
        raise VideoForgeError("Project must contain at least one clip.")

    clips: list[Clip] = []
    for index, raw in enumerate(raw_clips, 1):
        source = _resolve(base, raw.get("source"))
        if source is None:
            raise VideoForgeError(f"Clip {index} has no source.")
        speed = float(raw.get("speed", 1.0))
        if not 0.5 <= speed <= 2.0:
            raise VideoForgeError(f"Clip {index} speed must be between 0.5 and 2.0.")
        clips.append(
            Clip(
                source=source,
                start=float(raw.get("start", 0)),
                duration=float(raw["duration"]) if raw.get("duration") is not None else None,
                speed=speed,
                volume=float(raw.get("volume", 1.0)),
                transition=raw.get("transition", "none"),
                transition_duration=float(raw.get("transition_duration", 0.5)),
            )
        )

    output = _resolve(base, data.get("output", "outputs/final.mp4"))
    assert output is not None
    return Project(
        path=path.resolve(),
        output=output,
        width=int(video.get("width", 1920)),
        height=int(video.get("height", 1080)),
        fps=int(video.get("fps", 30)),
        clips=clips,
        narration=_resolve(base, audio.get("narration")),
        music=_resolve(base, audio.get("music")),
        music_volume=float(audio.get("music_volume", 0.15)),
        subtitles=_resolve(base, data.get("subtitles")),
        title=data.get("title"),
    )


def validate_project(project: Project) -> list[str]:
    problems: list[str] = []
    for clip in project.clips:
        if not clip.source.exists():
            problems.append(f"Missing clip: {clip.source}")
    for label, path in (
        ("narration", project.narration),
        ("music", project.music),
        ("subtitles", project.subtitles),
    ):
        if path and not path.exists():
            problems.append(f"Missing {label}: {path}")
    if project.width <= 0 or project.height <= 0 or project.fps <= 0:
        problems.append("Video width, height, and fps must be positive.")
    return problems
