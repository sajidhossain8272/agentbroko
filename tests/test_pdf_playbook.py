from pathlib import Path
import pytest
from pdf_playbook.generator import BRAND, DISCLAIMER, generate_playbook

def test_generates_pdf(tmp_path: Path):
    output = generate_playbook(tmp_path / "guide.pdf", {"title": "Test Guide", "audience": "Developers", "topic": "Build safely"})
    data = output.read_bytes()
    assert data.startswith(b"%PDF")
    assert len(data) > 20_000

def test_free_edition_rejects_brand_removal(tmp_path: Path):
    with pytest.raises(ValueError, match="premium"):
        generate_playbook(tmp_path / "guide.pdf", remove_branding=True)

def test_required_legal_copy_is_defined():
    assert "AgentBroko" in BRAND
    assert "solely responsible" in DISCLAIMER
