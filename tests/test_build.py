import compileall
import json
import re
from pathlib import Path

import jinja2
import pytest

from purrimer_build.engine import GENERATED_NOTE, checked
from purrimer_build.model import Tokens
from purrimer_build.naming import kebab, snake

from .conftest import TOKENS
from .test_components import CORE_AND_MOBILE


def test_targets_write_their_entry_files(built: Path) -> None:
    for rel in [
        "css/purrimer.css",
        "css/purrimer-components.css",
        "css/purrimer-classless.css",
        "svelte/index.ts",
        "solid/index.ts",
        "qtwidgets/purrimer_qt/__init__.py",
        "qtwidgets/purrimer_qt/qss/purrimer-blanc.qss",
        "qtquick/Purrimer/qmldir",
        "avalonia/Purrimer/Purrimer.axaml",
        "avalonia/Purrimer/Controls.axaml",
        "slint/purrimer.slint",
        "slint/purrimer-components.slint",
    ]:
        assert (built / rel).is_file(), rel


@pytest.mark.parametrize("name", sorted(CORE_AND_MOBILE))
def test_component_files_for_every_target(built: Path, name: str) -> None:
    assert (built / "svelte" / "components" / f"{name}.svelte").is_file()
    assert (built / "solid" / "components" / f"{name}.tsx").is_file()
    assert (built / "qtwidgets" / "purrimer_qt" / "components" / f"{snake(name)}.py").is_file()
    assert (built / "qtquick" / "Purrimer" / f"{name}.qml").is_file()
    assert (built / "avalonia" / "Purrimer" / "Themes" / f"{name}.axaml").is_file()
    assert (built / "slint" / "components" / f"{kebab(name)}.slint").is_file()


def test_generated_files_carry_the_note(built: Path) -> None:
    for path in built.rglob("*"):
        if path.suffix in {".css", ".ts", ".tsx", ".svelte", ".py", ".qml", ".axaml", ".cs", ".slint", ".qss"}:
            assert GENERATED_NOTE in path.read_text(encoding="utf-8"), path


def test_no_template_syntax_leaks(built: Path) -> None:
    for path in built.rglob("*"):
        if path.is_file() and path.suffix not in {".ttf", ".woff2", ".svg"}:
            text = path.read_text(encoding="utf-8")
            assert "{%" not in text and "{##" not in text, path


def test_generated_python_compiles(built: Path) -> None:
    assert compileall.compile_dir(str(built / "qtwidgets"), quiet=1)


def test_css_braces_balance(built: Path) -> None:
    for path in (built / "css").glob("*.css"):
        text = path.read_text(encoding="utf-8")
        assert text.count("{") == text.count("}"), path


def test_every_theme_gets_a_stylesheet(built: Path) -> None:
    themes = Tokens.load(TOKENS).themes
    for theme in themes:
        assert (built / "qtwidgets" / "purrimer_qt" / "qss" / f"purrimer-{theme}.qss").is_file()


def test_qt_tokens_json_parses(built: Path) -> None:
    data = json.loads((built / "qtwidgets" / "qt_tokens.json").read_text(encoding="utf-8"))
    assert data


def test_unknown_token_fails_the_render() -> None:
    tokens = Tokens.load(TOKENS)
    env = jinja2.Environment(undefined=jinja2.StrictUndefined)
    env.filters["tok"] = checked(tokens, lambda n: n)
    assert env.from_string('{{ "bgColor-default" | tok }}').render() == "bgColor-default"
    with pytest.raises(KeyError):
        env.from_string('{{ "bgColor-missing" | tok }}').render()


def _selectors(css: str) -> list[str]:
    """Selectors of every style rule, with comments, at-rule preludes and declarations dropped."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r'url\("[^"]*"\)', "", css)
    selectors = []
    for prelude in re.findall(r"([^{}]+)\{", css):
        prelude = prelude.strip()
        if prelude.startswith("@") or re.fullmatch(r"(from|to|\d+%)(\s*,\s*(from|to|\d+%))*", prelude):
            continue
        selectors += [s.strip() for s in prelude.split(",") if s.strip()]
    return selectors


def test_classless_css_uses_no_classes(built: Path) -> None:
    selectors = _selectors((built / "css" / "purrimer-classless.css").read_text(encoding="utf-8"))
    assert selectors
    assert not [s for s in selectors if re.search(r"\.[a-zA-Z_-]", s)]


def test_class_based_css_leaves_plain_elements_alone(built: Path) -> None:
    # purrimer.css and purrimer-components.css only style their own classes, the theme roots and @font-face.
    for name in ("purrimer.css", "purrimer-components.css"):
        for selector in _selectors((built / "css" / name).read_text(encoding="utf-8")):
            allowed = selector.startswith((":root", "[data-theme")) or re.search(r"\.(pm-|text-)", selector)
            assert allowed, f"{name}: {selector}"
