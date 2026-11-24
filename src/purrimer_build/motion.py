"""The motion catalog: data/motion.toml read into per-kind keyframe tables, CSS text and a reference evaluator.

The web gets @keyframes and .pm-m-* classes written from the catalog; each native target gets the same keyframes
evaluated for each kind (sleepy, playful, reduced) as plain numbers, plus the easing curves by token name, and plays
them with its own small evaluator. `sample()` here is the reference those evaluators are checked against.
"""

from __future__ import annotations

import math
import re
import tomllib
from dataclasses import dataclass, field
from importlib import resources

from .model import Easing, Tokens
from .naming import num

KINDS = ("sleepy", "playful", "reduced")
CATEGORIES = ("enter", "exit", "attention", "feedback", "ambient", "loading", "choreography")

# Units of the kind parameters and of each channel.
PARAM_DIMS = {"dist": "px", "far": "px", "lift": "px", "blur": "px", "rot": "deg", "spin": "deg"}
CHANNEL_DIMS = {
    "tx": "px",
    "ty": "px",
    "blur": "px",
    "halo": "px",
    "rot": "deg",
    "skew": "deg",
    "rotX": "deg",
    "rotY": "deg",
    "orbit": "deg",
}
TRANSFORM = ("tx", "txp", "ty", "typ", "rot", "rotX", "rotY", "sx", "sy", "skew")
GROUPS = {
    "transform": TRANSFORM,
    "opacity": ("opacity",),
    "blur": ("blur",),
    "reveal": ("reveal",),
    "halo": ("halo",),
    "wash": ("wash",),
    "ring": ("ringS", "ringO"),
    "draw": ("draw",),
    "orbit": ("orbit",),
}
CHANNELS = tuple(ch for chans in GROUPS.values() for ch in chans)
# Channels CSS clamps (opacity to 0..1, blur to 0 and up); the natives clamp the same ones.
CLAMPED = ("opacity", "ringO", "wash", "draw")
NON_NEGATIVE = ("blur",)
REST = {ch: 0.0 for ch in CHANNELS} | {"opacity": 1.0, "sx": 1.0, "sy": 1.0, "reveal": 1.0, "ringS": 1.0, "draw": 1.0}

DURATION_VARS = {
    "short": "--pm-m-short",
    "medium": "--pm-m-medium",
    "long": "--pm-m-long",
    "exit": "--pm-m-exit",
    "attn": "--pm-m-attn",
    "loop": "--pm-m-loop",
    "loopLong": "--pm-m-loop-long",
    "spin": "--pm-m-spin-dur",
    "stagger": "--pm-m-stagger",
    "press": "--pm-m-press",
}
EASE_SLOTS = ("enter", "big", "leave", "move", "wave", "pop", "fall")
FIXED_EASES = {"linear": "easing-linear", "drift": "easing-sleepy-drift"}


# Expressions


@dataclass(frozen=True)
class Num:
    v: float


@dataclass(frozen=True)
class Var:
    name: str


@dataclass(frozen=True)
class Bin:
    op: str
    a: object
    b: object


_TOKEN = re.compile(r"\s*(?:(\d+(?:\.\d+)?)|([A-Za-z]\w*)|(.))")


def parse_expr(text: str):
    tokens = []
    for m in _TOKEN.finditer(text.strip()):
        if m.group(1):
            tokens.append(("num", float(m.group(1))))
        elif m.group(2):
            tokens.append(("name", m.group(2)))
        elif m.group(3) and m.group(3).strip():
            tokens.append(("op", m.group(3)))
    pos = 0

    def peek():
        return tokens[pos] if pos < len(tokens) else (None, None)

    def take():
        nonlocal pos
        pos += 1
        return tokens[pos - 1]

    def atom():
        kind, val = take()
        if kind == "num":
            return Num(val)
        if kind == "name":
            return Var(val)
        if val == "-":
            inner = atom()
            if isinstance(inner, Num):
                return Num(-inner.v)
            return Bin("*", Num(-1), inner)
        if val == "(":
            node = additive()
            if take() != ("op", ")"):
                raise ValueError(f"Unbalanced parentheses in {text!r}")
            return node
        raise ValueError(f"Unexpected {val!r} in {text!r}")

    def term():
        node = atom()
        while peek() in (("op", "*"), ("op", "/")):
            op = take()[1]
            node = Bin(op, node, atom())
        return node

    def additive():
        node = term()
        while peek() in (("op", "+"), ("op", "-")):
            op = take()[1]
            node = Bin(op, node, term())
        return node

    node = additive()
    if pos != len(tokens):
        raise ValueError(f"Trailing input in {text!r}")
    return node


