---
name: video-forge
description: Create and edit local videos, reels, subtitles, and narration using FFmpeg and AgentBroko's procedural video engine.
version: 1.4.0
author: AgentBroko
license: MIT
tags:
  - video
  - editing
  - ffmpeg
  - local-first
  - reels
agentbroko:
  type: skill
  category: media
  capabilities:
    - video-generation
    - reels-and-shorts
    - subtitles
    - narration
    - ffmpeg-rendering
  install:
    npm: npx agentbroko install video-forge
    local: ./skills/video-forge
---

# Video Forge

Use this skill when the user wants to create or edit a video locally without uploading content to cloud services.

## When to use this skill

Choose this skill for requests such as:
- generate a short-form video or promo
- render a 9:16 vertical reel
- add subtitles or narration to footage
- edit clips together with transitions and captions
- convert a project spec into an MP4 using FFmpeg

## Required local tools

- FFmpeg
- FFprobe
- Python 3.10+

## Standard workflow

1. Validate the project or spec file before rendering.
2. Prepare local media assets and narration.
3. Run the AgentBroko CLI to render or edit the video.
4. Inspect output with ffprobe and verify the final export path.

## Commands

```bash
npx agentbroko video-forge validate project.json
npx agentbroko video-forge render project.json
npx agentbroko video-forge short --type story --theme golden -o outputs/story_short.mp4
npx agentbroko video-forge speak --text "Welcome to AgentBroko." --output audio/vo.wav --engine auto
```

## Output expectations

The agent should prefer local rendering, preserve original source media locally, and only output the final MP4 path or project file after validation succeeds.

## Safety and trust

This skill is local-first and designed for offline use. It should never rely on remote video processing services when a local engine is available.
