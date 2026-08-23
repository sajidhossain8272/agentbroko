from __future__ import annotations

import pytest
from video_forge.spec import normalize, default_duration
from video_forge.scenes import REGISTRY
from video_forge.theme import Theme, hex_rgb
from video_forge.timeline import Timeline
from video_forge.generator import generate_offline_spec


def test_scene_registry():
    expected = ["cold_open", "statement", "pill_list", "message", "node_stack", "orbit", "waveform", "feature_grid", "stat", "split_compare", "cta", "logo_reveal"]
    for sc in expected:
        assert sc in REGISTRY, f"Scene type {sc} must be in REGISTRY"


def test_spec_normalization():
    raw_spec = {
        "scenes": [
            {"type": "cold_open", "glyph": "play"},
            {"type": "statement", "lines": ["Test line"]},
        ]
    }
    norm = normalize(raw_spec)
    assert norm["video"]["width"] == 1920
    assert norm["video"]["height"] == 1080
    assert norm["scenes"][0]["act"] == "light"
    assert norm["scenes"][1]["act"] == "dark"  # auto-alternated


def test_default_duration():
    sc = {"type": "pill_list", "items": ["A", "B", "C"]}
    dur = default_duration(sc)
    assert dur > 3.0


def test_theme_resolution():
    theme = Theme({"brand": {"accent": "#3B5BFF"}})
    pal_dark = theme.palette("dark")
    assert pal_dark["bg"] == (28, 28, 28)
    assert theme.accent == (59, 91, 255)


def test_offline_spec_generator():
    spec = generate_offline_spec("Build an ad for AgentBroko", "AgentBroko", accent="#00FFCC", seconds=30)
    assert spec["brand"]["name"] == "AgentBroko"
    assert spec["brand"]["accent"] == "#00FFCC"
    assert len(spec["scenes"]) >= 5
    norm = normalize(spec)
    assert len(norm["scenes"]) >= 5


def test_timeline_solver():
    raw_spec = {
        "video": {"crossfade": 0.4},
        "scenes": [
            {"type": "cold_open", "glyph": "play"},
            {"type": "statement", "lines": ["Test line"]},
            {"type": "cta", "lines": ["Start Now"]}
        ]
    }
    norm = normalize(raw_spec)
    durs = [3.0, 4.0, 5.0]
    tl = Timeline(norm, durations=durs)
    assert tl.total_seconds() > 10.0
    assert tl.scene_start(0) == 0.0
    assert tl.scene_start(1) == 2.6
