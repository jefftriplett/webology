from webology import __version__, build_card_content


def test_version():
    assert __version__


def test_build_card_content():
    content = build_card_content()
    assert "jefftriplett.com" in content.plain
