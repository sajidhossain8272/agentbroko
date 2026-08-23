"""feature_grid — a set of labelled cards laid out in a responsive grid, each with
a numbered accent badge over a soft accent-tinted surface. Good for "what you get"
beats, and for pipelines where the numbering implies order.

scene fields: items: ["Title" | {"title":.., "desc":..}], optional columns (int).
"""

from ..theme import accent_family
from ._common import (bg_wash, enter, is_portrait, new_canvas, rise_dy,
                      side_margin)


def _grid(n, forced=None):
    if forced:
        return forced
    if n <= 3:
        return n
    if n == 4:
        return 2
    return 3


def _on(color):
    """Ink that stays legible on a filled accent chip."""
    lum = (0.299 * color[0] + 0.587 * color[1] + 0.114 * color[2]) / 255.0
    return (20, 20, 20) if lum > 0.62 else (255, 255, 255)


def render(ctx):
    cv = new_canvas(ctx)
    W, H = cv.W, cv.H
    p = ctx.p
    bg_wash(cv, p)

    items = ctx.scene.get("items") or []
    n = max(1, len(items))
    cols = _grid(n, ctx.scene.get("columns"))
    rows = (n + cols - 1) // cols

    gap = 30.0
    margin = side_margin(cv)
    cw = (W - margin * 2 - gap * (cols - 1)) / cols
    # Portrait frames have height to spare: let the cards breathe rather than
    # float as small squares in a tall, empty frame.
    portrait = is_portrait(cv)
    cap = 420.0 if portrait else 300.0
    avail_h = H * (0.56 if portrait else 0.72)
    ch = max(150.0, min(cap, (avail_h - gap * (rows - 1)) / rows))
    grid_w = cw * cols + gap * (cols - 1)
    grid_h = ch * rows + gap * (rows - 1)
    x0 = (W - grid_w) / 2
    y0 = (H - grid_h) / 2

    fam = accent_family(cv.accent, n)

    for i, it in enumerate(items):
        if isinstance(it, dict):
            title = str(it.get("title", ""))
            desc = it.get("desc")
        else:
            title, desc = str(it), None
        r, c = divmod(i, cols)
        k = enter(p, 0.05 + i * (0.5 / n), 0.42)
        if k <= 0.003:
            continue
        acc = fam[i]
        x = x0 + c * (cw + gap)
        y = y0 + r * (ch + gap) + rise_dy(k, 24)

        cv.card(x, y, cw, ch, r=20, alpha=k)
        cv.grad_rrect(x, y, cw, ch, 20,
                      cv.tint(acc, 0.28), cv.tint(acc, 0.04), alpha=k)

        # numbered accent chip — a solid block of colour, and an order cue
        br = min(38.0, ch * 0.11)
        bcy = y + ch * 0.30
        cv.ellipse(x + cw / 2, bcy, br, fill=acc, alpha=k)
        cv.text_center(x + cw / 2, bcy + 1, f"{i + 1:02d}", "semibold",
                       br * 0.86, _on(acc), alpha=k)

        tsize = cv.fit_size(title, "semibold", 40, cw - 68, min_size=24)
        ty = y + ch * 0.62
        cv.text_center(x + cw / 2, ty, title, "semibold", tsize,
                       (24, 24, 24), alpha=k)
        if desc:
            dsize = cv.fit_size(desc, "regular", 24, cw - 68, min_size=17)
            cv.text_center(x + cw / 2, ty + tsize * 0.92, desc, "regular",
                           dsize, (110, 110, 108), alpha=k)
    return cv.finish()
