"""Theme: palette tokens, light/dark "acts", and font resolution.

The reference ad alternates warm off-white and near-black acts with a mostly
monochrome palette and one sparing accent. Fonts resolve to the best installed
grotesque; Segoe UI (full weight range) is the default on Windows. Installing
Inter would improve fidelity to the reference — drop it in and it's picked first.
"""

import colorsys
import os

from PIL import ImageFont

FONT_DIR = os.environ.get("WINDIR", r"C:\Windows") + r"\Fonts"

# Preference-ordered filenames per weight. First existing wins.
_WEIGHTS = {
    "light":    ["Inter-Light.ttf", "segoeuil.ttf", "arial.ttf"],
    "regular":  ["Inter-Regular.ttf", "segoeui.ttf", "arial.ttf"],
    "medium":   ["Inter-Medium.ttf", "seguisb.ttf", "segoeui.ttf", "arial.ttf"],
    "semibold": ["Inter-SemiBold.ttf", "seguisb.ttf", "segoeuib.ttf", "arialbd.ttf"],
    "bold":     ["Inter-Bold.ttf", "segoeuib.ttf", "arialbd.ttf"],
    "black":    ["Inter-Black.ttf", "seguibl.ttf", "segoeuib.ttf", "arialbd.ttf"],
    # icon glyphs (phone, send, etc.) — Segoe MDL2 / Fluent icon sets
    "icon":     ["segmdl2.ttf", "SegoeIcons.ttf", "segoeuisymbol.ttf", "seguisym.ttf"],
}

# Warm off-white act.
LIGHT = dict(
    bg=(242, 241, 238),
    ink=(20, 20, 20),
    muted=(110, 110, 108),
    faint=(176, 174, 170),
    hair=(20, 20, 20, 40),
    card=(255, 255, 255),
    card2=(233, 232, 228),
    stroke=(20, 20, 20, 46),
    shadow=(0, 0, 0, 26),
)

# Near-black act.
DARK = dict(
    bg=(28, 28, 28),
    ink=(240, 240, 237),
    muted=(150, 150, 148),
    faint=(86, 86, 84),
    hair=(255, 255, 255, 36),
    card=(255, 255, 255),
    card2=(40, 40, 40),
    stroke=(255, 255, 255, 40),
    shadow=(0, 0, 0, 110),
)


def mix_rgb(a, b, t):
    """Linear blend of two RGB triples; t=0 -> a, t=1 -> b."""
    t = max(0.0, min(1.0, t))
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def shift(color, dl=0.0, ds=0.0, dh=0.0):
    """Nudge a colour in HLS space (lightness / saturation / hue deltas)."""
    r, g, b = [c / 255.0 for c in color[:3]]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    h = (h + dh) % 1.0
    l = min(1.0, max(0.0, l + dl))
    s = min(1.0, max(0.0, s + ds))
    rr, gg, bb = colorsys.hls_to_rgb(h, l, s)
    return (int(round(rr * 255)), int(round(gg * 255)), int(round(bb * 255)))


def accent_family(accent, n, spread=0.055):
    """`n` analogous variants of the accent — colour that still reads on-brand.

    Hue fans symmetrically around the accent and lightness alternates slightly, so
    adjacent elements separate without the set turning into a rainbow.
    """
    if n <= 1:
        return [tuple(accent[:3])]
    r, g, b = [c / 255.0 for c in accent[:3]]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    out = []
    for i in range(n):
        f = (i / (n - 1)) - 0.5                     # -0.5 .. 0.5
        hh = (h + f * 2.0 * spread) % 1.0
        ll = min(0.90, max(0.20, l + (0.05 if i % 2 else -0.05)))
        rr, gg, bb = colorsys.hls_to_rgb(hh, ll, s)
        out.append((int(round(rr * 255)), int(round(gg * 255)), int(round(bb * 255))))
    return out


def hex_rgb(s, default=(59, 91, 255)):
    if not s:
        return default
    s = s.strip().lstrip("#")
    if len(s) == 3:
        s = "".join(c * 2 for c in s)
    try:
        return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))
    except (ValueError, IndexError):
        return default


class Theme:
    def __init__(self, spec):
        v = spec.get("video", {})
        self.W = int(v.get("width", 1920))
        self.H = int(v.get("height", 1080))
        self.fps = int(v.get("fps", 30))
        self.ss = float(v.get("supersample", 1.5))

        b = spec.get("brand", {})
        self.brand = b
        self.accent = hex_rgb(b.get("accent"))
        self.font_override = b.get("font")  # optional explicit .ttf path for all weights

        self._font_paths = {}
        self._font_cache = {}

    # -- palette -----------------------------------------------------------
    def palette(self, act):
        return dict(DARK if act == "dark" else LIGHT)

    def ink(self, act):
        return self.palette(act)["ink"]

    # -- fonts -------------------------------------------------------------
    def _resolve_path(self, weight):
        if self.font_override and weight != "icon" and os.path.exists(self.font_override):
            return self.font_override
        if weight in self._font_paths:
            return self._font_paths[weight]
        for name in _WEIGHTS.get(weight, _WEIGHTS["regular"]):
            p = name if os.path.isabs(name) else os.path.join(FONT_DIR, name)
            if os.path.exists(p):
                self._font_paths[weight] = p
                return p
        # last resort: whatever regular resolves to, else PIL default
        fallback = os.path.join(FONT_DIR, "arial.ttf")
        self._font_paths[weight] = fallback
        return fallback

    def font(self, weight, px):
        px = max(1, int(round(px)))
        key = (weight, px)
        f = self._font_cache.get(key)
        if f is None:
            try:
                f = ImageFont.truetype(self._resolve_path(weight), px)
            except OSError:
                f = ImageFont.load_default()
            self._font_cache[key] = f
        return f
