"""
Cinematic 2D Rendering Engine for High-Retention Documentary & Storytelling Shorts.
Provides rich atmospheric backgrounds, multi-layered parallax, detailed anatomical/garment
character rendering, volumetric lighting shafts, dynamic particle systems, and cinematic post-FX.
"""

import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

# ----------------------------------------------------------------------------
# 1. Atmospheric & Multi-Layered Environment Generators
# ----------------------------------------------------------------------------

def draw_gradient_rect(img, box, top_color, bottom_color):
    """Draws a vertical linear color gradient across the specified box."""
    x0, y0, x1, y1 = box
    w = x1 - x0
    h = y1 - y0
    if w <= 0 or h <= 0:
        return

    # Generate gradient array
    r = np.linspace(top_color[0], bottom_color[0], h)
    g = np.linspace(top_color[1], bottom_color[1], h)
    b = np.linspace(top_color[2], bottom_color[2], h)
    a = np.linspace(top_color[3] if len(top_color) > 3 else 255,
                    bottom_color[3] if len(bottom_color) > 3 else 255, h)
    
    grad_1d = np.stack([r, g, b, a], axis=1).astype(np.uint8)
    grad_2d = np.tile(grad_1d[:, np.newaxis, :], (1, w, 1))
    grad_img = Image.fromarray(grad_2d, mode="RGBA")
    img.paste(grad_img, (x0, y0), grad_img)

def draw_sandstone_mountains(draw, width, height, offset_y, seed=42, color=(55, 42, 32, 255), crag_color=(38, 28, 20, 255)):
    """Draws realistic, craggy Arabian sandstone desert ridge with layered strata lines."""
    np.random.seed(seed)
    num_pts = 24
    xs = np.linspace(0, width, num_pts)
    ys = offset_y + np.random.uniform(-80, 80, num_pts)
    # Smooth points
    pts = [(0, height)]
    for x, y in zip(xs, ys):
        pts.append((int(x), int(y)))
    pts.append((width, height))
    draw.polygon(pts, fill=color)

    # Geological strata & cliff fissures
    for i in range(len(xs) - 1):
        x_m = int((xs[i] + xs[i+1]) / 2)
        y_m = int((ys[i] + ys[i+1]) / 2)
        draw.line([x_m, y_m, x_m + int(np.random.uniform(-30, 30)), y_m + int(np.random.uniform(80, 220))], fill=crag_color, width=3)
        draw.line([int(xs[i]), int(ys[i] + 40), int(xs[i+1]), int(ys[i+1] + 45)], fill=crag_color, width=2)

# ----------------------------------------------------------------------------
# 2. Detailed Historical Character Silhouette & Clothing Generator
# ----------------------------------------------------------------------------