def evaluate(node, params: dict) -> float:
    if isinstance(node, Num):
        return node.v
    if isinstance(node, Var):
        if node.name not in params:
            raise KeyError(f"Unknown motion parameter: {node.name}")
        return float(params[node.name])
    a, b = evaluate(node.a, params), evaluate(node.b, params)
    if node.op == "+":
        return a + b
    if node.op == "-":
        return a - b
    if node.op == "*":
        return a * b
    return a / b


def _dim(node):
    if isinstance(node, Num):
        return None
    if isinstance(node, Var):
        return PARAM_DIMS.get(node.name)
    da, db = _dim(node.a), _dim(node.b)
    if node.op == "/":
        return da
    return da or db


def _css(node, want, parent_op=None, right=False) -> str:
    """CSS calc() body for an expression, carrying `want` (px, deg or None) through bare numbers."""
    if isinstance(node, Num):
        return f"{num(node.v)}{want or ''}"
    if isinstance(node, Var):
        return f"var(--pm-m-{node.name})"
    if node.op in "+-":
        text = f"{_css(node.a, want, node.op)} {node.op} {_css(node.b, want, node.op, True)}"
        needs = parent_op in ("*", "/") or (parent_op == "-" and right)
    else:
        if node.op == "/":
            a, b = _css(node.a, want, "/"), _css(node.b, None, "/", True)
        elif want and _dim(node.a) == want:
            a, b = _css(node.a, want, "*"), _css(node.b, None, "*", True)
        elif want and _dim(node.b) == want:
            a, b = _css(node.a, None, "*"), _css(node.b, want, "*", True)
        elif want and isinstance(node.b, Num):
            a, b = _css(node.a, None, "*"), _css(node.b, want, "*", True)
        elif want and isinstance(node.a, Num):
            a, b = _css(node.a, want, "*"), _css(node.b, None, "*", True)
        elif want:
            a, b = _css(node.a, None, "*"), f"{_css(node.b, None, '*', True)} * 1{want}"
        else:
            a, b = _css(node.a, None, "*"), _css(node.b, None, "*", True)
        text = f"{a} {node.op} {b}"
        needs = parent_op == "/" and right
    return f"({text})" if needs else text


def css_value(text: str, want: str | None) -> str:
    """A catalog expression as a CSS value: a literal, a var() or a calc()."""
    node = parse_expr(text)
    if isinstance(node, Num):
        if node.v == 0 and want:
            return f"0{want}"
        return f"{num(node.v)}{want or ''}"
    if isinstance(node, Var) and PARAM_DIMS.get(node.name) == want:
        return f"var(--pm-m-{node.name})"
    if _dim(node) is None and want and not any(isinstance(n, Num) for n in _leaves(node)):
        return f"calc({_css(node, None)} * 1{want})"
    return f"calc({_css(node, want)})"


def _leaves(node):
    if isinstance(node, Bin):
        yield from _leaves(node.a)
        yield from _leaves(node.b)
    else:
        yield node


# The catalog


@dataclass
class Frame:
    at: float
    ease: str | None
    groups: dict[str, dict[str, str]]


@dataclass
class Anim:
    name: str
    cat: str
    dur: str = "medium"
    ease: str = "enter"
    count: str = "1"
    origin: tuple[float, float] | str = (0.5, 0.5)
    fill: str = "both"
    reverse: bool = False
    decorative: bool = False
    perspective: float = 0.0
    orbit: str = "0"
    css: str = "auto"  # auto: class and keyframes; class: class only; manual: written by hand in the stylesheet
    use: str | dict[str, str] | None = None
    frames: list[Frame] = field(default_factory=list)

    def source(self, kind: str) -> str:
        """The catalog entry whose keyframes this one plays in `kind`."""
        if self.use is None:
            return self.name
        if isinstance(self.use, str):
            return self.use
        return self.use["playful" if kind == "playful" else "sleepy"]

    @property
    def per_kind(self) -> bool:
        return isinstance(self.use, dict)

    @property
    def kinded(self) -> bool:
        """Keyframes that name their own curves. Browsers ignore var() in a keyframe's animation-timing-function, so
        the web gets one @keyframes per kind with the curves written out."""
        return any(fr.ease for fr in self.frames)


