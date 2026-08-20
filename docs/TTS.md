# Offline text-to-speech

`video-forge speak` never calls a web API. It detects local engines in this order:

1. Piper, when installed and given a local `.onnx` voice model with `--voice`.
2. espeak-ng/espeak.
3. Windows SAPI through PowerShell.
4. macOS `say`.

Check what is available with `video-forge doctor`. Piper generally sounds most natural, but its model files are large and must be obtained and licensed by the user. Do not commit voice models or private recordings; the repository ignores common audio and model extensions.

