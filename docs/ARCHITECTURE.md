# Architecture

AgentBroko is a small command router with independently documented skills.

```text
agentbroko CLI
  -> skill registry
     -> video-forge CLI
        -> project parser and validation
        -> FFmpeg/FFprobe process layer
        -> offline TTS adapters
        -> captions and output files
```

The Python package contains the real skill implementation. The npm package is a familiar launcher for developer environments and delegates to the local Python module. It does not upload files or implement rendering in Node.js.

Video Forge represents edits as JSON so humans and coding agents can make deterministic changes. It normalizes clips, concatenates them, mixes optional narration/music, burns optional subtitles, and produces an MP4 plus a minimal manifest.

Design principles: local-first processing, explicit files, no required secrets, replaceable skill modules, standard CLI behavior, and small dependency surface.

