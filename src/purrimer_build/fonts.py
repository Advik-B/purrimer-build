"""Font handling: copies the variable WOFF2 files and instances static TTF files for native toolkits."""

from __future__ import annotations

import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path

from .model import Tokens

STATIC_WEIGHTS = (400, 500, 600, 700)
WEIGHT_NAMES = {
    100: "Thin",
    200: "ExtraLight",
    300: "Light",
    400: "Regular",
    500: "Medium",
    600: "SemiBold",
    700: "Bold",
    800: "ExtraBold",
    900: "Black",
}
# Optical size for fonts with an opsz axis, matching body text at 14px.
OPSZ_FOR_STATIC = 14


@dataclass(frozen=True)
class StaticFont:
    family: str
    weight: int
    filename: str
    italic: bool


@dataclass(frozen=True)
class WebFont:
    family: str
    filename: str
    weight: str
    style: str


def copy_web_fonts(tokens: Tokens, fonts_dir: Path, out_dir: Path) -> list[WebFont]:
    woff_dir = out_dir / "woff2"
    woff_dir.mkdir(parents=True, exist_ok=True)
    result = []
    for entry in tokens.fonts:
        src = fonts_dir / Path(entry["file"]).name
        if not src.exists():
            print(f"Font file not found, skipped: {src}", file=sys.stderr)
            continue
        shutil.copyfile(src, woff_dir / src.name)
        result.append(WebFont(entry["family"], src.name, str(entry.get("weight", "400")), entry.get("style", "normal")))
    return result


def build_static_fonts(tokens: Tokens, fonts_dir: Path, out_dir: Path) -> list[StaticFont]:
    """Instance each variable font at fixed weights; static weights select reliably in every toolkit."""
    from fontTools.ttLib import TTFont
    from fontTools.varLib import instancer

    ttf_dir = out_dir / "ttf"
    ttf_dir.mkdir(parents=True, exist_ok=True)
    result: list[StaticFont] = []
    for entry in tokens.fonts:
        src = fonts_dir / Path(entry["file"]).name
        if not src.exists():
            continue
        probe = TTFont(src)
        family = entry["family"]
        stem = re.sub(r"[^A-Za-z0-9]", "", family)
        italic = bool(probe["OS/2"].fsSelection & 1)
        if "fvar" not in probe:
            probe.flavor = None
            name = f"{stem}-Regular.ttf"
            probe.save(ttf_dir / name)
            result.append(StaticFont(family, 400, name, italic))
            continue
        axes = {a.axisTag: (a.minValue, a.defaultValue, a.maxValue) for a in probe["fvar"].axes}
        lo, _, hi = axes.get("wght", (400, 400, 400))
        weights = [w for w in STATIC_WEIGHTS if lo <= w <= hi] or [int(min(max(400, lo), hi))]
        for w in weights:
            location = {}
            for tag, (amin, adef, amax) in axes.items():
                if tag == "wght":
                    location[tag] = w
                elif tag == "opsz":
                    location[tag] = min(max(OPSZ_FOR_STATIC, amin), amax)
                else:
                    location[tag] = adef
            font = instancer.instantiateVariableFont(TTFont(src), location, updateFontNames=False)
            _rename(font, family, w, italic)
            font.flavor = None
            name = f"{stem}-{WEIGHT_NAMES[w]}.ttf"
            font.save(ttf_dir / name)
            result.append(StaticFont(family, w, name, italic))
    return result


def _rename(font, family: str, weight: int, italic: bool) -> None:
    style = WEIGHT_NAMES[weight]
    ribbi = weight in (400, 700)
    legacy_family = family if ribbi else f"{family} {style}"
    legacy_style = ("Bold" if weight == 700 else "Regular") if ribbi else "Regular"
    if italic:
        legacy_style = "Bold Italic" if weight == 700 else "Italic"
        style_full = f"{style} Italic" if style != "Regular" else "Italic"
    else:
        style_full = style
    postscript = "%s-%s" % (re.sub(r"[^A-Za-z0-9]", "", family), style_full.replace(" ", ""))
    table = font["name"]
    for rec in list(table.names):
        if rec.nameID in (1, 2, 3, 4, 6, 16, 17, 21, 22, 25):
            table.removeNames(nameID=rec.nameID)
    table.setName(legacy_family, 1, 3, 1, 0x409)
    table.setName(legacy_style, 2, 3, 1, 0x409)
    table.setName(f"{family} {style_full}; Purrimer static", 3, 3, 1, 0x409)
    table.setName(f"{family} {style_full}", 4, 3, 1, 0x409)
    table.setName(postscript, 6, 3, 1, 0x409)
    table.setName(family, 16, 3, 1, 0x409)
    table.setName(style_full, 17, 3, 1, 0x409)
    font["OS/2"].usWeightClass = weight
    sel = font["OS/2"].fsSelection & ~(1 | 32 | 64)
    if italic:
        sel |= 1
    if weight == 700:
        sel |= 32
    if weight == 400 and not italic:
        sel |= 64
    font["OS/2"].fsSelection = sel
    font["head"].macStyle = (1 if weight == 700 else 0) | (2 if italic else 0)
    if "STAT" in font:
        del font["STAT"]
