from __future__ import annotations

import json
import tempfile
from pathlib import Path

from .errors import VideoForgeError
from .process import capture, require_command, run
from .project import Clip, Project, validate_project


def duration(path: Path) -> float:
    ffprobe = require_command("ffprobe")
    value = capture([
        ffprobe, "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", path,
    ])
    try:
        return float(value)
    except ValueError as exc:
        raise VideoForgeError(f"Could not determine duration of {path}") from exc


def _prepare_clip(clip: Clip, output: Path, project: Project) -> None:
    ffmpeg = require_command("ffmpeg")
    command: list[str | Path] = [ffmpeg, "-y", "-ss", str(clip.start)]
    if clip.duration is not None:
        command += ["-t", str(clip.duration)]
    command += ["-i", clip.source]
    vf = (
        f"scale={project.width}:{project.height}:force_original_aspect_ratio=decrease,"
        f"pad={project.width}:{project.height}:(ow-iw)/2:(oh-ih)/2:black,"
        f"fps={project.fps},setsar=1,setpts=PTS/{clip.speed}"
    )
    af = f"volume={clip.volume},atempo={clip.speed}"
    command += [
        "-vf", vf, "-af", af, "-c:v", "libx264", "-preset", "veryfast",
        "-crf", "20", "-c:a", "aac", "-ar", "48000", "-ac", "2", output,
    ]
    run(command)


def _concat(clips: list[Path], output: Path) -> None:
    ffmpeg = require_command("ffmpeg")
    list_file = output.with_suffix(".txt")
    list_file.write_text(
        "".join(f"file '{str(path).replace(chr(39), chr(39) * 2)}'\n" for path in clips),
        encoding="utf-8",
    )
    run([ffmpeg, "-y", "-f", "concat", "-safe", "0", "-i", list_file, "-c", "copy", output])


def _finish(project: Project, source: Path) -> None:
    ffmpeg = require_command("ffmpeg")
    project.output.parent.mkdir(parents=True, exist_ok=True)
    command: list[str | Path] = [ffmpeg, "-y", "-i", source]
    audio_inputs = 0
    if project.narration:
        command += ["-i", project.narration]
        audio_inputs += 1
    if project.music:
        command += ["-stream_loop", "-1", "-i", project.music]
        audio_inputs += 1

    vf: list[str] = []
    if project.subtitles:
        subtitle_path = str(project.subtitles).replace("\\", "/").replace(":", "\\:").replace("'", "\\'")
        vf.append(f"subtitles='{subtitle_path}'")
    if project.title:
        safe_title = project.title.replace("'", "\\'").replace(":", "\\:")
        vf.append(
            "drawtext=text='" + safe_title + "':fontsize=56:fontcolor=white:"
            "box=1:boxcolor=black@0.55:boxborderw=18:x=(w-text_w)/2:y=h*0.08:enable='lt(t,4)'"
        )
    if vf:
        command += ["-vf", ",".join(vf)]

    if audio_inputs == 1:
        idx = 1
        volume = project.music_volume if project.music and not project.narration else 1.0
        command += ["-filter_complex", f"[{idx}:a]volume={volume}[extra];[0:a][extra]amix=inputs=2:duration=first[a]", "-map", "0:v", "-map", "[a]"]
    elif audio_inputs == 2:
        command += [
            "-filter_complex",
            f"[2:a]volume={project.music_volume}[music];[0:a][1:a][music]amix=inputs=3:duration=first:dropout_transition=2[a]",
            "-map", "0:v", "-map", "[a]",
        ]
    command += ["-c:v", "libx264", "-crf", "20", "-preset", "medium", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", project.output]
    run(command)


def render_project(project: Project, *, keep_temp: bool = False) -> Path:
    problems = validate_project(project)
    if problems:
        raise VideoForgeError("Project validation failed:\n- " + "\n- ".join(problems))
    require_command("ffmpeg")
    require_command("ffprobe")

    temp_context = tempfile.TemporaryDirectory(prefix="video-forge-")
    temp = Path(temp_context.name)
    prepared: list[Path] = []
    try:
        for index, clip in enumerate(project.clips):
            output = temp / f"clip-{index:04d}.mp4"
            _prepare_clip(clip, output, project)
            prepared.append(output)
        joined = temp / "joined.mp4"
        _concat(prepared, joined)
        _finish(project, joined)
        manifest = project.output.with_suffix(".manifest.json")
        manifest.write_text(json.dumps({"project": str(project.path), "output": str(project.output)}, indent=2), encoding="utf-8")
        return project.output
    finally:
        if keep_temp:
            temp_context.cleanup = lambda: None  # type: ignore[method-assign]
            print(f"Temporary files kept at {temp}")
        else:
            temp_context.cleanup()
