from pathlib import Path
import pytest
from agentbroko.skills_installer import install_skills, SKILL_REGISTRY
from agentbroko.cli import main

def test_install_all_skills(tmp_path: Path):
    created = install_skills(tmp_path)
    assert len(created) >= 5
    assert (tmp_path / ".agents" / "skills" / "video-forge" / "SKILL.md").exists()
    assert (tmp_path / ".agents" / "skills" / "video-forge" / "templates" / "stories_of_the_ummah" / "universal_story.json").exists()
    assert (tmp_path / ".agents" / "skills" / "video-edit" / "SKILL.md").exists()
    assert (tmp_path / ".agents" / "skills" / "pdf-playbook" / "SKILL.md").exists()
    assert (tmp_path / ".agents" / "skills" / "pdf" / "SKILL.md").exists()
    assert (tmp_path / ".agents" / "AGENTS.md").exists()
    assert (tmp_path / ".cursorrules").exists()
    assert (tmp_path / "CLAUDE.md").exists()

def test_install_single_skill(tmp_path: Path):
    created = install_skills(tmp_path, skill_name="video-forge")
    assert (tmp_path / ".agents" / "skills" / "video-forge" / "SKILL.md").exists()
    assert not (tmp_path / ".agents" / "skills" / "pdf-playbook" / "SKILL.md").exists()
    
    # Check that AGENTS.md contains video-forge
    agents_md = (tmp_path / ".agents" / "AGENTS.md").read_text(encoding="utf-8")
    assert "Video Forge" in agents_md
    assert "Agent Stuck" in agents_md

def test_install_invalid_skill_raises(tmp_path: Path):
    with pytest.raises(ValueError, match="Unknown skill"):
        install_skills(tmp_path, skill_name="non-existent-skill")

def test_cli_add_single_skill(tmp_path: Path):
    result = main(["add", "pdf-playbook", str(tmp_path)])
    assert result == 0
    assert (tmp_path / ".agents" / "skills" / "pdf-playbook" / "SKILL.md").exists()

def test_cli_init_command(tmp_path: Path):
    result = main(["init", str(tmp_path)])
    assert result == 0
    assert (tmp_path / ".agents" / "skills" / "video-forge" / "SKILL.md").exists()

def test_standard_skill_packaging_exists():
    skill_dir = Path(__file__).resolve().parents[1] / "skills" / "video-forge"
    assert (skill_dir / "SKILL.md").exists()
    assert "name: video-forge" in (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    assert "description:" in (skill_dir / "SKILL.md").read_text(encoding="utf-8")

    optional_skill_dir = Path(__file__).resolve().parents[1] / "skills" / "video-edit"
    assert (optional_skill_dir / "SKILL.md").exists()
    assert "name: video-edit" in (optional_skill_dir / "SKILL.md").read_text(encoding="utf-8")

    root_manifest = Path(__file__).resolve().parents[1] / "agentbroko.json"
    assert root_manifest.exists()
    text = root_manifest.read_text(encoding="utf-8")
    assert '"name": "video-forge"' in text
    assert '"name": "video-edit"' in text
    assert '"skills":' in text


def test_cli_search_lists_video_skill(capsys):
    assert main(["search", "video"]) == 0
    captured = capsys.readouterr()
    assert "video-forge" in captured.out.lower()
    assert "video" in captured.out.lower()


def test_cli_guide_and_skills_menu(capsys):
    assert main(["guide"]) == 0
    captured = capsys.readouterr()
    assert "AGENTBROKO AI AGENT INSTRUCTION" in captured.out

    assert main(["skills"]) == 0
    captured = capsys.readouterr()
    assert "AgentBroko Autonomous AI Skills Hub" in captured.out
