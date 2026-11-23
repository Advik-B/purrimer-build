"""Component registry.

A component is a folder holding component.toml and one Jinja2 template per layer it supports:

    templates/components/Button/
        component.toml        name, group, summary, props
        web.css.j2            styles shared by the CSS, Svelte and Solid targets
        svelte.svelte.j2      Svelte 5 component
        solid.tsx.j2          Solid 2 component
        qml.qml.j2            Qt Quick component
        slint.slint.j2        Slint component
        avalonia.axaml.j2     Avalonia control theme
        avalonia.cs.j2        Avalonia control class, for controls Avalonia lacks
        pyside.py.j2          PySide6 widget

Adding a component means adding a folder. Missing layers are reported by `purrimer components`.
"""

from __future__ import annotations

import re
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

from .naming import kebab, snake

LAYERS = {
    "web.css": "web.css.j2",
    "svelte": "svelte.svelte.j2",
    "solid": "solid.tsx.j2",
    "qml": "qml.qml.j2",
    "slint": "slint.slint.j2",
    "avalonia.axaml": "avalonia.axaml.j2",
    "avalonia.cs": "avalonia.cs.j2",
    "pyside": "pyside.py.j2",
}

# Layers each target needs for a component to count as covered there.
TARGET_LAYERS = {
    "css": ("web.css",),
    "svelte": ("web.css", "svelte"),
    "solid": ("web.css", "solid"),
    "qtwidgets": ("pyside",),
    "qtquick": ("qml",),
    "avalonia": ("avalonia.axaml",),
    "slint": ("slint",),
}


@dataclass(frozen=True)
class Prop:
    name: str
    type: str
    default: object = None
    doc: str = ""
    values: tuple = ()


@dataclass
class Component:
    name: str
    group: str
    summary: str
    folder: Path
    props: list[Prop] = field(default_factory=list)
    spec: dict = field(default_factory=dict)

    def has(self, layer: str) -> bool:
        return (self.folder / LAYERS[layer]).exists()

    def template(self, layer: str) -> str:
        """Template name relative to the components loader root."""
        return f"{self.folder.name}/{LAYERS[layer]}"

    def covers(self, target: str) -> bool:
        return all(self.has(layer) for layer in TARGET_LAYERS[target])

    def uses(self, names: set[str]) -> set[str]:
        """Other components this one's templates import or instantiate, so a subset build can include them."""
        found: set[str] = set(self.spec.get("requires", []))
        by_snake = {snake(n): n for n in names}
        by_kebab = {kebab(n): n for n in names}
        for layer, filename in LAYERS.items():
            path = self.folder / filename
            if not path.exists():
                continue
            text = path.read_text(encoding="utf-8")
            if layer in ("svelte", "solid"):
                found |= {m for m in re.findall(r'from "\./(\w+)(?:\.svelte)?"', text) if m in names}
            elif layer == "pyside":
                found |= {by_snake[m] for m in re.findall(r"from \.(\w+) import", text) if m in by_snake}
            elif layer == "slint":
                found |= {by_kebab[m] for m in re.findall(r'from "([\w-]+)\.slint"', text) if m in by_kebab}
            elif layer == "qml":
                found |= {m for m in re.findall(r"^\s*(\w+) \{", text, re.M) if m in names}
            elif layer.startswith("avalonia"):
                found |= {m for m in re.findall(r"pm:(\w+)", text) if m in names}
                found |= {m for m in re.findall(r"\b(\w+)\.\w+Event\b", text) if m in names}
        found.discard(self.name)
        return found


def load_component(folder: Path) -> Component:
    spec = tomllib.loads((folder / "component.toml").read_text(encoding="utf-8"))
    props = []
    for name, p in spec.get("props", {}).items():
        props.append(
            Prop(name, p.get("type", "string"), p.get("default"), p.get("doc", ""), tuple(p.get("values", ())))
        )
    name = spec.get("name", folder.name)
    if name != folder.name:
        raise ValueError(f"{folder}: component name {name!r} must match its folder name")
    return Component(name, spec.get("group", "Other"), spec.get("summary", ""), folder, props, spec)


def with_dependencies(chosen: list[Component], everything: list[Component]) -> list[Component]:
    """The chosen components plus every component they use, directly or not, in registry order."""
    by_name = {c.name: c for c in everything}
    names = set(by_name)
    wanted = {c.name for c in chosen}
    queue = list(wanted)
    while queue:
        for dep in by_name[queue.pop()].uses(names):
            if dep not in wanted:
                wanted.add(dep)
                queue.append(dep)
    return [c for c in everything if c.name in wanted]


def discover(roots: list[Path]) -> list[Component]:
    """Components from every root; a later root overrides an earlier one with the same name."""
    found: dict[str, Component] = {}
    for root in roots:
        if not root.exists():
            continue
        for folder in sorted(p for p in root.iterdir() if (p / "component.toml").exists()):
            comp = load_component(folder)
            found[comp.name] = comp
    return sorted(found.values(), key=lambda c: (c.spec.get("order", 1000), c.name))
