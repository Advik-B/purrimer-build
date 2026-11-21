"""Run every example under examples/ on its target, screenshot it, and generate the docs.

    uv run scripts/showcase.py build                 # purrimer build -> showcase/dist
    uv run scripts/showcase.py run --targets all     # render, check, screenshot -> showcase/out/<target>/
    uv run scripts/showcase.py collect DIR           # CI: copy changed screenshots from DIR to docs/screenshots/
    uv run scripts/showcase.py docs                  # docs/components/*.md and the README gallery

`run` exits non-zero when an example is missing, fails its target's checks, logs a warning or error while rendering,
or produces a blank screenshot. Only CI runs `collect` and commits docs/screenshots/; local runs write showcase/out/.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from purrimer_build.cli import component_roots  # noqa: E402
from purrimer_build.cli import main as purrimer  # noqa: E402
from purrimer_build.components import Component, discover  # noqa: E402

EXAMPLES = ROOT / "examples"
SHOWCASE = ROOT / "showcase"
DIST = SHOWCASE / "dist"
OUT = SHOWCASE / "out"
WEB = SHOWCASE / "web"
SCREENSHOTS = ROOT / "docs" / "screenshots"
DOCS = ROOT / "docs" / "components"
README = ROOT / "README.md"

TARGETS = ("css", "classless", "svelte", "solid", "qtwidgets", "qtquick", "avalonia", "slint")
WEB_TARGETS = ("css", "classless", "svelte", "solid")
# Only components that map onto plain HTML elements have a classless example.
OPTIONAL_TARGETS = ("classless",)
THEMES = ("blanc", "noir")
THEME_LABELS = {"blanc": "Blanc", "noir": "Noir", "light": "Latte", "dark": "Mocha"}
SCALE = 2
PADDING = 16

# Example file, code-fence language and heading for each target.
FILES = {
    "css": ("css.html", "html", "CSS"),
    "classless": ("classless.html", "html", "CSS, classless"),
    "svelte": ("svelte.svelte", "svelte", "Svelte"),
    "solid": ("solid.tsx", "tsx", "Solid"),
    "qtwidgets": ("qtwidgets.py", "python", "Qt Widgets (PySide6)"),
    "qtquick": ("qtquick.qml", "qml", "Qt Quick"),
    "avalonia": ("avalonia.axaml", "xml", "Avalonia"),
    "slint": ("slint.slint", "slint", "Slint"),
}


@dataclass
class Example:
    component: Component
    folder: Path
    width: int
    height: int
    caption: str
    bleed: bool

    @property
    def name(self) -> str:
        return self.component.name

    def file(self, target: str) -> Path:
        return self.folder / FILES[target][0]

    def has(self, target: str) -> bool:
        return self.file(target).is_file()


def load_examples(only: set[str] | None = None) -> tuple[list[Example], list[str]]:
    examples, problems = [], []
    for comp in discover(component_roots([])):
        if only and comp.name not in only:
            continue
        folder = EXAMPLES / comp.name
        if not (folder / "example.toml").is_file():
            problems.append(f"{comp.name}: no examples/{comp.name}/example.toml")
            continue
        spec = tomllib.loads((folder / "example.toml").read_text(encoding="utf-8"))
        width, height = (int(v) for v in spec.get("size", "360x120").split("x"))
        examples.append(Example(comp, folder, width, height, spec.get("caption", ""), spec.get("bleed", False)))
    return examples, problems


def run(cmd: list[str], cwd: Path = ROOT, env: dict | None = None) -> bool:
    exe = shutil.which(cmd[0]) or cmd[0]
    print("$", " ".join(cmd), flush=True)
    return subprocess.run([exe, *cmd[1:]], cwd=cwd, env={**os.environ, **(env or {})}).returncode == 0


def manifest(examples: list[Example], targets: list[str], themes: list[str], name: str) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"manifest-{name}.json"
    data = {
        "root": str(ROOT),
        "dist": str(DIST),
        "out": str(OUT),
        "scale": SCALE,
        "padding": PADDING,
        "targets": targets,
        "themes": themes,
        "components": [
            {
                "name": e.name,
                "width": e.width,
                "height": e.height,
                "bleed": e.bleed,
                "files": {t: str(e.file(t)) for t in targets if e.has(t)},
            }
            for e in examples
        ],
    }
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return path


# Harnesses


def stage_web(examples: list[Example]) -> None:
    """Copy the generated web code and the web examples into showcase/web/stage/, as an app would."""
    stage = WEB / "stage"
    if stage.exists():
        shutil.rmtree(stage)
    for part in ("css", "svelte", "solid", "fonts/woff2"):
        shutil.copytree(DIST / part, stage / "purrimer" / part)
    for e in examples:
        dest = stage / "examples" / e.name
        dest.mkdir(parents=True)
        for target in WEB_TARGETS:
            if e.has(target):
                shutil.copyfile(e.file(target), dest / FILES[target][0])


def run_web(examples: list[Example], targets: list[str], themes: list[str]) -> bool:
    if not (WEB / "node_modules").is_dir() and not run(["npm", "ci"], cwd=WEB):
        return False
    stage_web(examples)
    ok = True
    if "svelte" in targets:
        ok &= run(["npm", "run", "check:svelte"], cwd=WEB)
    if "solid" in targets:
        ok &= run(["npm", "run", "check:solid"], cwd=WEB)
    ok &= run(["npm", "run", "check:harness"], cwd=WEB)
    if not run(["npm", "run", "build"], cwd=WEB):
        return False
    return run(["node", "shoot.ts", str(manifest(examples, targets, themes, "web"))], cwd=WEB) and ok


def run_qtwidgets(examples: list[Example], themes: list[str]) -> bool:
    script = SHOWCASE / "qt" / "run_widgets.py"
    env = {"QT_QPA_PLATFORM": "offscreen"}
    return run([sys.executable, str(script), str(manifest(examples, ["qtwidgets"], themes, "qtwidgets"))], env=env)


def run_qtquick(examples: list[Example], themes: list[str]) -> bool:
    qml = DIST / "qtquick"
    lint = [
        "pyside6-qmllint",
        "-I",
        str(qml),
        "--max-warnings",
        "0",
        *sorted(str(p) for p in (qml / "Purrimer").glob("*.qml")),
        *(str(e.file("qtquick")) for e in examples),
    ]
    ok = run(lint)
    script = SHOWCASE / "qt" / "run_quick.py"
    return run([sys.executable, str(script), str(manifest(examples, ["qtquick"], themes, "qtquick"))]) and ok


def run_avalonia(examples: list[Example], themes: list[str]) -> bool:
    project = SHOWCASE / "avalonia"
    if not run(["dotnet", "build", str(project), "-c", "Release", "-warnaserror", "-nologo", "-v", "q"]):
        return False
    path = manifest(examples, ["avalonia"], themes, "avalonia")
    return run(["dotnet", "run", "--project", str(project), "-c", "Release", "--no-build", "--", str(path)])


def run_slint(examples: list[Example], themes: list[str]) -> bool:
    script = SHOWCASE / "slint" / "run_slint.py"
    return run([sys.executable, str(script), str(manifest(examples, ["slint"], themes, "slint"))])


def blank_shots(examples: list[Example], targets: list[str], themes: list[str]) -> list[str]:
    """Screenshots that are missing or nearly one colour: the example rendered nothing."""
    from PIL import Image, ImageStat

    problems = []
    for target in targets:
        for e in (e for e in examples if e.has(target)):
            for theme in themes:
                path = OUT / target / f"{e.name}-{theme}.png"
                if not path.is_file():
                    problems.append(f"{target}/{e.name}/{theme}: no screenshot")
                    continue
                with Image.open(path) as img:
                    rgb = img.convert("RGB")
                    spread = max(ImageStat.Stat(rgb).stddev)
                    colours = len(rgb.getcolors(maxcolors=1 << 20) or ())
                if spread < 2 or colours < 8:
                    problems.append(f"{target}/{e.name}/{theme}: blank screenshot ({colours} colours)")
    return problems


def cmd_build(args: argparse.Namespace) -> int:
    return purrimer(
        [
            "build",
            "--clean",
            "--out",
            str(DIST),
            "--tokens",
            str(ROOT / "tokens/tokens.json"),
            "--fonts",
            str(ROOT / "tokens/fonts"),
        ]
    )


def cmd_run(args: argparse.Namespace) -> int:
    targets = list(TARGETS) if args.targets == "all" else [t.strip() for t in args.targets.split(",") if t.strip()]
    unknown = [t for t in targets if t not in TARGETS]
    if unknown:
        print(f"Unknown targets: {', '.join(unknown)}", file=sys.stderr)
        return 2
    themes = [t.strip() for t in args.themes.split(",")]
    only = {n.strip() for n in args.only.split(",")} if args.only else None
    if not DIST.is_dir():
        print("Run `scripts/showcase.py build` first.", file=sys.stderr)
        return 2
    examples, problems = load_examples(only)
    for e in examples:
        for t in targets:
            if t not in OPTIONAL_TARGETS and not e.has(t):
                problems.append(f"{e.name}: no {t} example ({e.file(t).relative_to(ROOT).as_posix()})")
    examples = [e for e in examples if all(e.has(t) for t in targets if t not in OPTIONAL_TARGETS)]
    for t in targets:
        if (OUT / t).exists():
            shutil.rmtree(OUT / t)

    failed = []
    web = [t for t in targets if t in WEB_TARGETS]
    if web and not run_web(examples, web, themes):
        failed.append("/".join(web))
    runners = {"qtwidgets": run_qtwidgets, "qtquick": run_qtquick, "avalonia": run_avalonia, "slint": run_slint}
    for t in targets:
        if t in runners and not runners[t](examples, themes):
            failed.append(t)
    problems += blank_shots(examples, targets, themes)
    if failed:
        problems.append(f"failed: {', '.join(failed)}")
    if problems:
        print("\nShowcase problems:\n  " + "\n  ".join(problems), file=sys.stderr)
        return 1
    print(f"\n{len(examples)} components x {len(targets)} targets x {len(themes)} themes rendered cleanly.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="showcase", description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("build", help="Build every target into showcase/dist.").set_defaults(func=cmd_build)
    r = sub.add_parser("run", help="Render and screenshot the examples.")
    r.add_argument("--targets", default="all")
    r.add_argument("--themes", default=",".join(THEMES))
    r.add_argument("--only", default="", help="Comma-separated component names.")
    r.set_defaults(func=cmd_run)
    c = sub.add_parser("collect", help="Copy new screenshots into docs/screenshots, skipping ones that look the same.")
    c.add_argument("source", type=Path, help="Folder with one subfolder of PNGs per target.")
    c.set_defaults(func=cmd_collect)
    sub.add_parser("docs", help="Write docs/components/*.md and the README gallery.").set_defaults(func=cmd_docs)
    args = parser.parse_args(argv)
    return args.func(args)


# Collect

# GPU rasterisers can flip a channel by one on anti-aliased edges between runs; ignore that, so an unchanged
# component never produces a commit.
NOISE = 2


def same_picture(a: Path, b: Path) -> bool:
    from PIL import Image, ImageChops

    with Image.open(a) as x, Image.open(b) as y:
        if x.size != y.size:
            return False
        diff = ImageChops.difference(x.convert("RGBA"), y.convert("RGBA"))
        return max(high for _, high in diff.getextrema()) <= NOISE


def cmd_collect(args: argparse.Namespace) -> int:
    source: Path = args.source
    new = {p.relative_to(source) for p in source.glob("*/*.png")}
    if not new:
        print(f"No screenshots in {source}.", file=sys.stderr)
        return 1
    copied = kept = removed = 0
    for rel in sorted(new):
        dest = SCREENSHOTS / rel
        if dest.is_file() and same_picture(source / rel, dest):
            kept += 1
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source / rel, dest)
        copied += 1
    for old in SCREENSHOTS.glob("*/*.png"):
        if old.relative_to(SCREENSHOTS) not in new:
            old.unlink()
            removed += 1
    print(f"{copied} screenshots updated, {kept} unchanged, {removed} removed.")
    return 0


# Docs

GENERATED = "<!-- Generated by scripts/showcase.py from examples/ and component.toml. Do not edit by hand. -->"
GALLERY_START = "<!-- gallery:start -->"
GALLERY_END = "<!-- gallery:end -->"
GALLERY_TARGET = "css"
GALLERY_COLUMNS = 3


def shot(target: str, name: str, theme: str, base: str) -> str:
    return f"{base}/{target}/{name}-{theme}.png"


def images(e: Example, target: str, base: str, width: int) -> str:
    return " ".join(
        f'<img src="{shot(target, e.name, theme, base)}" width="{width}" alt="{e.name}, {FILES[target][2]}, '
        f'{THEME_LABELS[theme]}">'
        for theme in THEMES
    )


def prop_rows(comp: Component) -> list[str]:
    rows = ["| Prop | Type | Default | Values | Description |", "| --- | --- | --- | --- | --- |"]
    for p in comp.props:
        default = "" if p.default in ("", None, []) else f"`{json.dumps(p.default)}`"
        values = ", ".join(f"`{v}`" for v in p.values)
        rows.append(f"| `{p.name}` | {p.type} | {default} | {values} | {p.doc} |")
    return rows


def component_page(e: Example) -> str:
    comp = e.component
    width = min(e.width, 400)
    lines = [GENERATED, "", f"# {comp.name}", "", comp.summary, "", f"{comp.group} · [All components](README.md)", ""]
    if e.caption:
        lines += [e.caption, ""]
    if comp.props:
        lines += ["## Props", "", *prop_rows(comp), ""]
        lines += [
            "Names follow the web targets. Qt Widgets takes `snake_case` arguments, Qt Quick `camelCase` properties, "
            "Avalonia `PascalCase` properties and Slint `kebab-case` properties; each example below shows the "
            "spelling for its target.",
            "",
        ]
    lines += ["## Examples", ""]
    lines += [
        f"Each example is run as it is shown here, on every push, and the screenshots are taken from that run "
        f"(left {THEME_LABELS[THEMES[0]]}, right {THEME_LABELS[THEMES[1]]}).",
        "",
    ]
    for target in (t for t in TARGETS if e.has(t)):
        filename, lang, title = FILES[target]
        code = e.file(target).read_text(encoding="utf-8").rstrip()
        lines += [f"### {title}", "", images(e, target, "../screenshots", width), "", f"```{lang}", code, "```", ""]
    return "\n".join(lines)


def index_page(examples: list[Example]) -> str:
    lines = [GENERATED, "", "# Components", "", "[Back to the README](../../README.md)", ""]
    for group, members in grouped(examples):
        lines += [f"## {group}", "", "| Component | Summary |", "| --- | --- |"]
        lines += [f"| [{e.name}]({e.name}.md) | {e.component.summary} |" for e in members]
        lines.append("")
    return "\n".join(lines)


def grouped(examples: list[Example]) -> list[tuple[str, list[Example]]]:
    groups: dict[str, list[Example]] = {}
    for e in examples:
        groups.setdefault(e.component.group, []).append(e)
    return list(groups.items())


def gallery(examples: list[Example]) -> str:
    lines = [GALLERY_START, "", "<table>"]
    for i in range(0, len(examples), GALLERY_COLUMNS):
        lines.append("<tr>")
        for e in examples[i : i + GALLERY_COLUMNS]:
            src = shot(GALLERY_TARGET, e.name, THEMES[0], "docs/screenshots")
            lines.append(
                f'<td align="center" valign="top"><a href="docs/components/{e.name}.md">'
                f'<img src="{src}" width="240" alt="{e.name}"><br><b>{e.name}</b></a></td>'
            )
        lines.append("</tr>")
    lines += ["</table>", "", GALLERY_END]
    return "\n".join(lines)


def cmd_docs(args: argparse.Namespace) -> int:
    examples, problems = load_examples()
    if problems:
        print("\n".join(problems), file=sys.stderr)
        return 1
    DOCS.mkdir(parents=True, exist_ok=True)
    for e in examples:
        (DOCS / f"{e.name}.md").write_bytes((component_page(e) + "\n").encode())
    (DOCS / "README.md").write_bytes((index_page(examples) + "\n").encode())
    readme = README.read_text(encoding="utf-8")
    start, end = readme.find(GALLERY_START), readme.find(GALLERY_END)
    if start < 0 or end < start:
        print(f"README.md needs {GALLERY_START} and {GALLERY_END} markers.", file=sys.stderr)
        return 1
    updated = readme[:start] + gallery(examples) + readme[end + len(GALLERY_END) :]
    README.write_bytes(updated.encode())
    missing = sum(
        not (SCREENSHOTS / t / f"{e.name}-{th}.png").is_file()
        for e in examples
        for t in TARGETS
        if e.has(t)
        for th in THEMES
    )
    print(f"Wrote {len(examples)} component pages and the README gallery.")
    if missing:
        print(f"{missing} screenshots are not in docs/screenshots yet; CI adds them after the next push to master.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
