from pathlib import Path
from agentbroko.skills_installer import install_skills
from agentbroko.cli import main

def test_install_skills(tmp_path: Path):
    created = install_skills(tmp_path)
    assert len(created) >= 4
    assert (tmp_path / ".agents" / "skills" / "video-forge" / "SKILL.md").exists()
    assert (tmp_path / ".agents" / "skills" / "pdf-playbook" / "SKILL.md").exists()
    assert (tmp_path / ".agents" / "skills" / "pdf" / "SKILL.md").exists()
    assert (tmp_path / ".agents" / "AGENTS.md").exists()

def test_cli_init_command(tmp_path: Path):
    result = main(["init", str(tmp_path)])
    assert result == 0
    assert (tmp_path / ".agents" / "skills" / "video-forge" / "SKILL.md").exists()
