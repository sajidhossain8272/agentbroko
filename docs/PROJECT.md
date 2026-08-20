# Project file schema

`project.json` uses paths relative to the project file unless an absolute path is supplied.

- `output`: destination MP4.
- `title`: optional title overlay shown for the first four seconds.
- `video.width`, `video.height`, `video.fps`: output format.
- `clips`: ordered list. Each clip has `source`, optional `start`, `duration`, `speed`, and `volume`.
- `audio.narration`: optional narration file mixed with the first clip's audio.
- `audio.music`: optional looping music file.
- `audio.music_volume`: music gain, usually `0.05`–`0.25`.
- `subtitles`: optional SRT/VTT subtitle file burned into the video.

Transitions are reserved for future timeline versions; the current stable renderer uses clean cuts between clips.

