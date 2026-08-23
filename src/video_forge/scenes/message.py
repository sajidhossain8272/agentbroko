"""message — a chat bubble with a secondary "engine" card and a round call button.
Reference: the "I need to reschedule my delivery" beat.

scene fields: message (bubble text), label (secondary card label, e.g. product
name), toggle (bool), call (bool)."""

from ..easing import ease_out, lerp, ramp
from ._common import enter, new_canvas, wrap_lines

PHONE = chr(0xE717)   # Segoe MDL2 Assets — Phone
SEND = chr(0xE724)    # Segoe MDL2 Assets — Send


def render(ctx):
    cv = new_canvas(ctx)
    W, H = cv.W, cv.H
    p = ctx.p
    msg = ctx.scene.get("message", "")
    label = ctx.scene.get("label", ctx.theme.brand.get("name", ""))
    show_toggle = ctx.scene.get("toggle", True)
    show_call = ctx.scene.get("call", True)

    bubble_w = 720.0
    pad = 44.0
    size = 40
    lines = wrap_lines(cv, msg, "regular", size, bubble_w - pad * 2)
    lh = size * 1.32
    bubble_h = max(150.0, len(lines) * lh + pad * 2)
    cx = W / 2 - (60 if show_call else 0)
    by = H / 2 - bubble_h / 2 - 40

    # secondary "engine" card, slightly behind & below
    kc = enter(p, 0.18, 0.45)
    if label:
        sw, sh = bubble_w - 60, 96
        sx = cx - sw / 2
        sy = by + bubble_h - 28 + (1 - kc) * 20
        cv.card(sx, sy, sw, sh, r=22, fill=cv.pal["card2"], alpha=kc, elevate=18)
        cv.text(sx + 40, sy + sh / 2, label, "medium", 32, (24, 24, 24),
                anchor="lm", alpha=kc)
        if show_toggle:
            tw, th = 92, 46
            tx = sx + sw - 40 - tw
            ty = sy + sh / 2 - th / 2
            cv.pill(tx, ty, tw, th, fill=cv.accent, alpha=kc)
            kr = th - 10
            cv.ellipse(tx + tw - th / 2, ty + th / 2, kr / 2, fill=(255, 255, 255),
                       alpha=kc)

    # main bubble
    kb = enter(p, 0.05, 0.4)
    sc = lerp(0.97, 1.0, kb)
    bw2, bh2 = bubble_w * sc, bubble_h * sc
    bx2, by2 = cx - bw2 / 2, by - (bh2 - bubble_h) / 2
    cv.card(bx2, by2, bw2, bh2, r=30, fill=(255, 255, 255), alpha=kb, elevate=30)
    ty = by2 + pad + lh * 0.5
    for i, ln in enumerate(lines):
        cv.text(bx2 + pad, ty + i * lh, ln, "regular", size, (70, 70, 70),
                anchor="lm", alpha=kb)
    # small send glyph, bottom-right
    cv.text(bx2 + bw2 - 42, by2 + bh2 - 36, SEND, "icon", 24, (188, 188, 188),
            anchor="mm", alpha=kb)

    # round call button
    if show_call:
        ka = ease_out(ramp(p, 0.3, 0.7))
        r = 52
        bxc = cx + bubble_w / 2 + 20 + r
        byc = by + bubble_h / 2
        cv.drop_shadow(bxc - r, byc - r, 2 * r, 2 * r, r, spread=18,
                       alpha=0.18 * ka, dy=8)
        cv.ellipse(bxc, byc, r, fill=(255, 255, 255), alpha=ka)
        cv.text_center(bxc, byc, PHONE, "icon", 40, (20, 20, 20), alpha=ka)
    return cv.finish()
