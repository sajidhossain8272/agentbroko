from __future__ import annotations

import numpy as np
from PIL import Image
import pytest
from video_forge.cinematic_10x import apply_cinematic_mastering
from video_forge.cinematic_renderer import draw_gradient_rect
from video_forge.shorts.particles import generate_heart_sprite, generate_sparkle_sprite, ParticlePool


def test_cinematic_mastering():
    # Create test 1080x1920 image
    img = Image.new("RGB", (1080, 1920), (120, 100, 80))
    mastered = apply_cinematic_mastering(img, grain_amount=0.02, vignette_strength=0.3, frame_num=0)
    assert mastered.size == (1080, 1920)
    assert mastered.mode == "RGB"


def test_gradient_rect():
    img = Image.new("RGBA", (200, 200), (0, 0, 0, 255))
    draw_gradient_rect(img, (0, 0, 200, 200), (255, 0, 0, 255), (0, 0, 255, 255))
    arr = np.array(img)
    # Top should be red, bottom blue
    assert arr[0, 100, 0] > 200
    assert arr[199, 100, 2] > 200


def test_particle_sprites():
    heart = generate_heart_sprite(size=64)
    assert heart.size == (64, 64)
    assert heart.mode == "RGBA"

    sparkle = generate_sparkle_sprite(size=64)
    assert sparkle.size == (64, 64)
    assert sparkle.mode == "RGBA"


def test_particle_pool():
    pool = ParticlePool(width=1080, height=1920, count=10, particle_type="sparkle")
    assert len(pool.xs) == 10
    frame = Image.new("RGBA", (1080, 1920), (0, 0, 0, 255))
    pool.render(frame, t=1.0)
