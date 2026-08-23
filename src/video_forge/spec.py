"""Spec loading, defaults, act alternation, and light validation.

A spec is plain JSON (see schema/spec.schema.json and ads/_template/spec.json).
This module fills defaults, auto-alternates light/dark acts where a scene omits
`act`, and estimates fallback scene durations for silent renders (when no VO
timing is available).
"""

import json

from .scenes import REGISTRY

DEFAULT_VIDEO = {"width": 1920, "height": 1080, "fps": 30,
                 "target_seconds": 60, "supersample": 1.5}
DEFAULT_VOICE = {"backend": "windows", "voice": "en-US", "rate": 0}
DEFAULT_MUSIC = {"file": None, "gain_db": -19.0, "duck_db": -11.0}
DEFAULT_BRAND = {"name": "Brand", "wordmark": None, "url": None,
                 "accent": "#3B5BFF", "font": None}

# Per-type base seconds + per-unit add-on, used only when VO timing is absent.
_DUR = {
    "cold_open":    (2.4, 0.0),
    "statement":    (3.4, 0.0),
    "pill_list":    (3.0, 0.55),
    "message":      (4.2, 0.0),
    "node_stack":   (4.6, 0.0),
    "orbit":        (4.4, 0.4),
    "waveform":     (3.6, 0.0),
    "feature_grid": (3.8, 0.35),
    "stat":         (3.2, 0.0),
    "split_compare": (4.0, 0.0),
    "cta":          (3.6, 0.0),
    "logo_reveal":  (3.4, 0.0),
    "screenshot":   (4.0, 0.0),
}


def _merge(base, override):
    out = dict(base)
    if override:
        for k, v in override.items():
            if v is not None:
                out[k] = v
    return out


def default_duration(scene):
    base, per = _DUR.get(scene.get("type"), (3.6, 0.0))
    n = len(scene.get("items", []) or [])
    return round(base + per * n, 3)


def normalize(spec):
    """Return a spec dict with defaults applied and scenes normalized in place."""
    spec = dict(spec)
    spec["video"] = _merge(DEFAULT_VIDEO, spec.get("video"))
    spec["voice"] = _merge(DEFAULT_VOICE, spec.get("voice"))
    spec["music"] = _merge(DEFAULT_MUSIC, spec.get("music"))
    spec["brand"] = _merge(DEFAULT_BRAND, spec.get("brand"))

    scenes = spec.get("scenes") or []
    if not scenes:
        raise ValueError("spec has no scenes")

    prev_act = None
    for i, sc in enumerate(scenes):
        t = sc.get("type")
        if t not in REGISTRY:
            raise ValueError(
                f"scene {i}: unknown type {t!r}. Known: {sorted(REGISTRY)}")
        act = sc.get("act")
        if act not in ("light", "dark"):
            # alternate; first scene defaults to light
            act = "light" if prev_act is None else (
                "dark" if prev_act == "light" else "light")
        sc["act"] = act
        prev_act = act
        sc.setdefault("vo", "")
    spec["scenes"] = scenes
    return spec


def load_spec(path):
    with open(path, "r", encoding="utf-8") as fh:
        return normalize(json.load(fh))
