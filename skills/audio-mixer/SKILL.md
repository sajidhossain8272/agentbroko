---
name: audio-mixer
description: Plan and perform local video audio mixing with narration, music ducking, sound effects, loudness targets, fades, and clipping checks.
version: 1.4.5
author: AgentBroko
license: MIT
tags: [audio, mixing, narration, music, sound-design]
---

# Audio Mixer

Use when the user needs voiceover, music, sound effects, ducking, cleanup, or delivery audio guidance.

1. Inspect source tracks, sample rates, channels, durations, and peaks with `ffprobe`.
2. Keep narration intelligible and dominant; duck music roughly 8-12 dB during speech.
3. Add fades, ambience, and effects only when they serve the scene and are license-cleared.
4. Leave headroom, check for clipping, and target platform-appropriate loudness.
5. Render locally with FFmpeg when the files and tools are available, then inspect the final output.

Use `npx agentbroko video-forge speak` for narration and `--audio` with a short template for a mastered audio track. Never claim a mix was rendered if only a mix plan was produced.
