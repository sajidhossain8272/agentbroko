"""cold_open — a single minimal glyph, centred, easing in. The reference opens on
a lone pause bar on off-white."""

from ..easing import ease_out, lerp, ramp
from ._common import bg_wash, enter, new_canvas


def render(ctx):
    cv = new_canvas(ctx)
    W, H = cv.W, cv.H
    p = ctx.p
    bg_wash(cv, p, 0.85)
    ink = cv.pal["ink"]
    k = enter(p, 0.08, 0.5)
    a = k
    sc = lerp(0.84, 1.0, k)
    cx, cy = W / 2, H / 2
    glyph = ctx.scene.get("glyph", "pause")
    # The opening frame is a single mark: give it the accent and a bloom, so the
    # hook lands on colour rather than grey-on-grey.
    cv.glow(cx, cy, 200, cv.accent, 0.34 * k)
    mark = cv.accent

    if glyph in ("pause", "bars"):
        bw, bh, gap = 26 * sc, 104 * sc, 30 * sc
        cv.rrect(cx - gap / 2 - bw, cy - bh / 2, bw, bh, bw * 0.36, fill=mark, alpha=a)
        cv.rrect(cx + gap / 2, cy - bh / 2, bw, bh, bw * 0.36, fill=mark, alpha=a)
    elif glyph == "play":
        r = 60 * sc
        cv.d.polygon(
            [(cv.s(cx - r * 0.5), cv.s(cy - r)), (cv.s(cx - r * 0.5), cv.s(cy + r)),
             (cv.s(cx + r), cv.s(cy))],
            fill=cv._col(mark, a))
    elif glyph == "dot":
        cv.ellipse(cx, cy, 46 * sc, fill=mark, alpha=a)
    else:
        cv.text_center(cx, cy, glyph, "black", 120, ink, alpha=a)

    label = ctx.scene.get("label")
    if label:
        la = ease_out(ramp(p, 0.35, 0.8))
        cv.text_center(cx, cy + 130, label.upper(), "semibold", 24, cv.pal["muted"],
                       tracking=6, alpha=la)
    return cv.finish()