def _frames(raw: list[dict], name: str) -> list[Frame]:
    out: list[Frame] = []
    for entry in raw:
        entry = dict(entry)
        offsets = entry.pop("at")
        ease = entry.pop("ease", None)
        if ease is not None and ease not in EASE_SLOTS and ease not in FIXED_EASES:
            raise ValueError(f"{name}: unknown easing {ease!r}")
        values: dict[str, str] = {}
        if entry.pop("none", False):
            values.update({ch: num(REST[ch]) for ch in TRANSFORM})
        if "s" in entry:
            s = entry.pop("s")
            values["sx"] = values["sy"] = s
        for ch, expr in entry.items():
            if ch not in CHANNELS:
                raise ValueError(f"{name}: unknown channel {ch!r}")
            parse_expr(expr)
            values[ch] = expr
        groups: dict[str, dict[str, str]] = {}
        for group, chans in GROUPS.items():
            hit = {ch: values[ch] for ch in chans if ch in values}
            if hit:
                if group == "transform":
                    hit = {ch: hit.get(ch, num(REST[ch])) for ch in TRANSFORM}
                groups[group] = hit
        for at in offsets:
            out.append(Frame(float(at), ease, groups))
    return out


@dataclass
class Catalog:
    kinds: dict[str, dict]
    anims: dict[str, Anim]

    @classmethod
    def load(cls, text: str | None = None) -> Catalog:
        if text is None:
            text = (resources.files("purrimer_build") / "data" / "motion.toml").read_text(encoding="utf-8")
        raw = tomllib.loads(text)
        anims: dict[str, Anim] = {}
        for name, entry in raw["anim"].items():
            entry = dict(entry)
            frames = _frames(entry.pop("frames", []), name)
            origin = entry.pop("origin", (0.5, 0.5))
            anim = Anim(name=name, frames=frames, origin=tuple(origin) if isinstance(origin, list) else origin, **entry)
            if anim.cat not in CATEGORIES:
                raise ValueError(f"{name}: unknown category {anim.cat!r}")
            anims[name] = anim
        for anim in anims.values():
            for kind in KINDS:
                src = anims.get(anim.source(kind))
                if src is None or src.use is not None or not src.frames:
                    raise ValueError(f"{anim.name}: uses {anim.source(kind)!r}, which has no keyframes of its own")
        return cls(raw["kinds"], anims)

    @property
    def rest(self) -> dict[str, float]:
        return dict(REST)

    def params(self, kind: str) -> dict:
        return {k: v for k, v in self.kinds[kind].items() if not isinstance(v, dict)}

    # Per-kind resolution, shared by every target.

    def duration_ms(self, tokens: Tokens, kind: str, expr: str) -> float:
        slots = self.kinds[kind]["durations"]
        values = {}
        for slot, src in slots.items():
            values[slot] = _token_ms(tokens, src)
        node = parse_expr(expr)
        return round(evaluate(node, values), 3)

    def ease_token(self, kind: str, slot: str) -> str:
        if slot in FIXED_EASES:
            return FIXED_EASES[slot]
        return self.kinds[kind]["easings"][slot]

    def count(self, kind: str, anim: Anim) -> int:
        if anim.count == "infinite":
            return -1
        if anim.count == "n":
            return int(self.kinds[kind]["n"])
        return int(anim.count)

    def tracks(self, kind: str, anim: Anim) -> dict[str, list[list]]:
        """Per channel: [[offset, value, easing token or None], ...] with the implicit 0% and 100% frames added.

        Channels that stay at rest are left out. A None easing means the animation's own curve, which an element
        may override; a named one is fixed by the keyframe, as in CSS."""
        src = self.anims[anim.source(kind)]
        params = self.params(kind)
        out: dict[str, list[list]] = {}
        for group, chans in GROUPS.items():
            by_at: dict[float, tuple[str | None, dict[str, str]]] = {}
            for fr in src.frames:
                if group in fr.groups:
                    prev = by_at.get(fr.at, (None, {}))
                    by_at[fr.at] = (fr.ease if fr.ease is not None else prev[0], {**prev[1], **fr.groups[group]})
            if not by_at:
                continue
            for edge in (0.0, 1.0):
                by_at.setdefault(edge, (None, {}))
            for ch in chans:
                track = []
                for at in sorted(by_at):
                    ease, vals = by_at[at]
                    value = evaluate(parse_expr(vals[ch]), params) if ch in vals else REST[ch]
                    token = self.ease_token(kind, ease) if ease else None
                    track.append([at, round(value, 6), token])
                if any(abs(v - REST[ch]) > 1e-9 for _, v, _ in track):
                    out[ch] = track
        return out

    def table(self, tokens: Tokens, kind: str) -> dict[str, dict]:
        """Everything a native player needs for one kind, by animation name."""
        params = self.params(kind)
        table = {}
        for name, anim in self.anims.items():
            src = self.anims[anim.source(kind)]
            table[name] = {
                "cat": anim.cat,
                "dur": self.duration_ms(tokens, kind, anim.dur),
                "ease": self.ease_token(kind, anim.ease),
                "count": self.count(kind, anim),
                "origin": list(anim.origin) if isinstance(anim.origin, tuple) else [0.0, 0.0],
                "menuOrigin": anim.origin == "menu",
                "fill": anim.fill,
                "reverse": anim.reverse,
                "decorative": anim.decorative,
                "perspective": src.perspective,
                "orbit": round(evaluate(parse_expr(src.orbit), params), 6),
                "tracks": self.tracks(kind, anim),
            }
        return table

    def stagger_ms(self, tokens: Tokens, kind: str) -> float:
        return _token_ms(tokens, self.kinds[kind]["durations"]["stagger"])

    def easings(self, tokens: Tokens) -> dict[str, list]:
        """Every easing a kind can name, as ["cubic", x1, y1, x2, y2], ["points", [[x, y], ...]] or ["linear"]."""
        names = set(FIXED_EASES.values())
        for kind in KINDS:
            names.update(self.kinds[kind]["easings"].values())
        names.add("easing-standard")
        return {n: easing_spec(tokens.easing_map[n]) for n in sorted(names)}

    # CSS

    def css_vars(self, tokens: Tokens, kind: str) -> list[tuple[str, str]]:
        """The --pm-m-* variables of one kind. Durations are written out in ms rather than read from the duration
        tokens, because reduced motion shortens those tokens and loops must keep their pace."""
        k = self.kinds[kind]
        base = "playful" if kind == "playful" else "sleepy"
        ms = {slot: _token_ms(tokens, src) for slot, src in k["durations"].items()}
        out = [(DURATION_VARS[slot][2:], f"{num(round(ms[slot], 3))}ms") for slot in DURATION_VARS]
        out.append(("pm-m-dots-dur", f"{num(round(ms['loop'] * (0.7 if kind == 'playful' else 0.45), 3))}ms"))
        out += [(f"pm-m-{slot}", f"var(--{k['easings'][slot]})") for slot in EASE_SLOTS]
        units = {"dist": "px", "far": "px", "lift": "px", "blur": "px", "rot": "deg", "spin": "deg"}
        for p in "dist far scale peak rot spin blur sx sy amp n lift breath ring".split():
            out.append((f"pm-m-{p}", f"{num(k[p])}{units.get(p, '')}"))
        out.append(("pm-m-press-scale", num(k["press"])))
        out.append(("pm-m-control-press", num(k["control"])))
        out.append(("pm-m-toggle-stretch", num(k["stretch"])))
        if kind == "playful":
            out += [
                ("pm-m-check-dur", f"{num(_token_ms(tokens, 'duration-playful-press'))}ms"),
                ("pm-m-check-ease", "var(--easing-playful-pop)"),
                ("pm-m-toggle-dur", f"{num(_token_ms(tokens, 'duration-playful-short'))}ms"),
                ("pm-m-toggle-ease", "var(--easing-playful-spring)"),
                ("pm-m-dash", "pm-chase-dash"),
            ]
        else:
            out += [
                ("pm-m-check-dur", f"{num(_token_ms(tokens, 'duration-fast'))}ms"),
                ("pm-m-check-ease", "var(--easing-standard)"),
                ("pm-m-toggle-dur", f"{num(_token_ms(tokens, 'duration-base'))}ms"),
                ("pm-m-toggle-ease", "var(--easing-standard)"),
                ("pm-m-dash", "none"),
            ]
        for anim in self.anims.values():
            if anim.per_kind:
                out.append((f"pm-m-p-{anim.name}", f"pm-{anim.source(base)}"))
            if anim.kinded:
                out.append((f"pm-m-k-{anim.name}", f"pm-{anim.name}" + ("-playful" if base == "playful" else "")))
        return out

    def css_duration(self, expr: str) -> str:
        node = parse_expr(expr)
        if isinstance(node, Var):
            return f"var({DURATION_VARS[node.name]})"

        def render(n, parent=None, right=False):
            if isinstance(n, Num):
                return num(n.v)
            if isinstance(n, Var):
                return f"var({DURATION_VARS[n.name]})"
            text = f"{render(n.a, n.op)} {n.op} {render(n.b, n.op, True)}"
            return f"({text})" if parent in ("*", "/") and n.op in "+-" else text

        return f"calc({render(node)})"

    def css_ease(self, slot: str) -> str:
        if slot == "linear":
            return "linear"
        if slot == "drift":
            return "var(--easing-sleepy-drift, ease-in-out)"
        return f"var(--pm-m-{slot})"

    def css_class(self, anim: Anim) -> str:
        decl = []
        if anim.dur != "medium":
            decl.append(f"--_pm-d: {self.css_duration(anim.dur)};")
        if anim.ease != "enter":
            decl.append(f"--_pm-e: {self.css_ease(anim.ease)};")
        if anim.count != "1":
            decl.append("--_pm-n: %s;" % ("infinite" if anim.count == "infinite" else "var(--pm-m-n)"))
        if anim.css == "manual":
            decl.append("animation-name: pm-hold;")
        elif anim.per_kind:
            decl.append(f"animation-name: var(--pm-m-p-{anim.name});")
        elif anim.kinded:
            decl.append(f"animation-name: var(--pm-m-k-{anim.name});")
        else:
            decl.append(f"animation-name: pm-{anim.source('sleepy')};")
        if anim.reverse:
            decl.append("animation-direction: reverse;")
        if anim.fill != "both":
            decl.append(f"animation-fill-mode: {anim.fill};")
        if anim.origin == "menu":
            decl.append("transform-origin: var(--pm-m-origin, 0 0);")
        elif anim.origin != (0.5, 0.5):
            ox, oy = anim.origin
            decl.append(f"transform-origin: {num(ox * 100)}% {num(oy * 100) if oy else 0}{'%' if oy else ''};")
        return f".pm-m-{anim.name} {{ {' '.join(decl)} }}"

    def css_keyframes(self, anim: Anim, tokens: Tokens | None = None) -> str:
        if anim.kinded:
            if tokens is None:
                raise ValueError(f"{anim.name}: keyframes with their own curves need the tokens")
            return "\n\n".join(self._keyframes(anim, tokens, kind) for kind in ("sleepy", "playful"))
        return self._keyframes(anim, None, None)

    def _keyframes(self, anim: Anim, tokens: Tokens | None, kind: str | None) -> str:
        used = {ch for fr in anim.frames for ch, v in fr.groups.get("transform", {}).items() if v != num(REST[ch])}
        suffix = "-playful" if kind == "playful" else ""
        literal = dict(tokens.easings_css) if tokens is not None else {}
        lines = [f"@keyframes pm-{anim.name}{suffix} {{"]
        order: list[tuple[str | None, dict]] = []
        merged: dict[tuple, int] = {}
        for fr in anim.frames:
            key = (repr(fr.groups), fr.ease)
            if key in merged:
                order[merged[key]][1]["at"].append(fr.at)
            else:
                merged[key] = len(order)
                order.append((fr.ease, {"at": [fr.at], "groups": fr.groups}))
        for ease, entry in order:
            sel = ", ".join(f"{num(a * 100)}%" for a in sorted(entry["at"]))
            props = []
            for group, vals in entry["groups"].items():
                props.append(_css_group(anim, group, vals, used))
            if ease and kind:
                props.append(f"animation-timing-function: {literal[self.ease_token(kind, ease)]};")
            elif ease:
                props.append(f"animation-timing-function: {self.css_ease(ease)};")
            lines.append(f"  {sel} {{ {' '.join(props)} }}")
        lines.append("}")
        return "\n".join(lines)


