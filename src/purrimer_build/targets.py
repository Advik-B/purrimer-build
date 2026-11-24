"""The seven targets. Each one renders its style templates, then one file per component layer it supports."""

from __future__ import annotations

import json
import shutil
import sys

from .components import Component
from .engine import GENERATED_NOTE, Build, checked
from .model import DARK_THEMES
from .motion import slint_source
from .naming import camel, kebab, num, pascal, snake

ALL_TARGETS = ("css", "svelte", "solid", "qtwidgets", "qtquick", "avalonia", "slint")

# Avalonia: Blanc and Noir are the built-in Light and Dark variants; Latte and Mocha inherit from them.
AVALONIA_KEYS = {"blanc": "Light", "noir": "Dark", "light": "Latte", "dark": "Mocha"}
AVALONIA_INHERITS = {"light": "Light", "dark": "Dark"}

SLINT_SPRING_FALLBACK = {
    "easing-playful-spring": "ease-out-back",
    "easing-playful-bounce": "ease-out-elastic",
}


def _missing(build: Build, comp: Component, target: str) -> None:
    print(f"  {target}: {comp.name} has no template for this target, skipped", file=sys.stderr)


def _copy_ttf(build: Build, dest: str) -> None:
    src = build.out / "fonts" / "ttf"
    for font in build.static_fonts:
        target = build.out / dest / font.filename
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src / font.filename, target)


# Web: CSS, Svelte, Solid


def web_env(build: Build):
    t = build.tokens
    return build.environment(filters={"tok": checked(t, lambda n: f"var(--{n})")})


def components_css(build: Build, env) -> str:
    parts = [f"/* {GENERATED_NOTE} */", f"/* {build.tokens.name} components. Load after purrimer.css. */", ""]
    for comp in build.components:
        if comp.has("web.css"):
            parts.append(f"/* {comp.name} */")
            parts.append(env.get_template("c/" + comp.template("web.css")).render(c=comp).strip())
            parts.append("")
    return "\n".join(parts) + "\n"


def build_css(build: Build) -> None:
    env = web_env(build)
    build.render(
        env,
        "t/styles/css/purrimer.css.j2",
        "css/purrimer.css",
        font_prefix="../fonts/woff2/",
        web_fonts=build.web_fonts,
    )
    build.write("css/purrimer-components.css", components_css(build, env))
    env.globals["svg_uri"] = lambda name, color: _svg_uri(build.icon_path(name, 16), color)
    build.render(
        env,
        "t/styles/css/purrimer-classless.css.j2",
        "css/purrimer-classless.css",
        font_prefix="../fonts/woff2/",
        web_fonts=build.web_fonts,
    )


def _svg_uri(path: str, color: str) -> str:
    """A 16px Octicon as a CSS url() for backgrounds."""
    svg = f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'><path fill='{color}' d='{path}'/></svg>"
    return 'url("data:image/svg+xml,%s")' % svg.replace("#", "%23").replace("<", "%3C").replace(">", "%3E")


def _web_framework(build: Build, name: str, ext: str, layer: str, theme_template: str, theme_file: str) -> None:
    env = web_env(build)
    base = name
    build.render(
        env,
        "t/styles/css/purrimer.css.j2",
        f"{base}/purrimer.css",
        font_prefix="../fonts/woff2/",
        web_fonts=build.web_fonts,
    )
    build.write(f"{base}/purrimer-components.css", components_css(build, env))
    build.render(env, "t/styles/web/tokens.ts.j2", f"{base}/tokens.ts")
    build.render(env, "t/styles/web/icons.ts.j2", f"{base}/icons.ts", icons=build.icons)
    build.render(env, "t/styles/web/motion.ts.j2", f"{base}/motion.ts")
    build.render(env, theme_template, f"{base}/{theme_file}")
    done = []
    for comp in build.components:
        if comp.has(layer):
            build.render(env, "c/" + comp.template(layer), f"{base}/components/{comp.name}.{ext}", c=comp)
            done.append(comp)
        else:
            _missing(build, comp, name)
    build.render(env, f"t/styles/{name}/index.ts.j2", f"{base}/index.ts", done=done)


def build_svelte(build: Build) -> None:
    _web_framework(build, "svelte", "svelte", "svelte", "t/styles/svelte/theme.svelte.ts.j2", "theme.svelte.ts")


def build_solid(build: Build) -> None:
    _web_framework(build, "solid", "tsx", "solid", "t/styles/solid/theme.ts.j2", "theme.ts")


# Qt Widgets (PySide6)


