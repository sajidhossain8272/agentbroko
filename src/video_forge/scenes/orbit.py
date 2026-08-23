"""orbit — a shaded central sphere ringed by concentric circles, with feature cards
placed around it. Reference: the "Natural turn-talking / Voice detection /
Interruption handling" beat.

scene fields: items: ["label", ...] (2-4 look best), optional center ("sphere"|"dot")."""

import math

import numpy as np
from PIL import Image

from ._common import bg_wash, enter, new_canvas, on_arc

_PRESETS = {
    1: [270],
    2: [205, 25],
    3: [210, 20, 110],
    4: [215, 335, 145, 60],
}


def _sphere(px_r, tint=None):
    d = max(2, px_r * 2)
    yy, xx = np.mgrid[0:d, 0:d].astype(np.float64)
    nx = (xx - px_r + 0.5) / px_r
    ny = (yy - px_r + 0.5) / px_r
    r2 = nx * nx + ny * ny
    mask = r2 <= 1.0
    nz = np.sqrt(np.clip(1 - r2, 0, 1))
    L = np.array([-0.52, -0.66, 0.54])
    L = L / np.linalg.norm(L)
    diff = np.clip(nx * L[0] + ny * L[1] + nz * L[2], 0, 1)
    val = 34 + diff ** 1.15 * 214            # dark bottom-left -> bright top-right
    rim = np.clip(1 - r2, 0, 1) ** 0.45
    val = val * (0.82 + 0.18 * rim)          # slight edge falloff
    val = np.clip(val, 0, 255).astype(np.uint8)
    a = (mask * 255).astype(np.uint8)
    if tint is None:
        return Image.fromarray(np.dstack([val, val, val, a]), "RGBA")
    # Ramp shadow -> tint -> highlight so the orb reads as a lit accent sphere
    # rather than a grey ball with a colour cast.
    v = val.astype(np.float64) / 255.0
    t = np.array(tint, dtype=np.float64)
    shadow = t * 0.16
    mid = 0.55
    low = v <= mid
    f = np.where(low, v / mid, (v - mid) / (1.0 - mid))[..., None]
    rgb = np.where(low[..., None],
                   shadow[None, None, :] + (t - shadow)[None, None, :] * f,
                   t[None, None, :] + (255.0 - t)[None, None, :] * f)
    rgb = np.clip(rgb, 0, 255).astype(np.uint8)
    return Image.fromarray(np.dstack([rgb, a]), "RGBA")


def _wrap2(cv, text, weight, size, max_w):
    if cv.measure(text, weight, size) <= max_w or " " not in text:
        return [text]
    words = text.split()
    best, bestdiff = None, 1e9
    for i in range(1, len(words)):
        a, b = " ".join(words[:i]), " ".join(words[i:])
        w = max(cv.measure(a, weight, size), cv.measure(b, weight, size))
        if w < bestdiff:
            best, bestdiff = (a, b), w
    return list(best)


def render(ctx):
    cv = new_canvas(ctx)
    W, H = cv.W, cv.H
    p = ctx.p
    items = ctx.scene.get("items") or []
    n = max(1, len(items))
    cx, cy = W / 2, H / 2 - 10
    bg_wash(cv, p, 0.8)

    ks = enter(p, 0.0, 0.45)
    # rings
    for rr in (206, 330):
        cv.ellipse(cx, cy, rr, rr, outline=cv.accent, width=1.6, alpha=0.42 * ks)
    # sphere
    if ctx.scene.get("center", "sphere") == "sphere":
        base_r = 122
        r = int(base_r * (0.9 + 0.1 * ks))
        cv.glow(cx, cy, r * 2.1, cv.accent, 0.28 * ks)
        sph = _sphere(cv.s(r), tint=cv.accent)
        if ks < 0.999:
            a = sph.getchannel("A").point(lambda v: int(v * ks))
            sph.putalpha(a)
        cv.img.paste(sph, (cv.s(cx) - sph.width // 2, cv.s(cy) - sph.height // 2), sph)
    else:
        cv.ellipse(cx, cy, 40, fill=cv.pal["ink"], alpha=ks)

    angles = _PRESETS.get(n, [i * 360 / n - 90 for i in range(n)])
    for i, label in enumerate(items):
        label = str(label)
        k = enter(p, 0.2 + i * 0.12, 0.4)
        if k <= 0.003:
            continue
        size = 36
        lines = _wrap2(cv, label, "medium", size, 300)
        tw = max(cv.measure(ln, "medium", size) for ln in lines)
        padx, lh = 40, size * 1.24
        bw = tw + padx * 2
        bh = lh * len(lines) + 40
        ax, ay = on_arc(cx, cy, 300, 232, angles[i % len(angles)])
        bx, by = ax - bw / 2, ay - bh / 2
        cv.card(bx, by, bw, bh, r=22, alpha=k, elevate=24)
        cv.grad_rrect(bx, by, bw, bh, 22, cv.tint(cv.accent, 0.24),
                      cv.tint(cv.accent, 0.04), alpha=k)
        ty = by + bh / 2 - (len(lines) - 1) * lh / 2
        for j, ln in enumerate(lines):
            cv.text_center(ax, ty + j * lh, ln, "medium", size, (24, 24, 24), alpha=k)
    return cv.finish()
