"""Compile and screenshot each Slint example with slint-viewer.

    python run_slint.py manifest.json

For every example and theme this writes a small frame component that sets Purrimer.theme and places the example's
`Example` component, checks it with `slint-viewer --check`, then renders it with `--screenshot`. Any diagnostic
(warnings included) or non-zero exit fails the run.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

manifest = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
slint_dir = Path(manifest["dist"]) / "slint"
work = Path(manifest["out"]) / "slint-frames"
out = Path(manifest["out"]) / "slint"
work.mkdir(parents=True, exist_ok=True)
out.mkdir(parents=True, exist_ok=True)
viewer = shutil.which("slint-viewer")
if viewer is None:
    sys.exit("slint-viewer is not on PATH (cargo install slint-viewer, or download it from the Slint releases)")

ENUM = {"blanc": "blanc", "noir": "noir", "light": "latte", "dark": "mocha"}
FRAME = """import { Purrimer, PurrimerTheme } from "purrimer-components.slint";
import { Example } from "%(example)s";

export component Frame inherits Window {
    width: %(w)dpx;
    height: %(h)dpx;
    background: Purrimer.bg-color-default;
    default-font-family: Purrimer.text-body-medium.font-family;
    default-font-size: Purrimer.text-body-medium.font-size;
    init => { Purrimer.theme = PurrimerTheme.%(theme)s; }
    %(body)s
}
"""
PADDED = """VerticalLayout {
        padding: %dpx;
        alignment: start;
        Example { }
    }"""
BLEED = "Example { width: parent.width; height: parent.height; }"

env = {**os.environ, "SLINT_SCALE_FACTOR": str(manifest["scale"]), "NO_COLOR": "1", "CLICOLOR": "0"}
failures: list[str] = []
for theme in manifest["themes"]:
    for comp in manifest["components"]:
        name = comp["name"]
        label = f"slint/{name}/{theme}"
        frame = work / f"{name}-{theme}.slint"
        example = Path(comp["files"]["slint"]).as_posix()
        frame.write_text(
            FRAME
            % {
                "example": example,
                "w": comp["width"],
                "h": comp["height"],
                "theme": ENUM[theme],
                "body": BLEED if comp["bleed"] else PADDED % manifest["padding"],
            },
            encoding="utf-8",
        )
        problems = []
        base = [viewer, "-I", str(slint_dir), str(frame), "--component", "Frame"]
        for args in (
            ["--check"],
            ["--screenshot", str(out / f"{name}-{theme}.png"), "--size", f"{comp['width']}x{comp['height']}"],
        ):
            result = subprocess.run(base + args, env=env, capture_output=True, text=True, timeout=120)
            output = re.sub(r"\x1b\[[0-9;]*m", "", result.stdout + result.stderr).strip()
            if result.returncode != 0 or output:
                problems.append(f"{' '.join(args[:1])} exited {result.returncode}: {output}")
                break
        if problems:
            failures.append(f"{label}\n  " + "\n  ".join(problems))
        else:
            print(f"ok {label}")

if failures:
    print(f"\n{len(failures)} Slint example(s) failed:\n" + "\n".join(failures), file=sys.stderr)
    sys.exit(1)
