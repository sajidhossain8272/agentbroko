from video_forge.templates import available_story_templates, load_story_template
from pathlib import Path


def test_ummah_templates_are_reusable_and_audio_guided():
    names = available_story_templates()
    assert {"three_men_in_cave", "mercy_to_a_dog", "generic_episode"}.issubset(names)

    template = load_story_template("three_men_in_cave")
    assert template["video"]["aspect"] == "9:16"
    assert len(template["scenes"]) >= 5
    assert template["source"]
    assert set(template["audio"]) == {"narration", "music", "mix"}

    skill_templates = Path(__file__).resolve().parents[1] / "skills" / "video-forge" / "templates" / "stories_of_the_ummah"
    assert (skill_templates / "three_men_in_cave.json").exists()
    assert (skill_templates / "mercy_to_a_dog.json").exists()
    assert (skill_templates / "generic_episode.json").exists()