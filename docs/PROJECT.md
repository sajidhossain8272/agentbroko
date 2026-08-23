# Project and Spec Schemas

AgentBroko Video Forge supports two primary video production workflows:

---

## 1. Declarative Procedural Specs (`spec.json`)

Used for high-retention marketing ads, product launch videos, kinetic typography, and motion graphics. Rendered via PIL + NumPy frame compositing streamed straight to FFmpeg `rawvideo` `libx264`.

### Top-level Structure:
```json
{
  "brand": {
    "name": "MyProduct",
    "accent": "#3B5BFF",
    "url": "https://myproduct.app",
    "font": null
  },
  "video": {
    "width": 1920,
    "height": 1080,
    "fps": 30,
    "target_seconds": 30,
    "supersample": 1.5,
    "crossfade": 0.45,
    "fade_in": 0.6,
    "fade_out": 0.9
  },
  "voice": {
    "backend": "edge",
    "voice": "en-US-ChristopherNeural",
    "rate": 0
  },
  "music": {
    "file": "audio/bed.mp3",
    "gain_db": -19.0,
    "duck_db": -11.0
  },
  "scenes": [
    {
      "type": "cold_open",
      "act": "light",
      "glyph": "play",
      "label": "INTRODUCING",
      "vo": "Introducing MyProduct. Built for speed."
    },
    {
      "type": "statement",
      "act": "dark",
      "kicker": "THE VALUE",
      "lines": [
        {"text": "10x Faster Execution", "color": "accent"},
        {"text": "Zero Cloud API Lock-in", "color": "ink"}
      ],
      "vo": "Experience extreme performance locally on your machine."
    },
    {
      "type": "pill_list",
      "act": "light",
      "items": ["Local-First", "High Retention", "Kinetic Subtitles"],
      "vo": "Engineered for creators and autonomous agents."
    },
    {
      "type": "cta",
      "act": "dark",
      "lines": [{"text": "Get Started Today", "color": "accent"}],
      "button": "Download Now",
      "url": "myproduct.app",
      "vo": "Get started with AgentBroko today."
    },
    {
      "type": "logo_reveal",
      "act": "light",
      "wordmark": "MyProduct",
      "mark": "play",
      "vo": "MyProduct. Built for the future."
    }
  ]
}
```

### Supported Scene Types:
- `cold_open`: Minimalist opener with glyph and eyebrow kicker.
- `statement`: 1-3 lines of large punchy typography with color accents.
- `pill_list`: 3-5 outlined badges/chips with pop-in easing.
- `message`: Interactive chat-bubble beat with prompt / reply styling.
- `node_stack`: Multi-column architectural system flow diagram.
- `orbit`: Centered focal sphere with orbiting benefit nodes.
- `waveform`: Audio frequency visualization with centered caption.
- `feature_grid`: 2-6 card feature grid with title and descriptions.
- `stat`: Large hero metric (e.g. `10x`, `$0`, `99.9%`) with caption.
- `split_compare`: Left vs right comparison card with directional transition.
- `cta`: Closing call-to-action button and destination URL.
- `logo_reveal`: Animated final brand lockup with mark and wordmark.
- `screenshot`: Framed product screenshot with Ken Burns push-in.

---

## 2. Clip Timelines (`project.json`)

Used for assembling recorded MP4 footage, B-roll, voiceover tracks, and subtitle burning.

```json
{
  "output": "outputs/final.mp4",
  "title": "My Video",
  "video": { "width": 1920, "height": 1080, "fps": 30 },
  "clips": [
    { "source": "media/clip-01.mp4", "start": 0, "duration": 5, "speed": 1, "volume": 1 }
  ],
  "audio": {
    "narration": "audio/narration.wav",
    "music": "audio/bed.mp3",
    "music_volume": 0.12
  },
  "subtitles": "captions/subtitles.srt"
}
```
