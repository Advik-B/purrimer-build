import pytest

from purrimer_build.model import Tokens

from .conftest import TOKENS


@pytest.fixture(scope="module")
def tokens() -> Tokens:
    return Tokens.load(TOKENS)


def test_themes_in_order(tokens: Tokens) -> None:
    assert tokens.themes[0] == "blanc"
    assert set(tokens.dark_themes) <= set(tokens.themes)


def test_every_color_has_every_theme(tokens: Tokens) -> None:
    for name, by_theme in tokens.colors.items():
        assert set(by_theme) == set(tokens.themes), name


def test_kind_lookup(tokens: Tokens) -> None:
    assert tokens.kind("bgColor-default") == "color"
    assert tokens.kind("borderRadius-medium") == "length"
    assert tokens.kind("duration-fast") == "duration"
    assert tokens.kind("easing-standard") == "easing"
    assert tokens.kind("text-title-small") == "type"


def test_unknown_token_raises(tokens: Tokens) -> None:
    with pytest.raises(KeyError):
        tokens.kind("bgColor-nonexistent")
