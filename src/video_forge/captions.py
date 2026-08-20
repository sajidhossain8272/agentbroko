from __future__ import annotations

from pathlib import Path


def _stamp(seconds: float) -> str:
    milliseconds = round(seconds * 1000)
    hours, milliseconds = divmod(milliseconds, 3_600_000)
    minutes, milliseconds = divmod(milliseconds, 60_000)
    secs, milliseconds = divmod(milliseconds, 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{milliseconds:03}"


def text_to_srt(text: str, output: Path, *, words_per_caption: int = 8, seconds_per_caption: float = 3.0) -> None:
    words = text.split()
    blocks: list[str] = []
    for index in range(0, len(words), words_per_caption):
        number = index // words_per_caption + 1
        start = (number - 1) * seconds_per_caption
        end = start + seconds_per_caption
        line = " ".join(words[index:index + words_per_caption])
        blocks.append(f"{number}\n{_stamp(start)} --> {_stamp(end)}\n{line}\n")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(blocks), encoding="utf-8")

