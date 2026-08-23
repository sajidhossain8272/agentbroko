"""Scene registry: maps a spec scene `type` to its `render(ctx) -> Image` function.

Every renderer takes a video_engine.context.FrameCtx and returns a 1920x1080 RGB
PIL image for that frame. spec.normalize() validates scene types against this map,
and timeline/render_video dispatch through it.
"""

from . import (
    cold_open,
    cta,
    feature_grid,
    logo_reveal,
    message,
    node_stack,
    orbit,
    pill_list,
    screenshot,
    split_compare,
    stat,
    statement,
    waveform,
)

REGISTRY = {
    "cold_open":     cold_open.render,
    "statement":     statement.render,
    "pill_list":     pill_list.render,
    "message":       message.render,
    "node_stack":    node_stack.render,
    "orbit":         orbit.render,
    "waveform":      waveform.render,
    "feature_grid":  feature_grid.render,
    "stat":          stat.render,
    "split_compare": split_compare.render,
    "cta":           cta.render,
    "logo_reveal":   logo_reveal.render,
    "screenshot":    screenshot.render,
}
