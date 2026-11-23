"""Command line: `purrimer build`, `purrimer components`, `purrimer new`."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

from . import __version__
from .components import LAYERS, discover, with_dependencies
from .engine import Build, package_templates
from .fonts import build_static_fonts, copy_web_fonts
from .model import Tokens
from .targets import ALL_TARGETS, run_target

NATIVE_TARGETS = {"qtwidgets", "qtquick", "avalonia", "slint"}


def component_roots(extra: list[Path]) -> list[Path]:
    # Later roots win, so extra folders can override or add components.
    return [package_templates() / "components", *extra]


def cmd_build(args: argparse.Namespace) -> int:
    targets = ALL_TARGETS if args.targets == "all" else tuple(t.strip() for t in args.targets.split(",") if t.strip())
    unknown = [t for t in targets if t not in ALL_TARGETS]
    if unknown:
        print(f"Unknown targets: {', '.join(unknown)}. Choose from: {', '.join(ALL_TARGETS)}", file=sys.stderr)
        return 2
    roots = component_roots(args.components_dir)
    comps = discover(roots)
    if args.only:
        wanted = {n.strip() for n in args.only.split(",")}
        unknown_names = sorted(wanted - {c.name for c in comps})
        if unknown_names:
            print(f"Unknown components: {', '.join(unknown_names)}", file=sys.stderr)
            return 2
        chosen = [c for c in comps if c.name in wanted]
        comps = with_dependencies(chosen, comps)
        extra = [c.name for c in comps if c.name not in wanted]
        if extra:
            print(f"Also building what they use: {', '.join(extra)}")
    tokens = Tokens.load(args.tokens)
    out: Path = args.out
    if args.clean and out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True, exist_ok=True)
    build = Build(tokens=tokens, components=comps, out=out, component_roots=roots[::-1])
    build.web_fonts = copy_web_fonts(tokens, args.fonts, out / "fonts")
    if NATIVE_TARGETS.intersection(targets):
        build.static_fonts = build_static_fonts(tokens, args.fonts, out / "fonts")
    options = {"avalonia_namespace": args.avalonia_namespace, "avalonia_assembly": args.avalonia_assembly}
    for target in targets:
        before = len(build.written)
        run_target(build, target, options)
        print(f"{target}: {len(build.written) - before} files")
    print(f"{len(comps)} components, {len(build.written)} files in {out}")
    return 0


def cmd_components(args: argparse.Namespace) -> int:
    comps = discover(component_roots(args.components_dir))
    width = max((len(c.name) for c in comps), default=10)
    print("component".ljust(width), "group".ljust(12), *[t.ljust(9) for t in ALL_TARGETS])
    for c in comps:
        marks = [("yes" if c.covers(t) else "-").ljust(9) for t in ALL_TARGETS]
        print(c.name.ljust(width), c.group.ljust(12), *marks)
    covered = {t: sum(c.covers(t) for c in comps) for t in ALL_TARGETS}
    print("total".ljust(width), "".ljust(12), *[f"{covered[t]}/{len(comps)}".ljust(9) for t in ALL_TARGETS])
    return 0


def cmd_new(args: argparse.Namespace) -> int:
    name = args.name
    if not name[:1].isupper() or not name.isidentifier():
        print("Component names are PascalCase identifiers, such as DatePicker.", file=sys.stderr)
        return 2
    root = args.components_dir[-1] if args.components_dir else package_templates() / "components"
    folder = root / name
    if folder.exists():
        print(f"{folder} already exists.", file=sys.stderr)
        return 1
    folder.mkdir(parents=True)
    (folder / "component.toml").write_text(
        f'name = "{name}"\ngroup = "{args.group}"\nsummary = ""\norder = 1000\n\n[props]\n', encoding="utf-8"
    )
    layers = args.layers.split(",") if args.layers else [layer for layer in LAYERS if layer != "avalonia.cs"]
    for layer in layers:
        (folder / LAYERS[layer]).write_text("", encoding="utf-8")
    print(f"Created {folder} with {', '.join(LAYERS[layer] for layer in layers)}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="purrimer", description="Generate Purrimer styles and components from tokens.json."
    )
    parser.add_argument("--version", action="version", version=f"purrimer-build {__version__}")
    parser.add_argument(
        "--components-dir",
        type=Path,
        action="append",
        default=[],
        help="Extra component folders; later ones override built-in components of the same name.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    b = sub.add_parser("build", help="Render styles and components.")
    b.add_argument("--tokens", type=Path, default=Path("tokens/tokens.json"))
    b.add_argument("--fonts", type=Path, default=Path("tokens/fonts"))
    b.add_argument("--out", type=Path, default=Path("dist"))
    b.add_argument("--targets", default="all", help=f"'all' or a comma-separated list of: {', '.join(ALL_TARGETS)}")
    b.add_argument("--only", default="", help="Comma-separated component names to build.")
    b.add_argument("--clean", action="store_true", help="Delete the output folder first.")
    b.add_argument("--avalonia-namespace", default="Purrimer.Avalonia")
    b.add_argument(
        "--avalonia-assembly",
        default="Purrimer.Avalonia",
        help="Assembly name used in avares:// URIs for fonts and control themes.",
    )
    b.set_defaults(func=cmd_build)

    c = sub.add_parser("components", help="Show which targets each component supports.")
    c.set_defaults(func=cmd_components)

    n = sub.add_parser("new", help="Create an empty component folder with one template per layer.")
    n.add_argument("name")
    n.add_argument("--group", default="Other")
    n.add_argument("--layers", default="", help=f"Comma-separated layers: {', '.join(LAYERS)}")
    n.set_defaults(func=cmd_new)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