def build_qtwidgets(build: Build) -> None:
    t = build.tokens
    env = build.environment(filters={"tok": checked(t, lambda n: repr(n))})
    pkg = "qtwidgets/purrimer_qt"
    for theme in t.themes:
        c = {n: t.colors[n][theme].qss() for n in t.colors}
        build.render(
            env,
            "t/styles/qtwidgets/purrimer.qss.j2",
            f"{pkg}/qss/purrimer-{theme}.qss",
            theme=theme,
            c=c,
            L={n: int(round(v)) for n, v in t.lengths},
            fam=t.family_names,
        )
    icon_files = []
    for theme in t.themes:
        cols = t.colors
        sets = {
            "check": cols["fgColor-onEmphasis"][theme],
            "dash": cols["fgColor-onEmphasis"][theme],
            "dot-fill": cols["fgColor-onEmphasis"][theme],
            "chevron-down": cols["fgColor-muted"][theme],
            "chevron-up": cols["fgColor-muted"][theme],
        }
        for icon, color in sets.items():
            name = f"{icon}-{theme}.svg"
            build.write(f"{pkg}/icons/{name}", _svg(build.icon_path(icon, 16), color.hex6()))
            icon_files.append(name)
        name = f"chevron-down-{theme}-disabled.svg"
        build.write(
            f"{pkg}/icons/{name}", _svg(build.icon_path("chevron-down", 16), cols["fgColor-disabled"][theme].hex6())
        )
        icon_files.append(name)
    build.render(env, "t/styles/qtwidgets/purrimer.qrc.j2", "qtwidgets/purrimer.qrc", icon_files=icon_files)
    build.write("qtwidgets/qt_tokens.json", json.dumps(_qt_tokens(build), indent=2) + "\n")
    _copy_ttf(build, f"{pkg}/fonts")
    build.render(env, "t/styles/qtwidgets/tokens.py.j2", f"{pkg}/tokens.py", qt=_qt_tokens(build))
    build.render(env, "t/styles/qtwidgets/theme.py.j2", f"{pkg}/theme.py", fonts=build.static_fonts)
    build.render(env, "t/styles/qtwidgets/icons.py.j2", f"{pkg}/icons.py", icons=build.icons)
    build.render(env, "t/styles/qtwidgets/motion.py.j2", f"{pkg}/motion.py")
    done = []
    for comp in build.components:
        if comp.has("pyside"):
            build.render(env, "c/" + comp.template("pyside"), f"{pkg}/components/{snake(comp.name)}.py", c=comp)
            done.append(comp)
        else:
            _missing(build, comp, "qtwidgets")
    build.render(env, "t/styles/qtwidgets/components_init.py.j2", f"{pkg}/components/__init__.py", done=done)
    build.render(env, "t/styles/qtwidgets/package_init.py.j2", f"{pkg}/__init__.py", done=done)


def _svg(path: str, color: str) -> str:
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">'
        f'<path fill="{color}" d="{path}"/></svg>\n'
    )


def _qt_tokens(build: Build) -> dict:
    t = build.tokens
    return {
        "themes": t.themes,
        "dark": t.dark_themes,
        "colors": {n: {th: t.colors[n][th].argb_hex() for th in t.themes} for n in t.colors},
        "shadows": {
            n: {
                th: [
                    {
                        "x": s.x,
                        "y": s.y,
                        "blur": s.blur,
                        "spread": s.spread,
                        "color": s.color.argb_hex(),
                        "inset": s.inset,
                    }
                    for s in t.shadows[n][th]
                ]
                for th in t.themes
            }
            for n in t.shadows
        },
        "lengths": dict(t.lengths),
        "durations": dict(t.durations),
        "easings": {n: e.bezier_segments() for n, e in t.easings},
        "textStyles": {
            s.name: {
                "family": t.family_names[s.family_key],
                "pixelSize": s.size,
                "lineHeight": s.line_height,
                "weight": s.weight,
                "letterSpacing": round(s.letter_spacing, 3),
            }
            for s in t.type_styles
        },
        "families": t.family_names,
    }


# Qt Quick


def build_qtquick(build: Build) -> None:
    t = build.tokens

    def tok(n: str) -> str:
        return "Purrimer." + camel(n)

    env = build.environment(filters={"tok": checked(t, tok)}, globals_={"qml_shadows": _qt_tokens(build)["shadows"]})
    mod = "qtquick/Purrimer"
    _copy_ttf(build, f"{mod}/fonts")
    build.render(env, "t/styles/qtquick/Purrimer.qml.j2", f"{mod}/Purrimer.qml", fonts=build.static_fonts)
    build.render(env, "t/styles/qtquick/Octicons.qml.j2", f"{mod}/Octicons.qml", icons=build.icons)
    build.render(env, "t/styles/qtquick/PmSpring.qml.j2", f"{mod}/PmSpring.qml")
    build.render(env, "t/styles/qtquick/PmMotion.js.j2", f"{mod}/PmMotion.js")
    build.render(env, "t/styles/qtquick/PmMotionPlayer.qml.j2", f"{mod}/PmMotionPlayer.qml")
    done = []
    for comp in build.components:
        if comp.has("qml"):
            build.render(env, "c/" + comp.template("qml"), f"{mod}/{comp.name}.qml", c=comp)
            done.append(comp)
        else:
            _missing(build, comp, "qtquick")
    build.render(env, "t/styles/qtquick/qmldir.j2", f"{mod}/qmldir", done=done)


