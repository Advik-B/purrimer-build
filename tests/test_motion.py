"""The motion catalog: one source for the web keyframes and the native tables."""

import re
from pathlib import Path

import pytest

from purrimer_build.model import Tokens
from purrimer_build.motion import KINDS, Catalog, css_value, sample

from .conftest import TOKENS


@pytest.fixture(scope="module")
def catalog() -> Catalog:
    return Catalog.load()


@pytest.fixture(scope="module")
def tokens() -> Tokens:
    return Tokens.load(TOKENS)


def test_catalog_covers_the_design_system(catalog: Catalog) -> None:
    # animations.md: 14 entrances, 12 exits, 14 attention, 6 feedback, 7 ambient, 3 loading here (yarn-roll sits with
    # ambient), 19 choreography presets.
    counts = {}
    for a in catalog.anims.values():
        counts[a.cat] = counts.get(a.cat, 0) + 1
    assert counts == {
        "enter": 14,
        "exit": 12,
        "attention": 14,
        "feedback": 6,
        "ambient": 8,
        "loading": 3,
        "choreography": 19,
    }


def test_every_entry_has_a_class_and_keyframes(built: Path, catalog: Catalog) -> None:
    css = (built / "css" / "purrimer.css").read_text(encoding="utf-8")
    frames = set(re.findall(r"@keyframes\s+([\w-]+)", css))
    for name, anim in catalog.anims.items():
        assert re.search(rf"\.pm-m-{name}\s*\{{", css), name
        if anim.css == "auto" and anim.use is None:
            assert f"pm-{name}" in frames, name
            if anim.kinded:
                assert f"pm-{name}-playful" in frames, name
    for kind_var in ("--pm-m-p-dialog", "--pm-m-k-land"):
        assert kind_var in css


def test_aliases_follow_the_kind(catalog: Catalog) -> None:
    dialog = catalog.anims["dialog"]
    assert dialog.source("sleepy") == "rise"
    assert dialog.source("playful") == "pounce"
    assert dialog.source("reduced") == "rise"


def test_css_values_carry_units() -> None:
    assert css_value("dist", "px") == "var(--pm-m-dist)"
    assert css_value("dist * -1", "px") == "calc(var(--pm-m-dist) * -1)"
    assert css_value("3 * amp + 1", "px") == "calc(3px * var(--pm-m-amp) + 1px)"
    assert css_value("amp * -0.6", "px") == "calc(var(--pm-m-amp) * -0.6px)"
    assert css_value("(sx + 1) / 2", None) == "calc((var(--pm-m-sx) + 1) / 2)"
    assert css_value("0", "deg") == "0deg"


@pytest.mark.parametrize("kind", KINDS)
def test_tables_resolve_for_every_kind(catalog: Catalog, tokens: Tokens, kind: str) -> None:
    table = catalog.table(tokens, kind)
    assert set(table) == set(catalog.anims)
    for name, entry in table.items():
        assert entry["dur"] > 0, name
        for ch, track in entry["tracks"].items():
            assert track[0][0] == 0 and track[-1][0] == 1, (name, ch)


def test_reference_samples(catalog: Catalog, tokens: Tokens) -> None:
    easings = catalog.easings(tokens)
    sleepy = catalog.table(tokens, "sleepy")
    playful = catalog.table(tokens, "playful")
    start = sample(sleepy, easings, "rise", 0)
    assert (start["opacity"], start["ty"], start["blur"]) == (0, 8, 6)
    end = sample(sleepy, easings, "rise", 1)
    assert (end["opacity"], end["ty"], end["blur"]) == (1, 0, 0)
    assert sample(playful, easings, "pounce", 0)["sx"] == 0.5
    # Reverse presets play their source backwards.
    assert sample(sleepy, easings, "backdrop-out", 0)["opacity"] == 1
    assert sample(sleepy, easings, "backdrop-out", 1)["opacity"] == 0
    # Playful springs overshoot; opacity stays clamped like CSS.
    mid = [sample(playful, easings, "rise", t / 20) for t in range(21)]
    assert min(s["ty"] for s in mid) < 0
    assert max(s["opacity"] for s in mid) == 1


def test_reduced_motion_only_fades(catalog: Catalog, tokens: Tokens) -> None:
    easings = catalog.easings(tokens)
    reduced = catalog.table(tokens, "reduced")
    for name in ("rise", "pounce", "slink-left", "tumble", "uncurl"):
        s = sample(reduced, easings, name, 0)
        assert (s["tx"], s["ty"], s["rot"], s["sx"], s["blur"]) == (0, 0, 0, 1, 0), name
        assert reduced[name]["dur"] == 200


def test_native_targets_carry_the_catalog(built: Path, catalog: Catalog) -> None:
    files = {
        "qtwidgets/purrimer_qt/motion.py": "CATALOG = {",
        "qtquick/Purrimer/PmMotion.js": "var CATALOG = {",
        "avalonia/Purrimer/PurrimerThemes.cs": "public static class PurrimerMotionCatalog",
        "slint/motion.slint": "export global PmMotionCatalog",
    }
    for rel, marker in files.items():
        text = (built / rel).read_text(encoding="utf-8")
        assert marker in text, rel
        for name in catalog.anims:
            assert f'"{name}"' in text or f"'{name}'" in text, (rel, name)
    assert "PmMotionPlayer 1.0 PmMotionPlayer.qml" in (built / "qtquick/Purrimer/qmldir").read_text(encoding="utf-8")
    assert "PmMotionCatalog" in (built / "slint/purrimer-components.slint").read_text(encoding="utf-8")
