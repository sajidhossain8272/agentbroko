# AgentBroko usage guide

## Discover commands

```bash
agentbroko --version
agentbroko skills
agentbroko video-forge --help
agentbroko pdf --help
```

## Video Forge

```bash
agentbroko video-forge doctor
agentbroko video-forge init my-video
agentbroko video-forge speak --file my-video/script.txt -o my-video/audio/narration.wav
agentbroko video-forge captions --file my-video/script.txt -o my-video/captions/subtitles.srt
agentbroko video-forge validate my-video/project.json
agentbroko video-forge render my-video/project.json
```

Copy videos into `my-video/media/` and edit `project.json` before rendering. See `docs/PROJECT.md`.

## PDF

```bash
agentbroko pdf info document.pdf
agentbroko pdf text document.pdf -o document.txt
agentbroko pdf render document.pdf -o document-pages --dpi 180
```

Text extraction needs `pypdf`; metadata and rendering need Poppler. See `docs/PDF.md`.

## Updating

```bash
npm update -g agentbroko
agentbroko --version
```

Never share tokens or private media in bug reports.
