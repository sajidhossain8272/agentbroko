"""
Procedural particle physics simulation for high-retention vertical shorts & reels.
Generates floating vector hearts, twinkling star sparkles, bokeh, and dust motes.
"""

from __future__ import annotations

import math
import numpy as np
from PIL import Image, ImageDraw


def generate_heart_sprite(size: int = 128, color: tuple = (255, 75, 130, 255)) -> Image.Image:
    """Renders a smooth vector heart glyph with border glow."""
    S = size * 4
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    pts = []
    cx = S / 2
    cy = S * 0.48
    scale = S / 36.0
    for deg in range(360):
        rad = math.radians(deg)
        x = 16 * (math.sin(rad) ** 3)
        y = -(13 * math.cos(rad) - 5 * math.cos(2 * rad) - 2 * math.cos(3 * rad) - math.cos(4 * rad))
        pts.append((cx + x * scale, cy + y * scale))
    draw.polygon(pts, fill=color)
    outline_col = (255, 255, 255, int(color[3] * 0.7 if len(color) > 3 else 180))
    draw.polygon(pts, outline=outline_col, width=max(1, int(S / 45)))
    return im.resize((size, size), Image.Resampling.LANCZOS)


def generate_sparkle_sprite(size: int = 128, color: tuple = (255, 235, 130, 255)) -> Image.Image:
    """Renders an 8-point twinkling star sparkle."""
    S = size * 4
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    cx, cy = S / 2, S / 2
    r_outer = S * 0.46
    r_inner = S * 0.08
    pts = []
    for i in range(8):
        angle = i * math.pi / 4
        r = r_outer if (i % 2 == 0) else r_inner
        pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(pts, fill=color)
    draw.ellipse([cx - r_inner * 1.8, cy - r_inner * 1.8, cx + r_inner * 1.8, cy + r_inner * 1.8], fill=(255, 255, 255, 255))
    return im.resize((size, size), Image.Resampling.LANCZOS)


class ParticlePool:
    """Pre-computed particle simulation pool with sinusoidal drift and buoyancy."""
    def __init__(self, width: int = 1080, height: int = 1920, count: int = 40, particle_type: str = "sparkle", seed: int = 42):
        self.width = width
        self.height = height
        self.count = count
        self.particle_type = particle_type
        
        np.random.seed(seed)
        self.xs = np.random.uniform(40, width - 40, count)
        self.ys = np.random.uniform(0, height, count)
        self.speeds = np.random.uniform(35, 120, count)
        self.drifts = np.random.uniform(15, 45, count)
        self.freqs = np.random.uniform(0.8, 2.5, count)
        self.phases = np.random.uniform(0, math.pi * 2, count)
        self.scales = np.random.uniform(0.4, 1.2, count)

        # Pre-cache sprite variants
        if particle_type == "heart":
            self.sprites = [
                generate_heart_sprite(size=int(48 * s), color=(255, 60, 120, 220)) for s in [0.5, 0.75, 1.0, 1.25]
            ]
        else:
            self.sprites = [
                generate_sparkle_sprite(size=int(40 * s), color=(255, 235, 140, 230)) for s in [0.5, 0.75, 1.0, 1.25]
            ]

    def render(self, img: Image.Image, t: float):
        """Composite all simulated particles onto the target frame."""
        for i in range(self.count):
            y = (self.ys[i] - t * self.speeds[i]) % self.height
            x = (self.xs[i] + math.sin(t * self.freqs[i] + self.phases[i]) * self.drifts[i]) % self.width
            
            # Select nearest scale bucket
            sprite_idx = min(len(self.sprites) - 1, max(0, int(self.scales[i] * len(self.sprites) / 1.3)))
            sp = self.sprites[sprite_idx]
            sw, sh = sp.size
            
            # Simple alpha paste
            img.paste(sp, (int(x - sw / 2), int(y - sh / 2)), sp)
