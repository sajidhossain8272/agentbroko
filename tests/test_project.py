import json

from video_forge.project import load_project, validate_project


def test_load_and_validate_project(tmp_path):
    media = tmp_path / "clip.mp4"
    media.touch()
    path = tmp_path / "project.json"
    path.write_text(json.dumps({"clips": [{"source": "clip.mp4"}]}), encoding="utf-8")
    project = load_project(path)
    assert project.clips[0].source == media.resolve()
    assert validate_project(project) == []

