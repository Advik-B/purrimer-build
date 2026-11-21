"""Bugs found by running the components (scripts/showcase.py), pinned with checks that need no GUI toolkit."""

import re
from pathlib import Path

import pytest

from purrimer_build.cli import component_roots
from purrimer_build.components import discover

EXAMPLES = Path(__file__).resolve().parents[1] / "examples"
EXAMPLE_FILES = (
    "css.html",
    "svelte.svelte",
    "solid.tsx",
    "qtwidgets.py",
    "qtquick.qml",
    "avalonia.axaml",
    "slint.slint",
)


def test_qt_widgets_never_use_the_size_property(built: Path) -> None:
    # QWidget already has a "size" property, so setProperty("size", "small") is ignored and [size=...] never matches.
    for path in (built / "qtwidgets" / "purrimer_qt").rglob("*.py"):
        assert 'setProperty("size"' not in path.read_text(encoding="utf-8"), path
    for path in (built / "qtwidgets" / "purrimer_qt" / "qss").glob("*.qss"):
        assert "[size=" not in path.read_text(encoding="utf-8"), path


def test_avalonia_progress_fill_starts_at_zero_width(built: Path) -> None:
    # A Width transition from NaN stays NaN, so the fill never showed.
    text = (built / "avalonia" / "Purrimer" / "Themes" / "ProgressBar.axaml").read_text(encoding="utf-8")
    assert re.search(r'<Border Name="PART_Indicator" Width="0"', text)


def test_qml_popups_have_a_height(built: Path) -> None:
    # QtQuick.Templates leaves a Popup's implicit size to the style; without one the Dialog was 0 high.
    for path in (built / "qtquick" / "Purrimer").glob("*.qml"):
        text = path.read_text(encoding="utf-8")
        if re.search(r"^T\.Popup \{", text, re.M):
            assert re.search(r"^    implicitHeight:", text, re.M), path


def test_qml_text_fields_draw_their_placeholder(built: Path) -> None:
    # T.TextField does not draw placeholderText; each template has to.
    for name in ("TextField", "SearchBar"):
        text = (built / "qtquick" / "Purrimer" / f"{name}.qml").read_text(encoding="utf-8")
        assert re.search(r"text: \w+\.placeholderText", text), name


def test_qml_does_not_find_handlers_through_children(built: Path) -> None:
    # Pointer handlers are not Items, so children[n] never reaches them.
    text = (built / "qtquick" / "Purrimer" / "BottomSheet.qml").read_text(encoding="utf-8")
    assert "children[1]" not in text
    assert "onOpened: y = Qt.binding" in text


def test_slint_layout_components_do_not_lay_out_input_areas(built: Path) -> None:
    # A TouchArea or FocusScope directly inside a layout gets a zero-width cell: clicks miss and the row shifts.
    for path in (built / "slint" / "components").glob("*.slint"):
        text = path.read_text(encoding="utf-8")
        if re.search(r"export component \w+ inherits (Horizontal|Vertical)Layout", text):
            assert not re.search(r"^    (\w+ := )?(TouchArea|FocusScope) \{", text, re.M), path


def test_list_item_padding_stays_inside_its_width(built: Path) -> None:
    css = (built / "css" / "purrimer-components.css").read_text(encoding="utf-8")
    rule = re.search(r"\.pm-list-item \{(.*?)\}", css, re.S)
    assert rule and "box-sizing: border-box" in rule.group(1)


@pytest.mark.parametrize(
    ("name", "base", "default"),
    [("Button", "pm-button", "default"), ("IconButton", "pm-icon-button", "default"), ("Chip", "pm-chip", "accent")],
)
def test_web_default_variants_add_no_undefined_modifier(built: Path, name: str, base: str, default: str) -> None:
    # pm-button--default and friends have no CSS rule: the default look is the base class, so skip the modifier.
    css = (built / "css" / "purrimer-components.css").read_text(encoding="utf-8")
    assert f".{base}--{default}" not in css
    for target, ext in (("svelte", "svelte"), ("solid", "tsx")):
        text = (built / target / "components" / f"{name}.{ext}").read_text(encoding="utf-8")
        assert f'!== "{default}" && `{base}--$' in text, f"{target}/{name}"


@pytest.mark.parametrize("comp", [c.name for c in discover(component_roots([]))])
def test_every_component_has_an_example_per_target(comp: str) -> None:
    folder = EXAMPLES / comp
    assert (folder / "example.toml").is_file(), comp
    for name in EXAMPLE_FILES:
        assert (folder / name).is_file(), f"{comp}/{name}"
