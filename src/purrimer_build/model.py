"""Token model: reads tokens.json from the Purrimer design system into typed values."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

THEME_LABELS = {"blanc": "Blanc", "noir": "Noir", "light": "Latte", "dark": "Mocha"}
DARK_THEMES = frozenset({"noir", "dark"})

# Base size for em values on native targets (text-body-medium).
EM_BASE_PX = 14.0

HEX_RE = re.compile(r"^#([0-9a-fA-F]{3,8})$")
RGB_RE = re.compile(r"^rgba?\(\s*([^)]*)\)$")
ALIAS_RE = re.compile(r"^\{(.+)\}$")


@dataclass(frozen=True)
class Color:
    r: int
    g: int
    b: int
    a: float = 1.0

    @property
    def a255(self) -> int:
        return int(round(self.a * 255))

    @property
    def opaque(self) -> bool:
        return self.a255 == 255

    def hex6(self) -> str:
        return "#%02x%02x%02x" % (self.r, self.g, self.b)

    def rgba_hex(self) -> str:
        """#rrggbb, or #rrggbbaa with alpha (CSS, Slint)."""
        return self.hex6() if self.opaque else "#%02x%02x%02x%02x" % (self.r, self.g, self.b, self.a255)

    def argb_hex(self) -> str:
        """#rrggbb, or #aarrggbb with alpha (Qt, Avalonia)."""
        return self.hex6() if self.opaque else "#%02x%02x%02x%02x" % (self.a255, self.r, self.g, self.b)

    def qss(self) -> str:
        return self.hex6() if self.opaque else "rgba(%d, %d, %d, %d)" % (self.r, self.g, self.b, self.a255)


def _channel(text: str) -> int:
    text = text.strip()
    if text.endswith("%"):
        return round(float(text[:-1]) * 2.55)
    return round(float(text))


def _alpha(text: str) -> float:
    text = text.strip()
    if text.endswith("%"):
        return float(text[:-1]) / 100.0
    return float(text)


def parse_color(text: str) -> Color:
    text = text.strip()
    m = HEX_RE.match(text)
    if m:
        h = m.group(1)
        if len(h) in (3, 4):
            h = "".join(c * 2 for c in h)
        if len(h) == 6:
            h += "ff"
        if len(h) != 8:
            raise ValueError(f"Unsupported hex colour: {text}")
        return Color(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), int(h[6:8], 16) / 255.0)
    m = RGB_RE.match(text)
    if m:
        parts = [p for p in re.split(r"[\s,/]+", m.group(1).strip()) if p]
        if len(parts) not in (3, 4):
            raise ValueError(f"Unsupported rgb() colour: {text}")
        a = _alpha(parts[3]) if len(parts) == 4 else 1.0
        return Color(_channel(parts[0]), _channel(parts[1]), _channel(parts[2]), a)
    raise ValueError(f"Unsupported colour value: {text}")


def split_top_level(text: str, sep: str = ",") -> list[str]:
    parts: list[str] = []
    depth = 0
    cur: list[str] = []
    for ch in text:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == sep and depth == 0:
            parts.append("".join(cur).strip())
            cur = []
        else:
            cur.append(ch)
    if "".join(cur).strip():
        parts.append("".join(cur).strip())
    return parts


def parse_length(text: str | float, em_base: float = EM_BASE_PX) -> float:
    if isinstance(text, (int, float)):
        return float(text)
    text = str(text).strip()
    if text in ("0", ""):
        return 0.0
    m = re.match(r"^(-?[\d.]+)(px|rem|em)?$", text)
    if not m:
        raise ValueError(f"Unsupported length: {text}")
    value, unit = float(m.group(1)), m.group(2) or "px"
    if unit == "rem":
        return value * 16.0
    if unit == "em":
        return value * em_base
    return value


def parse_duration(text: str) -> int:
    m = re.match(r"^([\d.]+)(ms|s)$", str(text).strip())
    if not m:
        raise ValueError(f"Unsupported duration: {text}")
    value = float(m.group(1))
    return int(round(value * 1000 if m.group(2) == "s" else value))


@dataclass(frozen=True)
class Shadow:
    x: float
    y: float
    blur: float
    spread: float
    color: Color
    inset: bool


