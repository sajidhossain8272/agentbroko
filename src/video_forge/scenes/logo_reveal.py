"""logo_reveal — centred wordmark + URL, the closing lockup. Reference t052.

scene fields: wordmark (else brand.name), url (else brand.url), mark ("pause"|None)."""

from ..easing import ease_out, lerp, ramp
from ._common import enter, new_canvas


def render(ctx):
    cv = new_canvas(ctx)
    W, H = cv.W, cv.H
    p = ctx.p
    b = ctx.theme.brand
    word = ctx.scene.get("wordmark") or b.get("wordmark") or b.get("name") or ""
    url = ctx.scene.get("url", b.get("url"))
    mark = ctx.scene.get("mark")
    ink = cv.pal["ink"]

    k = enter(p, 0.08, 0.5)
    sc = lerp(0.96, 1.0, k)
    size = int(96 * sc)
    size = cv.fit_size(word, "bold", size, W - 520, min_size=44)

    cx, cy = W / 2, H / 2
    tw = cv.measure(word, "bold", size)
    mark_w = 0.0
    if mark in ("pause", "bars"):
        mark_w = size * 0.62
    total = tw + mark_w
    x0 = cx - total / 2

    if mark in ("pause", "bars"):
        bw = size * 0.12
        bh = size * 0.82
        gap = bw * 0.9
        my = cy - bh / 2
        cv.rrect(x0, my, bw, bh, bw * 0.35, fill=ink, alpha=k)
        cv.rrect(x0 + bw + gap, my, bw, bh, bw * 0.35, fill=ink, alpha=k)

    cv.text(x0 + mark_w, cy, word, "bold", size, ink, anchor="lm", alpha=k)

    if url:
        ua = ease_out(ramp(p, 0.4, 0.85))
        cv.text_center(cx, H - 72, url, "regular", 26, cv.pal["muted"], alpha=ua)
    return cv.finish()