def _css_group(anim: Anim, group: str, vals: dict[str, str], used: set[str]) -> str:
    if group == "opacity":
        return f"opacity: {css_value(vals['opacity'], None)};"
    if group == "blur":
        return f"filter: blur({css_value(vals['blur'], 'px')});"
    if group == "reveal":
        r = float(evaluate(parse_expr(vals["reveal"]), {}))
        bottom = "100%" if r == 0 else "-64px" if r == 1 else f"calc({num(1 - r)} * 100% - {num(r * 64)}px)"
        return f"clip-path: inset(-64px -64px {bottom} -64px);"
    if group == "halo":
        spread = css_value(vals["halo"], "px")
        return f"box-shadow: var(--pm-m-shadow, 0 0 0 0 rgba(0, 0, 0, 0)), 0 0 0 {spread} var(--bgColor-accent-muted);"
    if group == "wash":
        w = float(evaluate(parse_expr(vals["wash"]), {}))
        color = "var(--pm-m-flash, var(--bgColor-attention-muted))"
        if w != 1:
            color = f"color-mix(in srgb, {color} {num(w * 100)}%, transparent)"
        return f"background-color: {color};"
    if group == "orbit":
        turn = float(evaluate(parse_expr(vals["orbit"]), {}))
        a, neg = f"{num(turn)}deg", f"{num(-turn)}deg"
        return f"transform: rotate({a}) translateX({css_value(anim.orbit, 'px')}) rotate({neg});"
    if group == "transform":
        return f"transform: {_css_transform(anim, vals, used)};"
    raise ValueError(f"{anim.name}: the {group} channel has no CSS form; mark the entry css = 'manual'")


