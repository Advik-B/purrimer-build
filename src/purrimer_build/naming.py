"""Name conversions shared by every target."""

from __future__ import annotations

import re


def words(name: str) -> list[str]:
    out: list[str] = []
    for chunk in re.split(r"[-._\s]+", name):
        if chunk:
            out.extend(p for p in re.split(r"(?<=[a-z0-9])(?=[A-Z])", chunk) if p)
    return out


def camel(name: str) -> str:
    w = words(name)
    return w[0][0].lower() + w[0][1:] + "".join(x[0].upper() + x[1:] for x in w[1:])


def pascal(name: str) -> str:
    return "".join(x[0].upper() + x[1:] for x in words(name))


def kebab(name: str) -> str:
    return "-".join(x.lower() for x in words(name))


def snake(name: str) -> str:
    return "_".join(x.lower() for x in words(name))


def num(value: float) -> str:
    value = round(float(value), 4)
    if value == int(value):
        return str(int(value))
    return ("%.4f" % value).rstrip("0").rstrip(".")
