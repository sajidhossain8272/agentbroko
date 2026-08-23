"""FrameCtx: the per-frame state handed to a scene renderer.

A scene renderer is `render(ctx) -> PIL.Image` (1920x1080 RGB). It reads ctx.p
(0..1 progress through the scene), ctx.t (seconds since scene start), ctx.act, and
ctx.scene (its own spec dict), and draws with a video_engine.draw.Canvas.
"""

from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class FrameCtx:
    theme: Any
    scene: Dict[str, Any]
    act: str
    p: float          # 0..1 progress through the scene
    t: float          # seconds since scene start
    dur: float        # scene duration in seconds
    index: int        # scene index
    total: int        # number of scenes
