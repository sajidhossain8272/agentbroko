# AgentBroko

AgentBroko is a local-first skills hub for developers, coding agents, and creative tools. Install AgentBroko once, then discover and use skills from one command. Video Forge is the first skill; future skills will use the same product and CLI.

No API keys, cloud accounts, telemetry, or paid services are required for the current skill.

## Install

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -e .
agentbroko skills
```

The npm entrypoint is also available as a launcher:

```bash
npm install -g agentbroko
agentbroko skills
```

Python 3.10+ and FFmpeg/FFprobe are required. See [docs/INSTALL.md](docs/INSTALL.md).

## Current skill: Video Forge

```bash
agentbroko video-forge doctor
agentbroko video-forge init my-video
agentbroko video-forge validate my-video/project.json
agentbroko video-forge render my-video/project.json
agentbroko video-forge speak --file my-video/script.txt --output my-video/audio/narration.wav
agentbroko video-forge captions --file my-video/script.txt --output my-video/captions/subtitles.srt
```

The direct `video-forge` command remains available for backwards compatibility. See [docs/QUICKSTART.md](docs/QUICKSTART.md), [docs/PROJECT.md](docs/PROJECT.md), and [docs/TTS.md](docs/TTS.md).

## Extending AgentBroko

Register each future skill in `src/agentbroko/cli.py`, give it documentation and tests, and keep it local-first with no hidden network calls. See [AGENTS.md](AGENTS.md).

## Contact and donations

Contact: [brokeinnovation@gmail.com](mailto:brokeinnovation@gmail.com)

Bitcoin: `bc1q59457phgvxtyxvsyuw0k2pqljkcvkt3jej67xh`

MIT licensed. See [LICENSE](LICENSE).
