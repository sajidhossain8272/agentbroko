---
name: caption-translator
description: Translate subtitles and captions while preserving timing, reading speed, line length, meaning, and culturally appropriate tone.
version: 1.4.5
author: AgentBroko
license: MIT
tags: [captions, subtitles, translation, accessibility]
---

# Caption Translator

Use when the user wants captions translated or localized.

1. Read the source SRT/VTT and preserve cue order, identifiers, timestamps, and formatting.
2. Translate meaning rather than word-for-word phrasing while preserving names, citations, and technical terms.
3. Keep lines short and readable; flag text that cannot fit without changing timing.
4. Preserve speaker intent and mark uncertainty instead of inventing context.
5. Return the translated subtitle file plus a short quality note.

For local files, use `npx agentbroko video-forge captions` for source generation and validate the translated file before export. Do not translate private content to an external service without user approval.