def _css_transform(anim: Anim, vals: dict[str, str], used: set[str]) -> str:
    def v(ch, dim):
        return css_value(vals.get(ch, num(REST[ch])), dim)

    def axis(px, frac):
        has_px, has_frac = px in used, frac in used
        p = v(px, "px")
        f = f"{num(float(evaluate(parse_expr(vals.get(frac, '0')), {})) * 100)}%"
        if has_px and has_frac:
            inner_p = p[5:-1] if p.startswith("calc(") else p
            return f"calc({f} + {inner_p})"
        if has_frac:
            return f
        return p

    parts = []
    if anim.perspective:
        parts.append(f"perspective({num(anim.perspective)}px)")
    if used & {"tx", "txp", "ty", "typ"}:
        parts.append(f"translate({axis('tx', 'txp')}, {axis('ty', 'typ')})")
    if "rot" in used:
        parts.append(f"rotate({v('rot', 'deg')})")
    if "rotX" in used:
        parts.append(f"rotateX({v('rotX', 'deg')})")
    if "rotY" in used:
        parts.append(f"rotateY({v('rotY', 'deg')})")
    if used & {"sx", "sy"}:
        parts.append(f"scale({v('sx', None)}, {v('sy', None)})")
    if "skew" in used:
        parts.append(f"skewX({v('skew', 'deg')})")
    return " ".join(parts) or "none"


