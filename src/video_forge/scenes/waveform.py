"""waveform — a centred statement over thin sine-wave line-art that pauses behind
the words. Reference: "Industry-leading transcription".

scene fields: text (single line), optional lines."""

import math

from ..easing import lerp
from ._common import drift, enter, new_canvas


def _wave_pts(cx0, cx1, cy, amp, period, phase, step=6):
    pts = []
    x = cx0
    while x <= cx1:
        y = cy + amp * math.sin(2 * math.pi * (x - cx0) / period + phase)
        pts.append((x, y))
        x += step
    return pts


def render(ctx):
    cv = new_canvas(ctx)
    W, H = cv.W, cv.H
    p, t = ctx.p, ctx.t
    text = ctx.scene.get("text") or " ".join(ctx.scene.get("lines", []))
    cy = H / 2 + drift(p)

    # No bg_wash here: the lozenge behind the text is filled with the flat
    # background colour, and would read as a visible patch over a washed bg.
    # The accent waves are this scene's colour instead.
    reveal = enter(p, 0.0, 0.5)
    waves = [(150, 360, 0.0, 0.90), (110, 250, 1.1, 0.60), (185, 470, 2.3, 0.42)]
    for amp, period, ph0, wa in waves:
        phase = ph0 + t * 0.7
        pts = _wave_pts(-40, W + 40, cy, amp * reveal, period, phase)
        cv.line(pts, cv.accent, width=2.0, alpha=wa * reveal)

    # mask a lozenge behind the text so the line "pauses" for the words
    tk = enter(p, 0.15, 0.4)
    size = cv.fit_size(text, "medium", 78, W - 520, min_size=40)
    tw = cv.measure(text, "medium", size)
    pad = 44
    cv.rrect(W / 2 - tw / 2 - pad, cy - size * 0.9, tw + pad * 2, size * 1.8,
             size * 0.9, fill=cv.pal["bg"], alpha=1.0)
    cv.text_center(W / 2, cy, text, "medium", size, cv.pal["ink"], alpha=tk)
    return cv.finish()
