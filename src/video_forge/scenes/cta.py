"""cta — closing call to action: headline lines + an accent button + URL.

scene fields: lines, button (label), url."""

from ..easing import ease_out, ramp
from ._common import color_for, drift, enter, new_canvas, parse_line, rise_dy


def render(ctx):
    cv = new_canvas(ctx)
    W, H = cv.W, cv.H
    p = ctx.p
    lines = ctx.scene.get("lines") or [ctx.scene.get("text", "")]
    button = ctx.scene.get("button")
    url = ctx.scene.get("url", ctx.theme.brand.get("url"))

    max_w = W - 360
    size = 96
    for ln in lines:
        s, _ = parse_line(ln)
        size = min(size, cv.fit_size(s, "medium", size, max_w, min_size=44))
    lh = size * 1.16
    has_btn = bool(button)
    block_h = lh * len(lines)
    top = (H - block_h) / 2 - (70 if has_btn else 0) + lh / 2 + drift(p)

    for i, ln in enumerate(lines):
        s, cname = parse_line(ln)
        k = enter(p, 0.08 + i * 0.1, 0.44)
        cv.text_center(W / 2, top + i * lh + rise_dy(k, 36), s, "medium", size,
                       color_for(cv, cname), alpha=k)

    by = top + block_h + 40
    if button:
        kb = ease_out(ramp(p, 0.35, 0.75))
        bsize = 34
        tw = cv.measure(button, "semibold", bsize)
        bw, bh = tw + 96, 84
        cv.pill(W / 2 - bw / 2, by, bw, bh, fill=cv.accent, alpha=kb)
        # accent buttons read on white text
        cv.text_center(W / 2, by + bh / 2, button, "semibold", bsize,
                       (255, 255, 255), alpha=kb)
        by += bh + 34
    if url:
        ku = ease_out(ramp(p, 0.5, 0.85))
        cv.text_center(W / 2, by + 14, url, "regular", 26, cv.pal["muted"], alpha=ku)
    return cv.finish()
