# Video Edit MCP and Optional Desktop Editing Workflow

This project keeps a clear boundary between its built-in local engine and any optional external desktop editing tool. AgentBroko's primary generation engine remains Video Forge; the optional Video Edit workflow exists for cases where the user already has footage or an existing project and wants a final polishing pass.

## Routing rules

- New video from a brief or concept -> `video-forge`
- Existing footage or project -> `video-edit`
- Optional external MCP editor -> only if explicitly connected in the user's environment

## Why this is optional

AgentBroko is designed to be local-first, offline, and honest about tool boundaries. It does not claim to own an NLE or video desktop application if the runtime is not connected to one. The Video Edit skill simply documents the workflow, required judgment, and safe routing pattern.

## Common patterns from the Video Edit workspace

- 9:16 vertical storytelling shorts and reels
- pacing and timeline polish after a first AI-generated pass
- caption sync and export cleanup
- thumbnail and social SEO framing
- story, romantic, and tech short templates

## Recommended agent behavior

1. Prefer `video-forge` for generating a video from a textual brief.
2. Switch to `video-edit` when the project is already in progress or the user wants to refine an existing asset.
3. If an MCP editor is connected, treat it as a tool integration rather than as a packaged feature of AgentBroko.
4. Validate output locally with FFmpeg / ffprobe before final delivery.

## Example prompts

- "Create a 30-second launch ad for my SaaS product."
- "Polish this existing reel and tighten the pacing in 9:16."
- "Use the optional visual editor to trim the rough cut and add captions."

## Summary

This registry keeps the product useful for both creation and editing without bundling a fake dependency. That gives AgentBroko a truthful architecture while still making the desktop-edit workflow discoverable to AI agents.
