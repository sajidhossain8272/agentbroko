"""Shared helpers for scene renderers: entrance easing, colour lookup, geometry."""

import math

from ..draw import Canvas
from ..easing import clamp, ease_out, lerp, ramp, smoothstep
from ..theme import accent_family, mix_rgb, shift


def new_canvas(ctx):
    return Canvas(ctx.theme, ctx.act)


def is_portrait(cv):
    return cv.H > cv.W


def side_margin(cv):
    """Comfortable horizontal margin in design units, proportional to the canvas.

    Absolute margins tuned for 1920x1080 eat most of a 1080-wide portrait frame,
    so every scene that lays out columns or grids derives its margin from here.
    """
    return round(cv.W * (0.075 if is_portrait(cv) else 0.125))


def content_w(cv):
    return cv.W - 2 * side_margin(cv)


def bg_wash(cv, p, strength=1.0):
    """Two slow accent blooms behind the content — colour in the empty space.

    Placement comes from the aspect ratio so portrait renders get bloom in their
    tall dead zones rather than only behind the content block. Drawn before any
    content, so it reads as lit background rather than an overlay.
    """
    W, H = cv.W, cv.H
    a = (0.17 if cv.act == "light" else 0.24) * strength
    r = max(W, H) * 0.40
    dy = drift(p, 26)
    warm = shift(cv.accent, dh=0.085, ds=0.04)
    if is_portrait(cv):
        cv.glow(W * 0.15, H * 0.19 + dy, r, cv.accent, a)
        cv.glow(W * 0.89, H * 0.79 + dy, r * 0.94, warm, a * 0.85)
    else:
        cv.glow(W * 0.12, H * 0.21 + dy, r * 0.86, cv.accent, a)
        cv.glow(W * 0.90, H * 0.83 + dy, r * 0.82, warm, a * 0.85)


def enter(p, start=0.10, span=0.42):
    """Standard element entrance: 0 -> 1 with an ease-out settle."""
    return ease_out(ramp(p, start, start + span))


def drift(p, amount=8.0):
    """Slow upward parallax drift across the whole scene (in design units)."""
    return -amount * smoothstep(p)


def rise_dy(k, dist=34.0):
    """Vertical offset for an entering element (k in 0..1)."""
    return (1.0 - k) * dist


def parse_line(line):
    if isinstance(line, dict):
        return str(line.get("text", "")), line.get("color", "ink")
    return str(line), "ink"


def color_for(cv, name):
    if name == "accent":
        return cv.accent
    if name == "muted":
        return cv.pal["muted"]
    if name == "faint":
        return cv.pal["faint"]
    if name == "bg":
        return cv.pal["bg"]
    if name == "card2":
        return cv.pal["card2"]
    return cv.pal["ink"]


def on_arc(cx, cy, rx, ry, deg):
    a = math.radians(deg)
    return cx + rx * math.cos(a), cy + ry * math.sin(a)


def wrap_lines(cv, text, weight, size, max_w):
    """Greedy word wrap to a max width (design units). Returns a list of lines."""
    words = str(text).split()
    if not words:
        return [""]
    lines, cur = [], words[0]
    for w in words[1:]:
        trial = cur + " " + w
        if cv.measure(trial, weight, size) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines
