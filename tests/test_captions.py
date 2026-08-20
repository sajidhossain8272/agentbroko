from video_forge.captions import text_to_srt


def test_text_to_srt(tmp_path):
    output = tmp_path / "captions.srt"
    text_to_srt("one two three four five", output, words_per_caption=3, seconds_per_caption=2)
    content = output.read_text(encoding="utf-8")
    assert "00:00:00,000 --> 00:00:02,000" in content
    assert "one two three" in content
    assert "00:00:02,000 --> 00:00:04,000" in content