# Avalonia


def build_avalonia(build: Build, namespace: str, assembly: str) -> None:
    t = build.tokens

    def tok(n: str) -> str:
        kind = t.kind(n)
        if kind in ("color", "shadow"):
            return "{DynamicResource Pm%s}" % pascal(n)
        return "{StaticResource Pm%s}" % pascal(n)

    def tokx(n: str, suffix: str) -> str:
        t.kind(n)
        return "{StaticResource Pm%s%s}" % (pascal(n), suffix)

    def font(key: str) -> str:
        if key not in t.family_names:
            raise KeyError(f"Unknown font family: {key}")
        return "{StaticResource PmFont%s}" % pascal(key)

    env = build.environment(
        filters={"tok": checked(t, tok), "tokx": tokx, "font": font},
        globals_={
            "ns": namespace,
            "assembly": assembly,
            "ava_keys": AVALONIA_KEYS,
            "ava_inherits": AVALONIA_INHERITS,
            "ava_shadow": _ava_shadow,
        },
    )
    base = "avalonia/Purrimer"
    _copy_ttf(build, f"{base}/Fonts")
    build.render(env, "t/styles/avalonia/Purrimer.axaml.j2", f"{base}/Purrimer.axaml")
    build.render(env, "t/styles/avalonia/PurrimerThemes.cs.j2", f"{base}/PurrimerThemes.cs")
    build.render(env, "t/styles/avalonia/Icons.axaml.j2", f"{base}/Icons.axaml", icons=build.icons)
    done = []
    for comp in build.components:
        if comp.has("avalonia.axaml"):
            build.render(env, "c/" + comp.template("avalonia.axaml"), f"{base}/Themes/{comp.name}.axaml", c=comp)
            if comp.has("avalonia.cs"):
                build.render(env, "c/" + comp.template("avalonia.cs"), f"{base}/Controls/{comp.name}.cs", c=comp)
            done.append(comp)
        else:
            _missing(build, comp, "avalonia")
    build.render(env, "t/styles/avalonia/Controls.axaml.j2", f"{base}/Controls.axaml", done=done)


def _ava_shadow(layers) -> str:
    if not layers:
        return "0 0 0 0 #00000000"
    parts = []
    for s in layers:
        text = f"{num(s.x)} {num(s.y)} {num(s.blur)} {num(s.spread)} {s.color.argb_hex()}"
        parts.append(("inset " + text) if s.inset else text)
    return ", ".join(parts)


# Slint


def build_slint(build: Build) -> None:
    t = build.tokens

    def tok(n: str) -> str:
        kind = t.kind(n)
        if kind in ("duration", "easing"):
            return "PurrimerMotion." + kebab(n)
        return "Purrimer." + kebab(n)

    def slint_easing(n: str) -> str:
        e = t.easing_map[n]
        if e.kind == "cubic":
            return "cubic-bezier(%s)" % ", ".join(num(v) for v in e.values)
        if e.kind == "linear":
            return "linear"
        return SLINT_SPRING_FALLBACK.get(n, "ease-out-back")

    env = build.environment(
        filters={"tok": checked(t, tok)},
        globals_={"slint_easing": slint_easing, "enum_names": {th: kebab(t.theme_labels[th]) for th in t.themes}},
    )
    _copy_ttf(build, "slint/fonts")
    build.render(env, "t/styles/slint/purrimer.slint.j2", "slint/purrimer.slint", fonts=build.static_fonts)
    build.render(env, "t/styles/slint/icons.slint.j2", "slint/icons.slint", icons=build.icons)
    build.write(
        "slint/motion.slint",
        f"// {GENERATED_NOTE}\n// The motion catalog: the same keyframes as the web's pm-m-* classes.\n"
        'import { PurrimerMotion } from "purrimer.slint";\n\n' + slint_source(build.motion, t),
    )
    done = []
    for comp in build.components:
        if comp.has("slint"):
            build.render(env, "c/" + comp.template("slint"), f"slint/components/{kebab(comp.name)}.slint", c=comp)
            done.append(comp)
        else:
            _missing(build, comp, "slint")
    build.render(env, "t/styles/slint/components.slint.j2", "slint/purrimer-components.slint", done=done)


def run_target(build: Build, name: str, options: dict) -> None:
    if name == "css":
        build_css(build)
    elif name == "svelte":
        build_svelte(build)
    elif name == "solid":
        build_solid(build)
    elif name == "qtwidgets":
        build_qtwidgets(build)
    elif name == "qtquick":
        build_qtquick(build)
    elif name == "avalonia":
        build_avalonia(build, options["avalonia_namespace"], options["avalonia_assembly"])
    elif name == "slint":
        build_slint(build)
    else:
        raise ValueError(f"Unknown target: {name}")


__all__ = ["ALL_TARGETS", "DARK_THEMES", "run_target"]
