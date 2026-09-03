# Changelog

All notable changes will be documented here. This project follows Semantic Versioning where practical.

## 1.4.2 - 2026-09-04

### ChatGPT Integration
- Added an OpenAPI contract for registering AgentBroko as a Custom GPT Action.
- Added a legacy `ai-plugin.json` compatibility manifest for plugin discovery tools.
- Added API contract tests and setup documentation.

## 1.4.1 - 2026-09-04

### Optional Video Edit Workflow
- Added discoverable `video-edit` skill packaging for existing footage, reels, timeline polish, caption sync, and optional MCP-connected desktop editing.
- Documented routing between local Video Forge generation and external editing tools without adding a mandatory editor dependency.
- Added reusable 9:16 short, social metadata, and post-production workflow guidance from the Video Edit workspace.

## 1.4.0 - 2026-08-24

### 🚀 Video Forge 10/10 Masterclass Procedural & Cinematic Engine
- **Procedural Motion Graphics Engine**: Added 13+ procedural scene types (`cold_open`, `statement`, `pill_list`, `message`, `node_stack`, `orbit`, `waveform`, `feature_grid`, `stat`, `split_compare`, `cta`, `logo_reveal`, `screenshot`) streamed directly to FFmpeg `rawvideo`.
- **Prompt-to-Video Generator**: Added `agentbroko video-forge generate "<brief>"` to turn natural language product briefs directly into broadcast MP4 ad videos.
- **9:16 Vertical Storytelling Shorts Suite**: Added vertical documentary and viral short renderer with atmospheric 3D parallax dunes, sandstone mountain ridges, volumetric god rays, character silhouette generation, and particle physics (floating vector hearts, twinkling sparkles, dust motes).
- **10/10 Cinematic Mastering**: Built-in 256-entry warm teal-orange LUT color grade, tiled 35mm film grain buffer with rolling shift, and precomputed radial vignette.
- **Advanced VO & Audio Ducking Engine**: Added `edge-tts` high-fidelity neural voice support, dynamic speech-driven scene duration solver, numpy loudness envelope calculation with real-time music ducking, peak limiting (-1.5 dBFS), and procedural ambient chord pads.
- **Kinetic Safe-Area Typography**: Pop-in spring easing, frosted glass pill badges, drop shadows, dual-tone glowing borders, and Ken Burns character levitation.
- **Unified CLI**: Intelligent `video-forge render` auto-detecting declarative `spec.json` and timeline `project.json`.

## 1.3.0 - 2026-08-23

- Released Agent-First IDE workflow, `npx agentbroko init` command, `.agents/skills/` provisioning, single-skill installer (`agentbroko add <skill>`), repo cloner, and complete developer documentation.
- Integrated PDF Playbook publication-grade handbook engine.

## 1.2.1 - 2026-08-23

- Bumped version to 1.2.1 and included test coverage for workspace initialization and recovery guides.

## 1.1.0 - 2026-08-20

- Added the AgentBroko PDF skill for metadata, text extraction, and page rendering.
- Added a complete end-user usage guide.

## 1.0.0 - 2026-08-20

- Initial Video Forge CLI with JSON timelines, FFmpeg rendering, captions, audio mixing, and offline text-to-speech support.
