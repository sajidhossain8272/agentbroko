"""Built-in storytelling templates for Video Forge."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


TEMPLATE_DIR = Path(__file__).with_name("templates") / "stories_of_the_ummah"


def available_story_templates() -> list[str]:
    return sorted(path.stem for path in TEMPLATE_DIR.glob("*.json"))


def load_story_template(name: str) -> dict[str, Any]:
    """Load a bundled story template by its filename stem."""
    path = TEMPLATE_DIR / f"{name}.json"
    if path.parent != TEMPLATE_DIR or not path.exists():
        names = ", ".join(available_story_templates())
        raise ValueError(f"Unknown story template '{name}'. Available templates: {names}")
    return json.loads(path.read_text(encoding="utf-8"))


def validate_story_template(template: dict[str, Any]) -> list[str]:
    """Return actionable errors for a universal storytelling template."""
    errors: list[str] = []
    for field in ("name", "series", "title", "source", "video", "audio", "scenes"):
        if not template.get(field):
            errors.append(f"missing required field: {field}")
    video = template.get("video", {})
    for field in ("width", "height", "fps", "aspect"):
        if not video.get(field):
            errors.append(f"missing video field: {field}")
    audio = template.get("audio", {})
    for field in ("narration", "music", "mix"):
        if not audio.get(field):
            errors.append(f"missing audio field: {field}")
    if not isinstance(template.get("scenes"), list) or not template["scenes"]:
        errors.append("scenes must be a non-empty list")
    return errors