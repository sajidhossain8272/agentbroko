---
name: video-edit
description: Optional desktop editing workflow for polishing an existing video, reel, or project with a local NLE or an external MCP video editor. Use when the user wants to edit existing footage, trim timelines, refine cuts, or apply final polish after local generation.
version: 1.4.3
author: AgentBroko
license: MIT
tags:
  - video
  - editing
  - reels
  - local-first
  - mcp
agentbroko:
  type: skill
  category: media
  capabilities:
    - video-editing
    - timeline-polish
    - short-form-post-production
    - caption-sync
    - optional-mcp-integration
  install:
    npm: npx agentbroko install video-edit
    local: ./skills/video-edit
---

# Video Edit

Use this skill when the user wants to refine or polish an existing video project instead of generating a completely new one from a brief.

## When to use this skill

- trim or rearrange existing footage
- add a final polish pass after Video Forge renders a first draft
- edit a social reel or short in a desktop editor or MCP-connected workflow
- perform caption sync, pacing tweaks, and final export adjustments

## Routing rules

1. When a user asks for a new video from a prompt, prefer `video-forge`.
2. When a user already has footage and wants editing, pacing, trimming, or delivery polish, use `video-edit`.
3. If a desktop editor or MCP bridge is connected, use it as an optional improvement layer rather than pretending it is built into AgentBroko.

## Reusable workflow patterns from the Video Edit workspace

- 9:16 vertical short and reel production
- final cut polishing, pacing, and timeline adjustments
- subtitle synchronization and social caption cleanup
- thumbnail and SEO metadata framing
- short-form story, romantic, and tech edit templates

## Commands

```bash
npx agentbroko add video-edit
npx agentbroko video-forge short --type story --theme golden -o outputs/story_short.mp4
```

## Output expectations

Do not claim a native desktop editor is bundled inside AgentBroko unless it is explicitly connected in the runtime environment. The repo should explain the divide between local generation via Video Forge and optional external editing tooling.