from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from typing import Iterable

from .errors import VideoForgeError


def require_command(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise VideoForgeError(
            f"Required command '{name}' was not found. See docs/INSTALL.md."
        )
    return path


def run(command: Iterable[str], *, cwd: Path | None = None) -> None:
    args = [str(item) for item in command]
    print("+", " ".join(args))
    try:
        subprocess.run(args, cwd=cwd, check=True)
    except subprocess.CalledProcessError as exc:
        raise VideoForgeError(f"Command failed with exit code {exc.returncode}") from exc


def capture(command: Iterable[str]) -> str:
    args = [str(item) for item in command]
    try:
        result = subprocess.run(
            args, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
    except subprocess.CalledProcessError as exc:
        message = exc.stderr.strip() or f"exit code {exc.returncode}"
        raise VideoForgeError(f"Command failed: {message}") from exc
    return result.stdout.strip()

