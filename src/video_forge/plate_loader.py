"""
Seamless AI Plate & Procedural Layer Compositing Engine.
Supports loading AI-generated image plates (e.g. from Gemini / Imagen / Midjourney)
and applying dynamic Ken Burns push-ins, parallax layers, rain/dust particles,
volumetric light shafts, and cinematic grade filters.
"""

import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

def load_or_render_plate(scene_name, default_render_fn, assets_dir="assets/scenes", p=0.0, t=0.0, target_size=(1080, 1920)):
    """
    Checks if an AI-generated image plate exists at assets_dir/{scene_name}.png (or .jpg).
    If found, loads it, scales it with Ken Burns zoom/pan, and composites over it.
    If not found, falls back gracefully to default_render_fn(p, t).
    """
    w, h = target_size
    possible_paths = [
        os.path.join(assets_dir, f"{scene_name}.png"),
        os.path.join(assets_dir, f"{scene_name}.jpg"),
        os.path.join(assets_dir, f"{scene_name}.jpeg"),
        os.path.join(assets_dir, f"{scene_name}.webp"),
    ]

    found_path = None
    for p_path in possible_paths:
        if os.path.exists(p_path):
            found_path = p_path
            break

    if found_path is not None:
        try:
            base_plate = Image.open(found_path).convert("RGBA")
            # Apply Ken Burns subtle push-in & pan
            zoom = 1.0 + 0.08 * p
            crop_w = int(w / zoom)
            crop_h = int(h / zoom)

            # Smooth center pan
            pan_x = int((w - crop_w) / 2 + math.sin(t * 0.5) * 15.0)
            pan_y = int((h - crop_h) / 2)

            # If plate is different size, resize
            if base_plate.size != (w, h):
                base_plate = base_plate.resize((w, h), Image.Resampling.LANCZOS)

            cropped = base_plate.crop((max(0, pan_x), max(0, pan_y), min(w, pan_x + crop_w), min(h, pan_y + crop_h)))
            return cropped.resize((w, h), Image.Resampling.LANCZOS)
        except Exception as e:
            print(f"Warning: Failed to load image plate {found_path}: {e}")

    # Fallback to rich procedural engine
    return default_render_fn(p, t)
