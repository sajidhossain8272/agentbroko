from __future__ import annotations

import pytest
from agentbroko.cli import main as agentbroko_main
from video_forge.cli import main as video_forge_main


def test_agentbroko_cli_doctor(capsys):
    rc = agentbroko_main(["doctor"])
    assert rc == 0
    captured = capsys.readouterr()
    assert "AgentBroko System Diagnostics" in captured.out


def test_agentbroko_cli_version(capsys):
    rc = agentbroko_main(["--version"])
    assert rc == 0
    captured = capsys.readouterr()
    assert "1.4.2" in captured.out


def test_video_forge_cli_doctor(capsys):
    rc = video_forge_main(["doctor"])
    assert rc == 0
    captured = capsys.readouterr()
    assert "Video Forge System Diagnostics" in captured.out
