from pathlib import Path

from purrimer_build.cli import component_roots, main
from purrimer_build.components import discover
from purrimer_build.targets import ALL_TARGETS

CORE_AND_MOBILE = {
    "Icon",
    "Button",
    "IconButton",
    "TextField",
    "Checkbox",
    "Radio",
    "Toggle",
    "Select",
    "Label",
    "Chip",
    "Banner",
    "ProgressBar",
    "Card",
    "Dialog",
    "AppBar",
    "BottomNav",
    "BottomSheet",
    "ListItem",
    "ListSection",
    "FAB",
    "Snackbar",
    "SearchBar",
    "SegmentedControl",
    "Tabs",
    "Avatar",
}


def test_every_component_is_present() -> None:
    names = {c.name for c in discover(component_roots([]))}
    assert CORE_AND_MOBILE <= names


def test_every_component_covers_every_target() -> None:
    missing = [(c.name, t) for c in discover(component_roots([])) for t in ALL_TARGETS if not c.covers(t)]
    assert missing == []


def test_new_scaffolds_and_extra_roots_override(tmp_path: Path, capsys) -> None:
    assert main(["--components-dir", str(tmp_path), "new", "DatePicker", "--group", "Forms"]) == 0
    folder = tmp_path / "DatePicker"
    assert (folder / "component.toml").is_file()
    assert (folder / "web.css.j2").is_file()
    names = [c.name for c in discover(component_roots([tmp_path]))]
    assert names.count("DatePicker") == 1
    assert main(["--components-dir", str(tmp_path), "new", "DatePicker"]) == 1


def test_new_rejects_bad_names(tmp_path: Path) -> None:
    assert main(["--components-dir", str(tmp_path), "new", "date-picker"]) == 2