SLINT_FIELDS = {ch: re.sub(r"([A-Z])", lambda m: "-" + m.group(1).lower(), ch) for ch in REST}
SLINT_KINDS = {"sleepy": 0, "playful": 1, "reduced": 2}


def _sf(v: float) -> str:
    text = num(round(v, 6))
    return text if "." in text or "e" in text else text + ".0"


def slint_source(catalog: Catalog, tokens: Tokens) -> str:
    """The catalog for Slint, which has no loops or dynamic data: one pure sample() with every track written out as
    a piecewise expression, per animation and kind (0 sleepy, 1 playful, 2 reduced)."""
    easings = catalog.easings(tokens)
    out: list[str] = []
    w = out.append
    fields = ", ".join(f"{f}: float" for f in SLINT_FIELDS.values())
    w(f"export struct PmMotionFrame {{ {fields} }}")
    w(
        "export struct PmMotionEntry { dur: duration, count: int, origin-x: float, origin-y: float, menu-origin: bool,"
        " fill-both: bool, reverse: bool, decorative: bool, perspective: float, ease: string }"
    )
    w("")
    w("export global PmMotionCatalog {")
    w("    // One Newton step towards the curve parameter whose x is `x`.")
    w("    pure function newton(ax: float, bx: float, cx: float, x: float, t: float) -> float {")
    w("        let d = (3 * ax * t + 2 * bx) * t + cx;")
    w("        let err = ((ax * t + bx) * t + cx) * t - x;")
    w("        return Math.abs(d) < 0.000001 ? t : Math.clamp(t - err / d, 0, 1);")
    w("    }")
    w("")
    w("    public pure function cubic-bezier(x1: float, y1: float, x2: float, y2: float, x: float) -> float {")
    w("        if x <= 0 { return 0; }")
    w("        if x >= 1 { return 1; }")
    w("        let ax = 1 - 3 * x2 + 3 * x1;")
    w("        let bx = 3 * x2 - 6 * x1;")
    w("        let cx = 3 * x1;")
    prev = "x"
    for i in range(1, 9):
        w(f"        let t{i} = self.newton(ax, bx, cx, x, {prev});")
        prev = f"t{i}"
    w("        return ((1 - 3 * y2 + 3 * y1) * t8 + (3 * y2 - 6 * y1)) * t8 * t8 + 3 * y1 * t8;")
    w("    }")
    w("")
    w("    // An easing token's curve at p.")
    w("    public pure function ease(token: string, p: float) -> float {")
    for name, spec in easings.items():
        if spec[0] == "linear":
            expr = "p"
        elif spec[0] == "cubic":
            expr = "self.cubic-bezier(%s, p)" % ", ".join(_sf(v) for v in spec[1:])
        else:
            pts = spec[1]
            expr = _sf(pts[-1][1])
            for (x0, y0), (x1, y1) in reversed(list(zip(pts, pts[1:], strict=False))):
                if x1 == x0:
                    continue
                seg = f"{_sf(y0)} + {_sf(y1 - y0)} * (p - {_sf(x0)}) / {_sf(x1 - x0)}"
                expr = f"p <= {_sf(x1)} ? {seg} : {expr}"
            expr = f"p <= {_sf(pts[0][0])} ? {_sf(pts[0][1])} : {expr}"
        w(f'        if token == "{name}" {{ return {expr}; }}')
    w("        return p;")
    w("    }")
    w("")
    w("    public pure function has(name: string) -> bool {")
    names = " || ".join(f'name == "{n}"' for n in catalog.anims)
    w(f"        return {names};")
    w("    }")
    w("")
    tables = {k: catalog.table(tokens, k) for k in KINDS}
    w("    public pure function entry(name: string, kind: int) -> PmMotionEntry {")
    for name in catalog.anims:
        rows = []
        for kind in KINDS:
            e = tables[kind][name]
            ox, oy = e["origin"]
            rows.append(
                f"{{ dur: {num(round(e['dur'], 3))}ms, count: {e['count']}, origin-x: {_sf(ox)}, origin-y: {_sf(oy)},"
                f" menu-origin: {str(e['menuOrigin']).lower()}, fill-both: {str(e['fill'] == 'both').lower()},"
                f" reverse: {str(e['reverse']).lower()}, decorative: {str(e['decorative']).lower()},"
                f' perspective: {_sf(e["perspective"])}, ease: "{e["ease"]}" }}'
            )
        w(f'        if name == "{name}" {{ return kind == 1 ? {rows[1]} : kind == 2 ? {rows[2]} : {rows[0]}; }}')
    w('        return { dur: 1ms, count: 1, origin-x: 0.5, origin-y: 0.5, fill-both: true, ease: "easing-linear" };')
    w("    }")
    w("")
    w("    // Every channel of `name` at `progress` (0 to 1) of one iteration. `easing` overrides the animation's own")
    w('    // curve ("" keeps it).')
    w("    public pure function sample(name: string, kind: int, progress: float, easing: string) -> PmMotionFrame {")
    for name in catalog.anims:
        w(f'        if name == "{name}" {{')
        for kind in ("playful", "reduced", "sleepy"):
            e = tables[kind][name]
            p = "(1 - progress)" if e["reverse"] else "progress"
            d = f'(easing == "" ? "{e["ease"]}" : easing)'
            values = {ch: _sf(REST[ch]) for ch in REST}
            for ch, track in e["tracks"].items():
                expr = _sf(track[-1][1])
                for (t0, v0, e0), (t1, v1, _e1) in reversed(list(zip(track, track[1:], strict=False))):
                    if t1 == t0:
                        continue
                    curve = f'"{e0}"' if e0 else d
                    local = f"({p} - {_sf(t0)}) / {_sf(t1 - t0)}" if t0 else f"{p} / {_sf(t1 - t0)}"
                    seg = _sf(v0) if v0 == v1 else f"{_sf(v0)} + {_sf(v1 - v0)} * self.ease({curve}, {local})"
                    expr = seg if expr == seg else f"{p} <= {_sf(t1)} ? {seg} : {expr}"
                expr = f"{p} <= {_sf(track[0][0])} ? {_sf(track[0][1])} : {expr}" if track[0][0] > 0 else expr
                if ch in CLAMPED:
                    expr = f"Math.clamp({expr}, 0, 1)"
                elif ch in NON_NEGATIVE:
                    expr = f"Math.max({expr}, 0)"
                values[ch] = expr
            if "orbit" in e["tracks"]:
                a = f"({values['orbit']}) * 1deg"
                values["tx"] = f"{_sf(e['orbit'])} * Math.cos({a})"
                values["ty"] = f"{_sf(e['orbit'])} * Math.sin({a})"
            literal = ", ".join(f"{SLINT_FIELDS[ch]}: {v}" for ch, v in values.items())
            cond = {"playful": "kind == 1", "reduced": "kind == 2", "sleepy": None}[kind]
            if cond:
                w(f"            if {cond} {{ return {{ {literal} }}; }}")
            else:
                w(f"            return {{ {literal} }};")
        w("        }")
    rest = ", ".join(f"{SLINT_FIELDS[ch]}: {_sf(v)}" for ch, v in REST.items())
    w(f"        return {{ {rest} }};")
    w("    }")
    w("")
    stagger = {k: catalog.stagger_ms(tokens, k) for k in KINDS}
    w("    public pure function stagger(kind: int) -> duration {")
    w(
        f"        return kind == 1 ? {num(stagger['playful'])}ms : kind == 2 ? {num(stagger['reduced'])}ms"
        f" : {num(stagger['sleepy'])}ms;"
    )
    w("    }")
    w("}")
    return "\n".join(out) + "\n"