def draw_ancient_arabian_man(draw, cx, cy, scale=1.0, pose="walk_rear", t=0.0, base_color=(75, 60, 48, 255), wrap_color=(95, 78, 62, 255)):
    """
    Renders a detailed, faceless ancient Arabian character with realistic cloth folds,
    headdress (ghutra/keffiyeh), shoulder mantle, waist sash, and posture articulation.
    
    poses: 'walk_rear', 'push_rock', 'dua_kneel', 'serve_standing', 'turn_away'
    """
    sway = math.sin(t * 4.0 + cx) * 3.0
    breathe = math.sin(t * 2.5) * 2.0

    if pose == "walk_rear":
        # Stride animation
        stride_l = math.sin(t * 5.0) * 18.0 * scale
        stride_r = -stride_l

        # Lower Robe / Thobe Hem
        draw.polygon([
            (cx - 38*scale + sway, cy), 
            (cx + 38*scale + sway, cy), 
            (cx + 62*scale + stride_r, cy + 260*scale), 
            (cx - 62*scale + stride_l, cy + 260*scale)
        ], fill=base_color)

        # Robe Vertical Draped Seam Lines & Shadowing
        draw.line([cx - 15*scale + sway, cy + 30*scale, cx - 25*scale + stride_l*0.5, cy + 250*scale], fill=(35, 26, 20, 200), width=2)
        draw.line([cx + 15*scale + sway, cy + 30*scale, cx + 25*scale + stride_r*0.5, cy + 250*scale], fill=(35, 26, 20, 200), width=2)

        # Upper Torso / Shoulder Mantle
        draw.polygon([
            (cx - 48*scale + sway, cy - 20*scale),
            (cx + 48*scale + sway, cy - 20*scale),
            (cx + 42*scale + sway, cy + 110*scale),
            (cx - 42*scale + sway, cy + 110*scale)
        ], fill=base_color)

        # Head / Traditional Headdress (Ghutra / Keffiyeh)
        draw.ellipse([cx - 25*scale + sway, cy - 85*scale + breathe, cx + 25*scale + sway, cy - 25*scale + breathe], fill=base_color)
        # Flowing fabric tail trailing in desert wind
        tail_flutter = math.sin(t * 7.0 + cx) * 8.0
        draw.polygon([
            (cx - 15*scale + sway, cy - 55*scale + breathe),
            (cx - 55*scale + sway + tail_flutter, cy + 25*scale),
            (cx - 25*scale + sway, cy + 45*scale)
        ], fill=wrap_color)

    elif pose == "dua_kneel":
        # Kneeling / Sitting in Sincere Supplication
        draw.polygon([
            (cx - 65*scale, cy + 60*scale),
            (cx + 65*scale, cy + 60*scale),
            (cx + 90*scale, cy + 240*scale),
            (cx - 90*scale, cy + 240*scale)
        ], fill=base_color)
        # Fabric fold shadows
        draw.line([cx - 30*scale, cy + 80*scale, cx - 45*scale, cy + 220*scale], fill=(25, 18, 14, 220), width=3)
        draw.line([cx + 30*scale, cy + 80*scale, cx + 45*scale, cy + 220*scale], fill=(25, 18, 14, 220), width=3)

        # Torso & Bowed Head
        draw.polygon([(cx - 45*scale, cy), (cx + 45*scale, cy), (cx + 55*scale, cy + 110*scale), (cx - 55*scale, cy + 110*scale)], fill=base_color)
        draw.ellipse([cx - 26*scale, cy - 35*scale + breathe, cx + 26*scale, cy + 25*scale + breathe], fill=base_color)

        # Raised Forearms & Hands in Reverent Du'a (Cupped Palms)
        # Left arm & cupped palm
        draw.polygon([(cx - 42*scale, cy + 30*scale), (cx - 26*scale, cy - 35*scale), (cx - 12*scale, cy - 25*scale), (cx - 28*scale, cy + 35*scale)], fill=wrap_color)
        draw.ellipse([cx - 28*scale, cy - 50*scale, cx - 10*scale, cy - 25*scale], fill=wrap_color)
        # Right arm & cupped palm
        draw.polygon([(cx + 42*scale, cy + 30*scale), (cx + 26*scale, cy - 35*scale), (cx + 12*scale, cy - 25*scale), (cx + 28*scale, cy + 35*scale)], fill=wrap_color)
        draw.ellipse([cx + 10*scale, cy - 50*scale, cx + 28*scale, cy - 25*scale], fill=wrap_color)

    elif pose == "push_rock":
        # Straining Leaning Posture
        strain_shake = math.sin(t * 22.0) * 2.0
        draw.polygon([
            (cx - 40*scale, cy + 30*scale),
            (cx + 35*scale + strain_shake, cy - 25*scale),
            (cx + 55*scale, cy + 270*scale),
            (cx - 65*scale, cy + 270*scale)
        ], fill=base_color)
        draw.ellipse([cx + 5*scale + strain_shake, cy - 75*scale, cx + 45*scale + strain_shake, cy - 25*scale], fill=base_color)
        # Outstretched arms pushing against stone face
        draw.polygon([(cx, cy - 10*scale), (cx + 55*scale + strain_shake, cy - 50*scale), (cx + 65*scale + strain_shake, cy - 30*scale), (cx + 10*scale, cy + 10*scale)], fill=wrap_color)
        draw.ellipse([cx + 50*scale + strain_shake, cy - 55*scale, cx + 75*scale + strain_shake, cy - 25*scale], fill=wrap_color)

    elif pose == "serve_standing":
        # Devoted Son standing upright holding milk bowl
        draw.polygon([(cx - 42*scale, cy), (cx + 42*scale, cy), (cx + 62*scale, cy + 380*scale), (cx - 62*scale, cy + 380*scale)], fill=base_color)
        draw.line([cx - 15*scale, cy + 50*scale, cx - 20*scale, cy + 350*scale], fill=(30, 22, 16, 200), width=2)
        draw.ellipse([cx - 26*scale, cy - 65*scale + breathe, cx + 26*scale, cy - 5*scale + breathe], fill=base_color)
        # Both arms cradling bowl
        draw.ellipse([cx + 25*scale, cy + 60*scale, cx + 135*scale, cy + 125*scale], fill=(135, 95, 65, 255), outline=(85, 55, 35, 255), width=3)
        draw.ellipse([cx + 35*scale, cy + 68*scale, cx + 125*scale, cy + 112*scale], fill=(248, 244, 235, 255)) # Pure white milk

    elif pose == "turn_away":
        # Man stepping back and raising palm in firm moral boundary
        draw.polygon([(cx - 45*scale, cy), (cx + 45*scale, cy), (cx + 70*scale, cy + 380*scale), (cx - 70*scale, cy + 380*scale)], fill=base_color)
        draw.ellipse([cx - 28*scale, cy - 65*scale + breathe, cx + 28*scale, cy - 5*scale + breathe], fill=base_color)
        # Palm raised forward
        draw.polygon([(cx - 40*scale, cy + 35*scale), (cx - 110*scale, cy + 5*scale), (cx - 115*scale, cy + 30*scale), (cx - 45*scale, cy + 60*scale)], fill=wrap_color)
        draw.ellipse([cx - 125*scale, cy - 5*scale, cx - 100*scale, cy + 35*scale], fill=wrap_color)

