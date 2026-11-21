from purrimer_build.naming import camel, kebab, num, pascal, snake, words


def test_words_split_on_separators_and_case() -> None:
    assert words("bgColor-accent-muted") == ["bg", "Color", "accent", "muted"]
    assert words("text-mobile-largeTitle") == ["text", "mobile", "large", "Title"]


def test_case_conversions() -> None:
    assert camel("control-medium-size") == "controlMediumSize"
    assert pascal("borderRadius-large") == "BorderRadiusLarge"
    assert kebab("SegmentedControl") == "segmented-control"
    assert snake("IconButton") == "icon_button"
    assert snake("FAB") == "fab"


def test_num_trims_trailing_zeros() -> None:
    assert num(16.0) == "16"
    assert num(0.25) == "0.25"
    assert num(1 / 3) == "0.3333"
