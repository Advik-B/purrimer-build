"""Render each Qt Widgets example offscreen and save a screenshot.

    QT_QPA_PLATFORM=offscreen python run_widgets.py manifest.json

Each examples/<Name>/qtwidgets.py defines example() -> QWidget. The run fails if an example raises or Qt logs a
warning, critical or fatal message while it is built, shown or grabbed.
"""

from __future__ import annotations

import importlib.util
import json
import os
import sys
import traceback
from pathlib import Path

manifest = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ["QT_SCALE_FACTOR"] = str(manifest["scale"])
os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
# The offscreen platform has no system fonts; give it only the bundled ones so renders match everywhere.
os.environ["QT_QPA_FONTDIR"] = str(Path(manifest["dist"]) / "fonts" / "ttf")
sys.path.insert(0, str(Path(manifest["dist"]) / "qtwidgets"))

from PySide6.QtCore import QEventLoop, Qt, QTimer, QtMsgType, qInstallMessageHandler  # noqa: E402
from PySide6.QtGui import QColor, QFont, QPainter, QPalette  # noqa: E402
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QWidget  # noqa: E402

# Longer than the slowest enter animation (duration-sleepy-long, 900ms) with room for slow CI runners.
SETTLE_MS = 1500

messages: list[str] = []


# The offscreen platform says this for every top-level window (here, Dialog); it is not about the example.
PLATFORM_NOISE = ("This plugin does not support propagateSizeHints()",)


def on_message(kind: QtMsgType, context, text: str) -> None:
    if kind != QtMsgType.QtDebugMsg and kind != QtMsgType.QtInfoMsg and text not in PLATFORM_NOISE:
        messages.append(f"{kind.name}: {text}")


qInstallMessageHandler(on_message)
app = QApplication(["purrimer-showcase"])
# The offscreen platform hints glyphs fully, which spaces letters unevenly; desktops hint vertically or slightly.
_font = app.font()
_font.setHintingPreference(QFont.HintingPreference.PreferVerticalHinting)
app.setFont(_font)

from purrimer_qt import apply  # noqa: E402
from purrimer_qt import tokens as T  # noqa: E402


def load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(f"example_{name}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def wait(ms: int) -> None:
    loop = QEventLoop()
    QTimer.singleShot(ms, loop.quit)
    loop.exec()


def settle() -> None:
    for _ in range(3):
        app.processEvents()


failures: list[str] = []
out = Path(manifest["out"]) / "qtwidgets"
out.mkdir(parents=True, exist_ok=True)
pad = manifest["padding"]
for theme in manifest["themes"]:
    apply(app, theme)
    for comp in manifest["components"]:
        label = f"qtwidgets/{comp['name']}/{theme}"
        messages.clear()
        try:
            frame = QWidget()
            frame.setFixedSize(comp["width"], comp["height"])
            frame.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
            palette = frame.palette()
            palette.setColor(QPalette.ColorRole.Window, QColor(T.COLORS["bgColor-default"][theme]))
            frame.setPalette(palette)
            frame.setAutoFillBackground(True)
            layout = QVBoxLayout(frame)
            margin = 0 if comp["bleed"] else pad
            layout.setContentsMargins(margin, margin, margin, margin)
            example = load(comp["files"]["qtwidgets"], comp["name"]).example()
            dialog = example if isinstance(example, QDialog) else None
            if dialog is None:
                layout.addWidget(example)
            if not comp["bleed"]:
                layout.addStretch()
            # Qt gives the first focusable child keyboard focus; keep it on the frame so no focus ring shows.
            frame.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
            frame.show()
            frame.setFocus()
            wait(SETTLE_MS)  # let enter animations (Snackbar fade, BottomSheet slide) finish
            shot = frame.grab()
            if dialog is not None:
                # A QDialog is its own window: show it, then draw it over a scrim in the middle of the frame.
                dialog.show()
                wait(SETTLE_MS)
                painter = QPainter(shot)
                painter.fillRect(
                    0, 0, comp["width"], comp["height"], QColor(T.COLORS["overlay-backdrop-bgColor"][theme])
                )
                image = dialog.grab()
                x = (comp["width"] - dialog.width()) // 2
                y = (comp["height"] - dialog.height()) // 2
                painter.drawPixmap(x, y, image)
                painter.end()
                dialog.close()
            if not shot.save(str(out / f"{comp['name']}-{theme}.png")):
                messages.append("could not save the screenshot")
            frame.close()
            frame.deleteLater()
            settle()
        except Exception:
            messages.append(traceback.format_exc())
        if messages:
            failures.append(f"{label}\n  " + "\n  ".join(messages))
        else:
            print(f"ok {label}")

if failures:
    print(f"\n{len(failures)} Qt Widgets example(s) failed:\n" + "\n".join(failures), file=sys.stderr)
    sys.exit(1)
