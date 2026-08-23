"""split_compare — two figures side by side across a hairline divider, e.g.
"$175 -> $0". Reference: the money transition.

scene fields: left/right = {"label":.., "value":.., "color":"ink|accent|muted"},
optional arrow (bool)."""

from ..easing import ease_out, ramp
from ._common import color_for, enter, new_canvas, rise_dy


def _side(cv, cx, side, k, W):
    label = side.get("label", "")
    value = str(side.get("value", ""))
    col = color_for(cv, side.get("color", "ink"))
    cy = cv.H / 2
    if label:
        cv.text_center(cx, cy - 92, label.upper(), "semibold", 24,
                       cv.pal["muted"], tracking=5, alpha=k)
    size = cv.fit_size(value or "0", "black", 150, W / 2 - 220, min_size=70)
    cv.text_center(cx, cy + 6 + rise_dy(k, 28), value, "black", size, col, alpha=k)


def render(ctx):
    cv = new_canvas(ctx)
    W, H = cv.W, cv.H
    p = ctx.p
    left = ctx.scene.get("left", {})
    right = ctx.scene.get("right", {})

    kd = enter(p, 0.05, 0.4)
    cv.line([(W / 2, H / 2 - 120), (W / 2, H / 2 + 120)], cv.pal["hair"],
            width=2, alpha=kd)

    kl = enter(p, 0.05, 0.42)
    kr = enter(p, 0.22, 0.42)
    _side(cv, W * 0.29, left, kl, W)
    _side(cv, W * 0.71, right, kr, W)

    if ctx.scene.get("arrow", True):
        ka = ease_out(ramp(p, 0.45, 0.8))
        cv.text_center(W / 2, H / 2 + 2, "→", "regular", 72,
                       cv.pal["ink"], alpha=ka)
    return cv.finish()