def parse_shadow(text: str) -> list[Shadow]:
    layers: list[Shadow] = []
    if text.strip() == "none":
        return layers
    for part in split_top_level(text):
        color_match = re.search(r"(rgba?\([^)]*\)|#[0-9a-fA-F]{3,8})", part)
        if not color_match:
            raise ValueError(f"Shadow without a colour: {part}")
        color = parse_color(color_match.group(1))
        rest = (part[: color_match.start()] + part[color_match.end() :]).strip()
        inset = False
        nums: list[float] = []
        for word in rest.split():
            if word == "inset":
                inset = True
            else:
                nums.append(parse_length(word))
        while len(nums) < 4:
            nums.append(0.0)
        layers.append(Shadow(nums[0], nums[1], nums[2], nums[3], color, inset))
    return layers


@dataclass(frozen=True)
class Easing:
    kind: str  # "cubic", "linear" or "points"
    values: tuple = ()

    def bezier_segments(self) -> list[float]:
        """QEasingCurve BezierSpline segments: c1x, c1y, c2x, c2y, endx, endy, repeated."""
        if self.kind == "linear":
            return [round(1 / 3, 5), round(1 / 3, 5), round(2 / 3, 5), round(2 / 3, 5), 1, 1]
        if self.kind == "cubic":
            return list(self.values) + [1, 1]
        seg: list[float] = []
        for (x0, y0), (x1, y1) in zip(self.values, self.values[1:], strict=False):
            if x1 <= x0:
                continue
            seg += [
                round(x0 + (x1 - x0) / 3, 5),
                round(y0 + (y1 - y0) / 3, 5),
                round(x0 + 2 * (x1 - x0) / 3, 5),
                round(y0 + 2 * (y1 - y0) / 3, 5),
                round(x1, 5),
                round(y1, 5),
            ]
        return seg


def parse_linear_points(args: str) -> tuple:
    entries: list[list] = []
    for part in split_top_level(args):
        bits = part.split()
        value = float(bits[0])
        stops = [float(b.rstrip("%")) / 100.0 for b in bits[1:]]
        if not stops:
            entries.append([value, None])
        for s in stops:
            entries.append([value, s])
    if entries[0][1] is None:
        entries[0][1] = 0.0
    if entries[-1][1] is None:
        entries[-1][1] = 1.0
    last = 0.0
    for e in entries:
        if e[1] is not None:
            e[1] = max(e[1], last)
            last = e[1]
    i = 0
    while i < len(entries):
        if entries[i][1] is None:
            j = i
            while entries[j][1] is None:
                j += 1
            start, end = entries[i - 1][1], entries[j][1]
            count = j - i + 1
            for k in range(i, j):
                entries[k][1] = start + (end - start) * (k - i + 1) / count
            i = j
        i += 1
    return tuple((e[1], e[0]) for e in entries)


def parse_easing(text: str) -> Easing:
    text = text.strip()
    if text == "linear":
        return Easing("linear")
    m = re.match(r"^cubic-bezier\(([^)]*)\)$", text)
    if m:
        return Easing("cubic", tuple(float(v) for v in m.group(1).split(",")))
    m = re.match(r"^linear\((.*)\)$", text, re.S)
    if m:
        return Easing("points", parse_linear_points(m.group(1)))
    raise ValueError(f"Unsupported easing: {text}")


@dataclass(frozen=True)
class TypeStyle:
    name: str
    family_key: str
    size: float
    line_height: float
    weight: int
    letter_spacing: float
    css: dict = field(hash=False, compare=False, default_factory=dict)


@dataclass
class Token:
    name: str
    value: object
    usage: str = ""


