"""statement — one to three big centred lines. The workhorse scene.

scene fields: lines: [ "text" | {"text":..., "color":"ink|accent|muted"} ],
optional kicker (small label above), weight (default "medium")."""

from ._common import (color_for, drift, enter, new_canvas, parse_line, rise_dy)


def render(ctx):
    cv = new_canvas(ctx)
    W, H = cv.W, cv.H
    p = ctx.p
    lines = ctx.scene.get("lines") or [ctx.scene.get("text", "")]
    weight = ctx.scene.get("weight", "medium")
    max_w = W - 360

    # Size to the widest line.
    size = 108
    for ln in lines:
        s, _ = parse_line(ln)
        size = min(size, cv.fit_size(s, weight, size, max_w, min_size=40))

    lh = size * 1.16
    kicker = ctx.scene.get("kicker")
    kicker_gap = 78 if kicker else 0
    block_h = lh * len(lines)
    top = (H - block_h) / 2 + lh / 2 + kicker_gap / 2 + drift(p)

    if kicker:
        ka = enter(p, 0.0, 0.4)
        cv.text_center(W / 2, top - block_h / 2 - kicker_gap, kicker.upper(),
                       "semibold", 26, cv.accent, tracking=6, alpha=ka)

    for i, ln in enumerate(lines):
        s, cname = parse_line(ln)
        k = enter(p, 0.10 + i * 0.10, 0.44)
        y = top + i * lh + rise_dy(k, 40)
        col = color_for(cv, cname)
        cv.text_center(W / 2, y, s, weight, size, col, alpha=k)
    return cv.finish()
