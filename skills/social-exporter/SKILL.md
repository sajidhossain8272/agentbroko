---
name: social-exporter
description: Prepare validated video exports for YouTube Shorts, TikTok, Instagram Reels, square feeds, and landscape platforms with correct dimensions, frame rate, codecs, captions, audio, and filenames.
version: 1.4.5
author: AgentBroko
license: MIT
tags: [social, export, shorts, reels, tiktok, youtube]
---

# Social Exporter

Use when the user wants platform-ready deliverables.

Ask which platforms, duration, aspect ratios, caption treatment, audio policy, and quality target are required. Build an export matrix covering filename, dimensions, FPS, codec, bitrate/CRF, audio, caption mode, thumbnail, and metadata. For local rendering use Video Forge and FFmpeg, then inspect every output with `ffprobe`.

Default presets:
- Shorts/Reels/TikTok: 1080x1920, 9:16, H.264, yuv420p, AAC, faststart.
- Square feed: 1080x1080, 1:1, H.264, yuv420p, AAC, faststart.
- Landscape: 1920x1080, 16:9, H.264, yuv420p, AAC, faststart.

Do not promise platform acceptance or performance. Flag music licensing, watermark, safe-area, and caption risks before delivery.
