from __future__ import annotations

import numpy as np
import pytest
from video_forge.audio import _synth_pad, _envelope, _trim_silence


def test_synth_pad_generation():
    sr = 44100
    n = sr * 2  # 2 seconds
    pad = _synth_pad(n, sr=sr)
    assert len(pad) == n
    assert pad.dtype == np.float32
    # Ensure it's not silent
    assert np.max(np.abs(pad)) > 0.01


def test_envelope_calculation():
    sr = 44100
    # Simulate a burst of audio in the middle
    x = np.zeros(sr * 2, dtype=np.float32)
    x[int(sr * 0.5):int(sr * 1.5)] = 0.5
    env = _envelope(x, sr=sr)
    assert len(env) == len(x)
    assert env.max() > 0.5
    assert env[0] < 0.1


def test_trim_silence():
    sr = 44100
    x = np.zeros(sr * 3, dtype=np.float32)
    # Audio only in the middle second
    x[sr:sr * 2] = 0.8
    trimmed = _trim_silence(x, thresh=0.01)
    assert len(trimmed) < len(x)
    assert len(trimmed) >= sr
