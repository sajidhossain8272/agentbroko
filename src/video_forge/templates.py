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