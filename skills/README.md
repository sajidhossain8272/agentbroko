# AgentBroko skill packages

This directory contains reusable, agent-discoverable skill packages that follow the common Agent Skills convention.

## Included skills

- `video-forge` — local-first video creation, editing, subtitles, and narration.
- `video-edit` — optional post-production workflow for existing footage and reels.

These skills are packaged for ChatGPT/Codex through the repository-level
`.codex-plugin/plugin.json` manifest.

## Standard structure

Each skill package contains:
- `SKILL.md` — agent-facing instructions
- optional scripts/resources for execution

## Example discovery metadata

```json
{
  "name": "video-forge",
  "description": "Create and edit local videos and reels.",
  "path": "skills/video-forge"
}
```
