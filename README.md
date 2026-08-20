# Video Forge

Video Forge is a free, local-first video editing toolkit for people and coding agents. It turns a small JSON timeline into a finished video using FFmpeg, can create subtitles, and can generate narration with an offline text-to-speech engine. No API keys, cloud accounts, telemetry, or paid services are required.

It is intentionally easy for an IDE agent (Cursor, VS Code extensions, Copilot-style agents, or any local model) to operate: agents edit `project.json`, run a command, inspect the output, and iterate.

## Quick start

1. Install Python 3.10+ and FFmpeg (including `ffprobe`). See [docs/INSTALL.md](docs/INSTALL.md).
2. From this repository, run:

   ```bash
   python -m venv .venv
   # Windows: .venv\\Scripts\\activate
   # macOS/Linux: source .venv/bin/activate
   python -m pip install -e .
   video-forge doctor
   video-forge init my-video
   ```

3. Put source videos in `my-video/media/`, edit `my-video/project.json`, and render:

   ```bash
   video-forge validate my-video/project.json
   video-forge render my-video/project.json
   ```

The result is written to the `output` path in the project file. See [docs/QUICKSTART.md](docs/QUICKSTART.md) for a complete example.

## Offline narration and captions

Generate a WAV without an API:

```bash
video-forge speak --file my-video/script.txt --output my-video/audio/narration.wav
video-forge captions --file my-video/script.txt --output my-video/captions/subtitles.srt
```

The command automatically uses Piper, espeak-ng, Windows SAPI, or macOS `say` when available. Piper voice models are downloaded separately by the user and are not bundled in this repository. Details are in [docs/TTS.md](docs/TTS.md).

## Agent workflow

Give your coding agent the task: “Edit `project.json` to make a 30-second vertical trailer from the clips in `media/`, generate narration from `script.txt`, then run `video-forge validate` and `video-forge render`.” Agents can safely change clip order, trims, speed, volumes, output dimensions, title, narration, music, and subtitles.

The project schema is documented in [docs/PROJECT.md](docs/PROJECT.md). Keep media and generated outputs local; `.gitignore` excludes common private media, audio, and output files by default.

## Development

```bash
python -m pip install -e .
python -m pytest
```

## Contact and donations

Questions, ideas, and contributions: [brokeinnovation@gmail.com](mailto:brokeinnovation@gmail.com)

Bitcoin donations: `bc1q59457phgvxtyxvsyuw0k2pqljkcvkt3jej67xh`

Donations are optional and do not unlock features. Please verify the address before sending funds.

## License

MIT. See [LICENSE](LICENSE).

