# Quickstart

```bash
video-forge init demo
```

Copy one or more videos into `demo/media/`. Edit `demo/project.json`:

```json
{
  "output": "outputs/short.mp4",
  "title": "A local edit",
  "video": {"width": 1080, "height": 1920, "fps": 30},
  "clips": [
    {"source": "media/a.mp4", "start": 3, "duration": 7, "speed": 1.0, "volume": 1.0},
    {"source": "media/b.mp4", "start": 0, "duration": 6, "speed": 1.2, "volume": 0.7}
  ],
  "audio": {"narration": "audio/narration.wav", "music": null, "music_volume": 0.12},
  "subtitles": "captions/subtitles.srt"
}
```

Then:

```bash
video-forge speak --text "Your narration goes here." --output demo/audio/narration.wav
video-forge captions --text "Your narration goes here." --output demo/captions/subtitles.srt
video-forge validate demo/project.json
video-forge render demo/project.json
```

If your source has no audio, omit narration or provide an audio file. FFmpeg handles scaling, padding, trimming, speed, volume, title overlays, subtitles, and audio mixing.

