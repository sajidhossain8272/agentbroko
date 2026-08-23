# Instructions for coding agents

This repository is designed to be operated and extended by coding agents. AgentBroko is the product; Video Forge is its first skill.

## Skill contract

- Register each user-facing skill in `src/agentbroko/cli.py` so `agentbroko skills` exposes it.
- Keep a direct skill command for scripting compatibility.
- Add documentation under `docs/` and tests under `tests/`.
- Keep installation predictable through Python packaging and the npm launcher.
- Register new skills in `SKILLS` and route them through `src/agentbroko/cli.py`.

## Editing a user's video

1. Run `video-forge doctor` and report missing local tools.
2. Inspect media with `ffprobe`; do not upload media to a cloud service.
3. Create or edit a JSON project using `docs/PROJECT.md`.
4. Generate narration only when requested. Use an installed offline engine.
5. Run `video-forge validate <project>` before rendering.
6. Render and report the exact output path. Never commit source media or generated output unless the user explicitly asks.

## Repository development

- Keep all functionality local-first and useful without an API key.
- Never add telemetry, hidden network requests, secrets, or committed model binaries.
- Prefer FFmpeg filters and Python standard-library code.
- Add focused tests for project parsing and deterministic helpers.
- Preserve compatibility with Python 3.10+ and Windows, macOS, and Linux.
