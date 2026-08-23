"""audio: text-to-speech voiceover, a music bed, ducking, and the final mux.

Flow (driven by build.py):
  synth_vo(spec, out_dir)        -> per-scene VO clips (mono float32 @ SR) or None
  scene_durations(spec, vo)      -> VO-driven per-scene seconds (fed to Timeline)
  build_mix(spec, out_dir, tl, vo) -> mixed.wav (VO + ducked music), or None
  mux(silent_mp4, mixed_wav, out)  -> final.mp4

Design choices for robustness:
  * All decoding goes through ffmpeg to raw float32 (handles wav/mp3/etc alike).
  * Ducking and normalisation are done in numpy — no fragile ffmpeg filtergraphs —
    then a single mux copies the video and encodes AAC.
  * Everything degrades: no TTS -> music-only; no music file -> a subtle synth pad;
    nothing at all -> build.py falls back to the silent video.
"""

import os
import subprocess
import sys
import wave

import numpy as np

from ._ffmpeg import ffmpeg_bin

SR = 44100
LEAD = 0.35          # silence before a scene's VO starts
TAIL = 0.55          # silence after a scene's VO ends
_MIN_FLOOR = 2.4     # a scene never shorter than this, even for a 3-word line


# --------------------------------------------------------------------------
# decoding / encoding helpers
# --------------------------------------------------------------------------
def _load_audio_mono(path, sr=SR):
    """Decode any audio file to a mono float32 numpy array via ffmpeg."""
    if not path or not os.path.exists(path):
        return None
    cmd = [ffmpeg_bin(), "-v", "error", "-i", path, "-ac", "1", "-ar", str(sr),
           "-f", "f32le", "-"]
    try:
        out = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             check=True).stdout
    except (subprocess.CalledProcessError, OSError):
        return None
    if not out:
        return None
    return np.frombuffer(out, dtype=np.float32).copy()


def _write_wav(path, samples, sr=SR):
    """Write a mono float32 [-1,1] array as 16-bit PCM wav."""
    x = np.clip(samples, -1.0, 1.0)
    pcm = (x * 32767.0).astype("<i2")
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(pcm.tobytes())
    return path


# --------------------------------------------------------------------------
# TTS backends
# --------------------------------------------------------------------------
_PS_SCRIPT = r"""param([string]$TextFile,[string]$OutFile,[int]$Rate,[string]$Voice)
Add-Type -AssemblyName System.Speech
$s = New-Object System.Speech.Synthesis.SpeechSynthesizer
if ($Voice) {
  try { $s.SelectVoice($Voice) }
  catch {
    try {
      $ci = [System.Globalization.CultureInfo]::new($Voice)
      $s.SelectVoiceByHints([System.Speech.Synthesis.VoiceGender]::Female,
                            [System.Speech.Synthesis.VoiceAge]::Adult, 0, $ci)
    } catch {}
  }
}
$s.Rate = $Rate
$s.SetOutputToWaveFile($OutFile)
$t = Get-Content -Raw -Encoding UTF8 $TextFile
$s.Speak($t)
$s.Dispose()
"""


def _tts_windows(text, out_wav, voice_dir, voice="en-US", rate=0):
    if sys.platform != "win32":
        raise RuntimeError("windows TTS backend requires Windows")
    ps_path = os.path.join(voice_dir, "_say.ps1")
    if not os.path.exists(ps_path):
        with open(ps_path, "w", encoding="utf-8") as fh:
            fh.write(_PS_SCRIPT)
    txt_path = out_wav + ".txt"
    with open(txt_path, "w", encoding="utf-8") as fh:
        fh.write(text)
    cmd = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
           "-File", ps_path, txt_path, out_wav, str(int(rate)), str(voice or "")]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL,
                   stderr=subprocess.PIPE)
    return out_wav if os.path.exists(out_wav) else None


def _tts_elevenlabs(text, out_path, voice="Rachel", **_):
    import requests
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        raise RuntimeError("ELEVENLABS_API_KEY not set")
    vid = os.environ.get("ELEVENLABS_VOICE_ID", voice)
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{vid}"
    r = requests.post(url, headers={"xi-api-key": key},
                      json={"text": text, "model_id": "eleven_multilingual_v2"},
                      timeout=60)
    r.raise_for_status()
    with open(out_path, "wb") as fh:
        fh.write(r.content)
    return out_path


