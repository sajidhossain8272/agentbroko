from __future__ import annotations

import platform
import shutil
import subprocess
from pathlib import Path

from .errors import VideoForgeError
from .process import run


def available_engines() -> list[str]:
    engines: list[str] = []
    if shutil.which("piper"):
        engines.append("piper")
    if shutil.which("espeak-ng") or shutil.which("espeak"):
        engines.append("espeak")
    if platform.system() == "Windows" and shutil.which("powershell"):
        engines.append("windows")
    if platform.system() == "Darwin" and shutil.which("say"):
        engines.append("say")
    return engines


def synthesize(
    text: str,
    output: Path,
    *,
    engine: str = "auto",
    voice: Path | None = None,
    rate: int = 175,
) -> str:
    output.parent.mkdir(parents=True, exist_ok=True)
    choices = available_engines()
    selected = choices[0] if engine == "auto" and choices else engine
    if not selected or selected == "auto":
        raise VideoForgeError("No offline TTS engine found. See docs/TTS.md.")

    if selected == "piper":
        if not voice:
            raise VideoForgeError("Piper requires --voice path/to/model.onnx")
        command = ["piper", "--model", str(voice), "--output_file", str(output)]
        print("+ piper --model ...")
        subprocess.run(command, input=text, text=True, check=True)
    elif selected == "espeak":
        executable = shutil.which("espeak-ng") or shutil.which("espeak")
        assert executable
        run([executable, "-s", str(rate), "-w", output, text])
    elif selected == "windows":
        escaped_text = text.replace("'", "''")
        escaped_output = str(output.resolve()).replace("'", "''")
        script = (
            "Add-Type -AssemblyName System.Speech; "
            "$s=New-Object System.Speech.Synthesis.SpeechSynthesizer; "
            f"$s.Rate={max(-10, min(10, round((rate - 175) / 15)))}; "
            f"$s.SetOutputToWaveFile('{escaped_output}'); "
            f"$s.Speak('{escaped_text}'); $s.Dispose()"
        )
        run(["powershell", "-NoProfile", "-Command", script])
    elif selected == "say":
        run(["say", "-r", str(rate), "-o", output, "--data-format=LEF32@22050", text])
    else:
        raise VideoForgeError(f"Unsupported TTS engine: {selected}")
    return selected

