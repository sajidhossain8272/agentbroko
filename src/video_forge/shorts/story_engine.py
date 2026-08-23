"""
Storytelling vertical video engine (9:16 / 1080x1920 @ 30 or 60 FPS).
Assembles multi-layered atmospheric backgrounds, 3D parallax, volumetric lighting,
particle simulations, voiceover-synchronized subtitles, and FFmpeg rawvideo encoding.
"""

from __future__ import annotations

import math
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from .._ffmpeg import ffmpeg_bin
from ..cinematic_renderer import (
    draw_gradient_rect,
    draw_sandstone_mountains,
    draw_ancient_arabian_man,
    draw_volumetric_light_shaft,
    draw_floating_dust_particles,
    apply_cinematic_vignette,
)
from ..cinematic_10x import (
    apply_cinematic_mastering,
    draw_photorealistic_dunes,
    draw_photorealistic_sun_glare,
    draw_kinetic_subtitles,
)
from .particles import ParticlePool


def get_system_font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont:
    paths = [
        r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\seguibl.ttf",
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def render_vertical_story(
    scenes: List[Dict[str, Any]],
    output_path: str,
    fps: int = 30,
    width: int = 1080,
    height: int = 1920,
    theme: str = "golden",
    include_particles: bool = True,
    audio_path: Optional[str] = None,
    mastering: bool = True,
) -> str:
    """Render a vertical 9:16 story video directly to MP4 using FFmpeg rawvideo pipe."""
    total_seconds = sum(sc.get("duration", 3.5) for sc in scenes)
    total_frames = int(round(total_seconds * fps))

    # Pre-calculate scene start times
    start_times = []
    curr = 0.0
    for sc in scenes:
        start_times.append(curr)
        curr += sc.get("duration", 3.5)

    font_sub = get_system_font(size=44, bold=True)
    particles = ParticlePool(width=width, height=height, count=30, particle_type="sparkle") if include_particles else None

    # Set up FFmpeg rawvideo pipe
    ffmpeg = ffmpeg_bin()
    cmd = [
        ffmpeg, "-hide_banner", "-loglevel", "error", "-y",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{width}x{height}", "-r", str(fps),
        "-i", "-",
    ]
    if audio_path and os.path.exists(audio_path):
        cmd.extend(["-i", audio_path, "-c:a", "aac", "-b:a", "192k", "-shortest"])
    else:
        cmd.extend(["-an"])

    cmd.extend([
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        output_path,
    ])

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)

    try:
        for f in range(total_frames):
            t = f / fps
            
            # Identify active scene
            sc_idx = 0
            for i, st in enumerate(start_times):
                if t >= st:
                    sc_idx = i
            
            sc = scenes[sc_idx]
            sc_start = start_times[sc_idx]
            sc_dur = sc.get("duration", 3.5)
            p = min(1.0, max(0.0, (t - sc_start) / sc_dur))

            # 1. Base gradient sky
            frame = Image.new("RGBA", (width, height), (0, 0, 0, 255))
            if theme == "sunset":
                draw_gradient_rect(frame, (0, 0, width, height), (38, 18, 30, 255), (185, 95, 50, 255))
            else:
                draw_gradient_rect(frame, (0, 0, width, height), (22, 28, 48, 255), (210, 150, 80, 255))

            draw = ImageDraw.Draw(frame)

            # 2. Sun glare & god rays
            draw_photorealistic_sun_glare(frame, sun_center=(width // 2, 350), intensity=0.9, palette=theme)
            draw_volumetric_light_shaft(frame, (width // 2 - 100, 350), (width // 2 + 100, 350), (width, height - 300), (0, height - 300), blur_radius=16)

            # 3. 3D Parallax Sand Dunes / Mountain Ridge
            draw_photorealistic_dunes(draw, width, height, t=t, p=p, horizon_y=850, palette_type=theme)

            # 4. Character Silhouette (if specified)
            pose = sc.get("pose", "walk_rear")
            char_x = int(width // 2 + math.sin(t * 0.8) * 30)
            char_y = 1180
            draw_ancient_arabian_man(draw, char_x, char_y, scale=1.1, pose=pose, t=t)

            # 5. Simulated Dust & Sparkle Particles
            if particles:
                particles.render(frame, t)
            draw_floating_dust_particles(draw, width, height, t, num_particles=25)

            # 6. Kinetic Safe-Area Subtitles
            sub_text = sc.get("text") or sc.get("vo") or ""
            if sub_text:
                draw_kinetic_subtitles(draw, sub_text, font=font_sub, center_y=1640, max_width=width - 120)

            # 7. Cinematic Mastering (LUT + Vignette + 35mm Grain)
            rgb_frame = frame.convert("RGB")
            if mastering:
                final_img = apply_cinematic_mastering(rgb_frame, grain_amount=0.02, vignette_strength=0.35, frame_num=f)
            else:
                final_img = rgb_frame

            proc.stdin.write(final_img.tobytes())

        proc.stdin.close()
        rc = proc.wait()
        if rc != 0:
            raise RuntimeError(f"FFmpeg render failed with returncode {rc}")

    except Exception:
        proc.kill()
        raise

    return output_path