def _tts_openai(text, out_path, voice="alloy", **_):
    import requests
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY not set")
    r = requests.post("https://api.openai.com/v1/audio/speech",
                      headers={"Authorization": f"Bearer {key}"},
                      json={"model": "gpt-4o-mini-tts", "voice": voice,
                            "input": text, "response_format": "mp3"},
                      timeout=60)
    r.raise_for_status()
    with open(out_path, "wb") as fh:
        fh.write(r.content)
    return out_path


def _tts_edge(text, out_mp3, voice="en-US-ChristopherNeural", rate=0):
    import asyncio
    import edge_tts
    rate_str = f"+{rate}%" if rate > 0 else (f"{rate}%" if rate < 0 else "+0%")
    async def _run():
        comm = edge_tts.Communicate(text, voice or "en-US-ChristopherNeural", rate=rate_str)
        await comm.save(out_mp3)
    asyncio.run(_run())
    return out_mp3 if os.path.exists(out_mp3) else None


def _tts_say(text, out_aiff):
    cmd = ["say", "-o", out_aiff, text]
    subprocess.run(cmd, check=True)
    return out_aiff if os.path.exists(out_aiff) else None


def _tts_espeak(text, out_wav):
    cmd = ["espeak", "-w", out_wav, text]
    subprocess.run(cmd, check=True)
    return out_wav if os.path.exists(out_wav) else None


def synth_vo(spec, out_dir):
    """Synthesize one VO clip per scene. Returns a list aligned to spec['scenes'],
    each entry {"samples":np.float32, "dur":sec} or None (empty/failed)."""
    voice = spec.get("voice", {})
    backend = (voice.get("backend") or ("windows" if sys.platform == "win32" else "edge")).lower()
    vname = voice.get("voice")
    rate = int(voice.get("rate", 0) or 0)
    scenes = spec["scenes"]

    vo_dir = os.path.join(out_dir, "_vo")
    os.makedirs(vo_dir, exist_ok=True)

    out = []
    for i, sc in enumerate(scenes):
        text = (sc.get("vo") or "").strip()
        if not text:
            out.append(None)
            continue
        try:
            if backend in ("edge", "edge-tts"):
                raw = _tts_edge(text, os.path.join(vo_dir, f"s{i:02d}.mp3"),
                                voice=vname or "en-US-ChristopherNeural", rate=rate)
            elif backend == "windows":
                if sys.platform == "win32":
                    raw = _tts_windows(text, os.path.join(vo_dir, f"s{i:02d}.wav"),
                                       vo_dir, voice=vname or "en-US", rate=rate)
                else:
                    raw = _tts_edge(text, os.path.join(vo_dir, f"s{i:02d}.mp3"),
                                    voice=vname or "en-US-ChristopherNeural", rate=rate)
            elif backend in ("say", "mac"):
                raw = _tts_say(text, os.path.join(vo_dir, f"s{i:02d}.aiff"))
            elif backend == "espeak":
                raw = _tts_espeak(text, os.path.join(vo_dir, f"s{i:02d}.wav"))
            elif backend == "elevenlabs":
                raw = _tts_elevenlabs(text, os.path.join(vo_dir, f"s{i:02d}.mp3"),
                                      voice=vname or "Rachel")
            elif backend == "openai":
                raw = _tts_openai(text, os.path.join(vo_dir, f"s{i:02d}.mp3"),
                                  voice=vname or "alloy")
            else:
                # fallback attempt windows or edge
                try:
                    raw = _tts_edge(text, os.path.join(vo_dir, f"s{i:02d}.mp3"),
                                    voice=vname or "en-US-ChristopherNeural", rate=rate)
                except Exception:
                    raw = _tts_windows(text, os.path.join(vo_dir, f"s{i:02d}.wav"),
                                       vo_dir, voice=vname or "en-US", rate=rate)
        except Exception as e:
            print(f"[audio] scene {i} TTS failed ({e})", file=sys.stderr)
            out.append(None)
            continue

        samples = _load_audio_mono(raw)
        if samples is None or samples.size == 0:
            out.append(None)
            continue
        # trim trailing near-silence so scene cuts land tight on the words
        samples = _trim_silence(samples)
        out.append({"samples": samples, "dur": samples.size / SR})
    if all(v is None for v in out):
        return None
    return out


def _trim_silence(x, thresh=0.006):
    idx = np.where(np.abs(x) > thresh)[0]
    if idx.size == 0:
        return x
    end = min(x.size, idx[-1] + int(0.12 * SR))
    start = max(0, idx[0] - int(0.04 * SR))
    return x[start:end]