def _token_ms(tokens: Tokens, src) -> float:
    if isinstance(src, (int, float)):
        return float(src)
    m = re.fullmatch(r"\s*([\w-]+)\s*(?:\*\s*([\d.]+))?\s*", src)
    if not m:
        raise ValueError(f"Bad duration source: {src!r}")
    value = tokens.duration_map[m.group(1)]
    return value * float(m.group(2)) if m.group(2) else float(value)


def easing_spec(e: Easing) -> list:
    if e.kind == "linear":
        return ["linear"]
    if e.kind == "cubic":
        return ["cubic", *e.values]
    return ["points", [[round(x, 5), round(y, 5)] for x, y in e.values]]


# Reference evaluator


def ease_at(spec: list, p: float) -> float:
    if spec[0] == "linear":
        return p
    if spec[0] == "points":
        pts = spec[1]
        if p <= pts[0][0]:
            return pts[0][1]
        for (x0, y0), (x1, y1) in zip(pts, pts[1:], strict=False):
            if p <= x1:
                return y1 if x1 == x0 else y0 + (y1 - y0) * (p - x0) / (x1 - x0)
        return pts[-1][1]
    _, x1, y1, x2, y2 = spec
    return cubic_bezier(x1, y1, x2, y2, p)


def cubic_bezier(x1: float, y1: float, x2: float, y2: float, x: float) -> float:
    """y for x on the curve, by Newton's method with a bisection fallback (the same steps every target uses)."""
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0

    def bx(t):
        return ((1 - 3 * x2 + 3 * x1) * t + (3 * x2 - 6 * x1)) * t * t + 3 * x1 * t

    def by(t):
        return ((1 - 3 * y2 + 3 * y1) * t + (3 * y2 - 6 * y1)) * t * t + 3 * y1 * t

    def dx(t):
        return (3 * (1 - 3 * x2 + 3 * x1) * t + 2 * (3 * x2 - 6 * x1)) * t + 3 * x1

    t = x
    for _ in range(8):
        err = bx(t) - x
        if abs(err) < 1e-6:
            return by(t)
        d = dx(t)
        if abs(d) < 1e-6:
            break
        t -= err / d
    lo, hi, t = 0.0, 1.0, x
    for _ in range(30):
        if bx(t) < x:
            lo = t
        else:
            hi = t
        t = (lo + hi) / 2
    return by(t)