# ----------------------------------------------------------------------------
# 3. Volumetric God Rays & Atmospheric Dust Particles
# ----------------------------------------------------------------------------

def draw_volumetric_light_shaft(img, p1, p2, p3, p4, color=(255, 240, 190, 120), blur_radius=12):
    """Draws a soft diffused volumetric light shaft with feathered edges."""
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    d.polygon([p1, p2, p3, p4], fill=color)
    if blur_radius > 0:
        overlay = overlay.filter(ImageFilter.GaussianBlur(blur_radius))
    img.paste(Image.alpha_composite(img.convert("RGBA"), overlay), (0, 0))

def draw_floating_dust_particles(draw, width, height, t, num_particles=35, seed=101, color=(255, 235, 170, 180)):
    """Draws floating, organic dust motes dancing in sunbeams."""
    np.random.seed(seed)
    xs = np.random.uniform(0, width, num_particles)
    ys = np.random.uniform(0, height, num_particles)
    sizes = np.random.uniform(2, 6, num_particles)
    speeds = np.random.uniform(15, 45, num_particles)

    for i in range(num_particles):
        px = (xs[i] + math.sin(t * 1.5 + i) * 35) % width
        py = (ys[i] - t * speeds[i]) % height
        r = sizes[i]
        draw.ellipse([px - r, py - r, px + r, py + r], fill=color)

# ----------------------------------------------------------------------------
# 4. Cinematic Post-Processing (Vignette & Film Grain)
# ----------------------------------------------------------------------------

_vignette_mask = None
def apply_cinematic_vignette(img, intensity=0.45):
    """Applies a soft cinematic lens vignette darkening to frame edges."""
    global _vignette_mask
    w, h = img.size
    if _vignette_mask is None or _vignette_mask.size != (w, h):
        # Create radial gradient mask
        y, x = np.ogrid[:h, :w]
        cx, cy = w / 2.0, h / 2.0
        # Normalized distance from center
        dist = np.sqrt(((x - cx) / (w * 0.55)) ** 2 + ((y - cy) / (h * 0.55)) ** 2)
        dist = np.clip(dist - 0.35, 0.0, 1.0)
        vignette_arr = (dist * (255 * intensity)).astype(np.uint8)
        mask_rgba = np.zeros((h, w, 4), dtype=np.uint8)
        mask_rgba[:, :, 3] = vignette_arr
        _vignette_mask = Image.fromarray(mask_rgba, mode="RGBA")
    
    img.paste(_vignette_mask, (0, 0), _vignette_mask)