# --------------------------------------------------------------------------
# durations
# --------------------------------------------------------------------------
def scene_durations(spec, vo):
    from .spec import default_duration
    scenes = spec["scenes"]
    durs = []
    for i, sc in enumerate(scenes):
        base = default_duration(sc)
        clip = vo[i] if vo and i < len(vo) else None
        if clip:
            floor = max(_MIN_FLOOR, min(base, 3.2))
            durs.append(round(max(clip["dur"] + LEAD + TAIL, floor), 3))
        else:
            durs.append(base)
    return durs


# --------------------------------------------------------------------------
# music bed + mix
# --------------------------------------------------------------------------
def _synth_pad(n, sr=SR):
    """A subtle, slowly-swelling ambient chord — un-annoying background."""
    t = np.arange(n) / sr
    freqs = [110.0, 164.81, 220.0, 329.63]      # A2 / E3 / A3 / E4
    pad = np.zeros(n, dtype=np.float64)
    for k, f in enumerate(freqs):
        detune = 1.0 + 0.0016 * (k - 1.5)
        pad += np.sin(2 * np.pi * f * detune * t) * (0.6 ** k)
    lfo = 0.5 + 0.5 * np.sin(2 * np.pi * 0.05 * t)   # 20s swell
    pad *= 0.10 * (0.6 + 0.4 * lfo)
    # soft 1s fades so it eases in/out with the video
    f = int(sr * 1.0)
    if n > 2 * f:
        ramp = np.linspace(0, 1, f)
        pad[:f] *= ramp
        pad[-f:] *= ramp[::-1]
    return pad.astype(np.float32)


def _music_bed(spec, n, sr=SR):
    music = spec.get("music", {})
    gain = 10.0 ** (float(music.get("gain_db", -19)) / 20.0)
    m = _load_audio_mono(music.get("file")) if music.get("file") else None
    if m is None or m.size == 0:
        bed = _synth_pad(n, sr)
    else:
        if m.size < n:
            reps = int(np.ceil(n / m.size))
            m = np.tile(m, reps)
        bed = m[:n].astype(np.float32)
    return bed * gain


def _envelope(x, sr=SR, win=0.12):
    """Smoothed, normalised 0..1 loudness envelope of the VO for ducking."""
    a = np.abs(x)
    w = max(1, int(sr * win))
    k = np.ones(w, dtype=np.float64) / w
    env = np.convolve(a, k, mode="same")
    peak = env.max()
    if peak <= 1e-6:
        return np.zeros_like(env)
    env = env / peak
    return np.clip(env * 1.4, 0.0, 1.0)      # widen so quiet VO still ducks


def build_mix(spec, out_dir, timeline, vo):
    total = timeline.total_seconds()
    n = int(round(total * SR)) + SR              # +1s tail
    vo_buf = np.zeros(n, dtype=np.float64)

    have_vo = False
    if vo:
        for i, clip in enumerate(vo):
            if not clip:
                continue
            have_vo = True
            start = timeline.scene_start(i) + LEAD
            s0 = int(round(start * SR))
            seg = clip["samples"].astype(np.float64)
            e0 = min(n, s0 + seg.size)
            if s0 < n and e0 > s0:
                vo_buf[s0:e0] += seg[:e0 - s0]

    music = _music_bed(spec, n, SR).astype(np.float64)
    if have_vo:
        duck = 10.0 ** (float(spec.get("music", {}).get("duck_db", -11)) / 20.0)
        env = _envelope(vo_buf)
        music *= duck + (1.0 - duck) * (1.0 - env)

    mix = vo_buf + music
    # peak-limit to -1.5 dBFS (scale down only; never boost quiet mixes)
    peak = np.abs(mix).max()
    target = 10.0 ** (-1.5 / 20.0)
    if peak > target:
        mix *= target / peak

    if not have_vo and (spec.get("music", {}).get("file") is None):
        # music-only with a synth pad is fine, but if it's essentially silent, skip
        if np.abs(mix).max() < 1e-4:
            return None

    return _write_wav(os.path.join(out_dir, "mixed.wav"), mix, SR)


# --------------------------------------------------------------------------
# mux
# --------------------------------------------------------------------------
def mux(silent_mp4, mixed_wav, out_path):
    cmd = [
        ffmpeg_bin(), "-hide_banner", "-loglevel", "error", "-y",
        "-i", silent_mp4, "-i", mixed_wav,
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        "-shortest", "-movflags", "+faststart",
        out_path,
    ]
    subprocess.run(cmd, check=True)
    return out_path