def track_at(track: list[list], p: float, default_ease: list, easings: dict[str, list]) -> float:
    if p <= track[0][0]:
        return track[0][1]
    for (t0, v0, e0), (t1, v1, _) in zip(track, track[1:], strict=False):
        if p <= t1:
            if t1 == t0:
                return v1
            local = (p - t0) / (t1 - t0)
            spec = easings[e0] if e0 else default_ease
            return v0 + (v1 - v0) * ease_at(spec, local)
    return track[-1][1]


def sample(table: dict, easings: dict[str, list], name: str, progress: float, ease: str | None = None) -> dict:
    """Channel values of one iteration at `progress` (0 to 1), as a native player computes them."""
    entry = table[name]
    p = 1 - progress if entry["reverse"] else progress
    default = easings[ease or entry["ease"]]
    out = dict(REST)
    for ch, track in entry["tracks"].items():
        out[ch] = track_at(track, p, default, easings)
        if ch in CLAMPED:
            out[ch] = min(1.0, max(0.0, out[ch]))
        elif ch in NON_NEGATIVE:
            out[ch] = max(0.0, out[ch])
    if "orbit" in entry["tracks"]:
        a = math.radians(out["orbit"])
        out["tx"] += entry["orbit"] * math.cos(a)
        out["ty"] += entry["orbit"] * math.sin(a)
    return out


__all__ = ["CATEGORIES", "CHANNELS", "KINDS", "REST", "Catalog", "css_value", "sample"]
