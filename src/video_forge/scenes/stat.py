"""stat — one oversized figure with a caption; the number counts up on entry.

scene fields: value ("$175", "99.9%", "10x"), caption, optional sub."""

import re

from ..easing import ease_out, ramp
from ._common import color_for, drift, enter, new_canvas, rise_dy

_NUM = re.compile(r"^([^\d\-]*)(-?[\d,]*\.?\d+)(.*)$", re.S)


def _count(value, k):
    m = _NUM.match(value.strip())
    if not m:
        return value
    pre, num, suf = m.groups()
    raw = num.replace(",", "")
    try:
        target = float(raw)
    except ValueError:
        return value
    cur = target * ease_out(k)
    decimals = len(raw.split(".")[1]) if "." in raw else 0
    if decimals:
        body = f"{cur:,.{decimals}f}"
    else:
        body = f"{int(round(cur)):,}"
    if "," not in num:
        body = body.replace(",", "")
    return f"{pre}{body}{suf}"


def render(ctx):
    cv = new_canvas(ctx)
    W, H = cv.W, cv.H
    p = ctx.p
    value = str(ctx.scene.get("value", ""))
    caption = ctx.scene.get("caption", "")
    sub = ctx.scene.get("sub")
    color = color_for(cv, ctx.scene.get("color", "ink"))

    k = enter(p, 0.05, 0.45)
    cy = H / 2 + drift(p)
    size = cv.fit_size(value or "0", "black", 260, W - 360, min_size=90)
    shown = _count(value, ramp(p, 0.05, 0.7)) if value else value
    cv.text_center(W / 2, cy - 20 + rise_dy(k, 30), shown, "black", size, color, alpha=k)

    if caption:
        ca = ease_out(ramp(p, 0.25, 0.7))
        cv.text_center(W / 2, cy + size * 0.62, caption, "medium", 40,
                       cv.pal["ink"], alpha=ca)
    if sub:
        sa = ease_out(ramp(p, 0.35, 0.8))
        cv.text_center(W / 2, cy + size * 0.62 + 58, sub, "regular", 28,
                       cv.pal["muted"], alpha=sa)
    return cv.finish()
