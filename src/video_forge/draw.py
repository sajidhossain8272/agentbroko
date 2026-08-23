"""Canvas: supersampled 2D primitives for the scene library.

Scenes draw in *design units* (a 1920x1080 coordinate space). The canvas renders
internally at `theme.ss`x that resolution and downsamples with LANCZOS on finish(),
which gives clean anti-aliased type, hairlines and rounded corners. Colours may be
RGB or RGBA; an optional `alpha` (0..1) multiplies the alpha for element fades.
"""

from PIL import Image, ImageChops, ImageDraw, ImageFilter

from .easing import clamp


class Canvas:
    def __init__(self, theme, act):
        self.theme = theme
        self.act = act
        self.ss = theme.ss
        self.pal = theme.palette(act)
        self.accent = theme.accent
        self.W, self.H = theme.W, theme.H
        self.pw, self.ph = self.s(self.W), self.s(self.H)
        self.img = Image.new("RGB", (self.pw, self.ph), self.pal["bg"])
        self.d = ImageDraw.Draw(self.img, "RGBA")

    # -- scaling -----------------------------------------------------------
    def s(self, v):
        return int(round(v * self.ss))

    def font(self, weight, size):
        return self.theme.font(weight, size * self.ss)

    def _col(self, fill, alpha=None):
        if fill is None:
            return None
        if len(fill) == 3:
            r, g, b, a = fill[0], fill[1], fill[2], 255
        else:
            r, g, b, a = fill
        if alpha is not None:
            a = int(round(a * clamp(alpha)))
        return (r, g, b, a)

    # -- text --------------------------------------------------------------
    def _adv(self, s, font, track_px=0):
        if not track_px:
            return self.d.textlength(s, font=font)
        return (sum(self.d.textlength(c, font=font) for c in s)
                + track_px * max(0, len(s) - 1))

    def measure(self, s, weight, size, tracking=0):
        """Text advance width, in design units."""
        f = self.font(weight, size)
        return self._adv(s, f, tracking * self.ss) / self.ss

    def fit_size(self, s, weight, start, max_w, min_size=22, tracking=0):
        size = start
        while size > min_size and self.measure(s, weight, size, tracking) > max_w:
            size -= 2
        return max(min_size, size)

    def text(self, x, y, s, weight, size, fill, anchor="lm", tracking=0, alpha=None):
        f = self.font(weight, size)
        col = self._col(fill, alpha)
        if col[3] <= 0:
            return
        px, py = self.s(x), self.s(y)
        if not tracking:
            self.d.text((px, py), s, font=f, fill=col, anchor=anchor)
            return
        track_px = tracking * self.ss
        total = self._adv(s, f, track_px)
        h = anchor[0] if anchor else "l"
        v = anchor[1] if len(anchor) > 1 else "m"
        if h == "m":
            px -= total / 2
        elif h == "r":
            px -= total
        cx = px
        for c in s:
            self.d.text((cx, py), c, font=f, fill=col, anchor="l" + v)
            cx += self.d.textlength(c, font=f) + track_px

    def text_center(self, cx, y, s, weight, size, fill, tracking=0, alpha=None,
                    anchor_v="m"):
        self.text(cx, y, s, weight, size, fill, anchor="m" + anchor_v,
                  tracking=tracking, alpha=alpha)

    # -- shapes ------------------------------------------------------------
    def rrect(self, x, y, w, h, r, fill=None, outline=None, width=1, alpha=None):
        box = [self.s(x), self.s(y), self.s(x + w), self.s(y + h)]
        rad = self.s(r)
        kw = {}
        if fill is not None:
            kw["fill"] = self._col(fill, alpha)
        if outline is not None:
            kw["outline"] = self._col(outline, alpha)
            kw["width"] = max(1, self.s(width))
        self.d.rounded_rectangle(box, radius=rad, **kw)

    def pill(self, x, y, w, h, fill=None, outline=None, width=1, alpha=None):
        self.rrect(x, y, w, h, h / 2, fill=fill, outline=outline, width=width, alpha=alpha)

    def ellipse(self, cx, cy, rx, ry=None, fill=None, outline=None, width=1, alpha=None):
        ry = rx if ry is None else ry
        box = [self.s(cx - rx), self.s(cy - ry), self.s(cx + rx), self.s(cy + ry)]
        kw = {}
        if fill is not None:
            kw["fill"] = self._col(fill, alpha)
        if outline is not None:
            kw["outline"] = self._col(outline, alpha)
            kw["width"] = max(1, self.s(width))
        self.d.ellipse(box, **kw)

    def line(self, pts, fill, width=1, alpha=None):
        p = [(self.s(x), self.s(y)) for x, y in pts]
        self.d.line(p, fill=self._col(fill, alpha), width=max(1, self.s(width)),
                    joint="curve")

    def rect(self, x, y, w, h, fill=None, outline=None, width=1, alpha=None):
        box = [self.s(x), self.s(y), self.s(x + w), self.s(y + h)]
        kw = {}
        if fill is not None:
            kw["fill"] = self._col(fill, alpha)
        if outline is not None:
            kw["outline"] = self._col(outline, alpha)
            kw["width"] = max(1, self.s(width))
        self.d.rectangle(box, **kw)

    # -- colour fields -----------------------------------------------------
    def grad_rrect(self, x, y, w, h, r, c0, c1, alpha=None, vertical=True):
        """Rounded rect filled with a linear c0 -> c1 gradient."""
        pw, ph = self.s(w), self.s(h)
        if pw <= 1 or ph <= 1:
            return
        a0, a1 = self._col(c0, alpha), self._col(c1, alpha)
        if a0[3] <= 0 and a1[3] <= 0:
            return
        n = max(2, ph if vertical else pw)
        strip = Image.new("RGBA", (1, n) if vertical else (n, 1))
        px = strip.load()
        for i in range(n):
            t = i / (n - 1)
            c = tuple(int(round(a0[k] + (a1[k] - a0[k]) * t)) for k in range(4))
            if vertical:
                px[0, i] = c
            else:
                px[i, 0] = c
        grad = strip.resize((pw, ph), Image.Resampling.BILINEAR)
        mask = Image.new("L", (pw, ph), 0)
        ImageDraw.Draw(mask).rounded_rectangle(
            [0, 0, pw - 1, ph - 1], radius=self.s(r), fill=255)
        grad.putalpha(ImageChops.multiply(grad.getchannel("A"), mask))
        self.img.paste(grad, (self.s(x), self.s(y)), grad)

    def glow(self, cx, cy, r, color, alpha=0.20):
        """Soft radial colour bloom — puts accent into otherwise empty background."""
        pr = self.s(r)
        if pr <= 1:
            return
        col = self._col(color, alpha)
        if col[3] <= 0:
            return
        # Pad by 3 sigma so the blur reaches zero *inside* the tile; without this
        # the tile boundary shows up as a hard rectangle over the background.
        blur = pr * 0.42
        pad = max(1, int(round(blur * 3)))
        size = pr * 2 + pad * 2
        tile = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        ImageDraw.Draw(tile).ellipse(
            [pad, pad, pad + pr * 2 - 1, pad + pr * 2 - 1], fill=col)
        tile = tile.filter(ImageFilter.GaussianBlur(blur))
        self.img.paste(tile, (self.s(cx) - pr - pad, self.s(cy) - pr - pad), tile)

    def tint(self, color, t=0.5):
        """Blend a colour toward the card surface — a light, readable tinted fill.

        Always blends toward `card` (white in both acts) rather than `card2`, so a
        tinted surface stays light and dark ink stays legible on it regardless of act.
        """
        base = self.pal["card"]
        return tuple(int(round(base[i] + (color[i] - base[i]) * clamp(t)))
                     for i in range(3))

    # -- elevation ---------------------------------------------------------
    def drop_shadow(self, x, y, w, h, r, spread=26, alpha=0.16, dy=10):
        """Soft shadow rendered in a local tile, composited under a card."""
        a = int(round(255 * clamp(alpha)))
        if a <= 0:
            return
        pad = spread * 3
        ox, oy = self.s(x - pad), self.s(y - pad + dy)
        tw, th = self.s(w + 2 * pad), self.s(h + 2 * pad)
        if tw <= 0 or th <= 0:
            return
        tile = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
        td = ImageDraw.Draw(tile)
        td.rounded_rectangle([self.s(pad), self.s(pad), self.s(pad + w), self.s(pad + h)],
                             radius=self.s(r), fill=(0, 0, 0, a))
        tile = tile.filter(ImageFilter.GaussianBlur(self.s(spread)))
        # clip paste box to image bounds
        self.img.paste(tile, (ox, oy), tile)

    def card(self, x, y, w, h, r=18, fill=None, elevate=26, shadow_alpha=None,
             alpha=1.0, outline=None, width=1):
        if elevate and alpha > 0.02:
            sa = shadow_alpha if shadow_alpha is not None else (
                0.11 if self.act == "light" else 0.42)
            self.drop_shadow(x, y, w, h, r, spread=elevate, alpha=sa * alpha)
        self.rrect(x, y, w, h, r, fill=fill or self.pal["card"], alpha=alpha,
                   outline=outline, width=width)

    def paste_layer(self, layer, x=0, y=0):
        self.img.paste(layer, (self.s(x), self.s(y)), layer)

    # -- finish ------------------------------------------------------------
    def finish(self):
        if (self.pw, self.ph) == (self.W, self.H):
            return self.img
        return self.img.resize((self.W, self.H), Image.Resampling.LANCZOS)
