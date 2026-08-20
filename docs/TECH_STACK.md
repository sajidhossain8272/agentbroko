# Technology stack

- Python 3.10+: AgentBroko CLI, skill routing, timeline parsing, validation, captions, and process orchestration.
- Python standard library: argparse, dataclasses, JSON, subprocess, pathlib, and temporary files.
- FFmpeg and FFprobe: video/audio decoding, filtering, scaling, encoding, inspection, subtitles, and mixing.
- Optional offline TTS: Piper, espeak-ng/espeak, Windows System.Speech, or macOS `say`.
- Node.js 18+ and npm: optional `agentbroko` launcher and distribution channel.
- pytest: development tests.
- GitHub Actions: cross-platform continuous integration.

AgentBroko does not bundle FFmpeg, voices, media, or model binaries. Users install and license those separately.

