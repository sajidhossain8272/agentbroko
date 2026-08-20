# Installation

## FFmpeg

Install FFmpeg and ensure both `ffmpeg` and `ffprobe` are on your PATH.

- Windows: install a trusted FFmpeg build, extract it, and add its `bin` directory to PATH.
- macOS: `brew install ffmpeg`
- Debian/Ubuntu: `sudo apt update && sudo apt install ffmpeg`

## Python package

Python 3.10 or newer is recommended:

```bash
python -m venv .venv
# Windows PowerShell
.venv\\Scripts\\Activate.ps1
# macOS/Linux
source .venv/bin/activate
python -m pip install -e .
```

No runtime Python dependency is required beyond the standard library.