class Tokens:
    """Every token family from tokens.json, resolved per theme."""

    def __init__(self, data: dict):
        self.raw = data
        self.name = data.get("name", "Purrimer")
        self.themes: list[str] = [t["id"] for t in data["color"]["themes"]]
        self.theme_labels = {t: THEME_LABELS.get(t, t.title()) for t in self.themes}
        self.dark_themes = [t for t in self.themes if t in DARK_THEMES]
        first = self.themes[0]

        def themed(value, theme):
            if isinstance(value, dict):
                return value.get(theme, value.get(first))
            return value

        raw_colors = {t["name"]: t["value"] for t in data["color"]["tokens"]}
        self.usage = {t["name"]: t.get("usage", "") for t in data["color"]["tokens"]}
        self.color_css = {n: {th: themed(v, th) for th in self.themes} for n, v in raw_colors.items()}

        def resolve(name: str, theme: str, depth: int = 0) -> Color:
            if depth > 16:
                raise ValueError(f"Alias chain too deep at {name}")
            text = self.color_css[name][theme]
            m = ALIAS_RE.match(text.strip())
            if m:
                return resolve(m.group(1), theme, depth + 1)
            return parse_color(text)

        self.colors: dict[str, dict[str, Color]] = {n: {th: resolve(n, th) for th in self.themes} for n in raw_colors}

        self.shadow_css: dict[str, dict[str, str]] = {}
        self.shadows: dict[str, dict[str, list[Shadow]]] = {}
        for t in data.get("shadow", {}).get("tokens", []):
            self.shadow_css[t["name"]] = {th: themed(t["value"], th) for th in self.themes}
            self.shadows[t["name"]] = {th: parse_shadow(self.shadow_css[t["name"]][th]) for th in self.themes}

        def flat(family: str) -> list[tuple[str, str]]:
            return [(t["name"], t["value"]) for t in data.get(family, {}).get("tokens", [])]

        self.spacing = [(n, parse_length(v)) for n, v in flat("spacing")]
        self.radius = [(n, parse_length(v)) for n, v in flat("radius")]
        self.size = [(n, parse_length(v)) for n, v in flat("size")]
        self.border_width = [(n, parse_length(v)) for n, v in flat("borderWidth")]
        self.lengths = self.spacing + self.radius + self.size + self.border_width
        self.length_map = dict(self.lengths)
        self.lengths_css = flat("spacing") + flat("radius") + flat("size") + flat("borderWidth")
        self.durations = [(n, parse_duration(v)) for n, v in flat("duration")]
        self.duration_map = dict(self.durations)
        self.durations_css = flat("duration")
        self.easings = [(n, parse_easing(v)) for n, v in flat("easing")]
        self.easing_map = dict(self.easings)
        self.easings_css = flat("easing")
        known = {
            "name",
            "version",
            "meta",
            "color",
            "type",
            "spacing",
            "radius",
            "size",
            "borderWidth",
            "shadow",
            "duration",
            "easing",
        }
        self.other_css = []
        for key, value in data.items():
            if key not in known and isinstance(value, dict) and "tokens" in value:
                self.other_css.extend(flat(key))

        typ = data["type"]
        self.families: dict[str, str] = typ["families"]
        self.family_names = {k: v.split(",")[0].strip().strip("\"'") for k, v in self.families.items()}
        self.fonts: list[dict] = typ.get("fonts", [])
        self.type_styles: list[TypeStyle] = []
        for group in typ["groups"]:
            for st in group["styles"]:
                key = st.get("family", group.get("family", "sans"))
                size = parse_length(st["fontSize"])
                lh_raw = st.get("lineHeight")
                if lh_raw is None:
                    line_height = round(size * 20.0 / 14.0)
                elif isinstance(lh_raw, (int, float)) or re.match(r"^[\d.]+$", str(lh_raw)):
                    lh = float(lh_raw)
                    line_height = lh * size if lh < 10 else lh
                else:
                    line_height = parse_length(lh_raw)
                ls = st.get("letterSpacing")
                letter_spacing = parse_length(ls, em_base=size) if ls else 0.0
                weight = int(str(st.get("fontWeight", 400)).split()[0])
                self.type_styles.append(
                    TypeStyle(st["name"], key, size, line_height, weight, letter_spacing, css={**st, "familyKey": key})
                )
        self.type_map = {s.name: s for s in self.type_styles}

    @classmethod
    def load(cls, path: Path) -> Tokens:
        return cls(json.loads(Path(path).read_text(encoding="utf-8")))

    def css_color(self, name: str, theme: str) -> str:
        text = self.color_css[name][theme]
        m = ALIAS_RE.match(text.strip())
        return f"var(--{m.group(1)})" if m else text

    def is_color(self, name: str) -> bool:
        return name in self.colors

    def kind(self, name: str) -> str:
        if name in self.colors:
            return "color"
        if name in self.shadows:
            return "shadow"
        if name in self.length_map:
            return "length"
        if name in self.duration_map:
            return "duration"
        if name in self.easing_map:
            return "easing"
        if name in self.type_map:
            return "type"
        raise KeyError(f"Unknown token: {name}")
