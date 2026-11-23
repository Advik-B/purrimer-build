"""Render each Qt Quick example in a window and save a screenshot.

    python run_quick.py manifest.json

Each examples/<Name>/qtquick.qml is loaded into a frame that sets Purrimer.theme. The run fails if the QML does not
load or Qt logs a warning, critical or fatal message (QML binding and type errors arrive as warnings).
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

manifest = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
dist = Path(manifest["dist"])
# A real window, not the offscreen platform: offscreen falls back to the software scene graph, which cannot draw
# RectangularShadow. CI runs this under xvfb with Mesa. System DPI scaling is off, so the scale is QT_SCALE_FACTOR.
os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
os.environ["QT_SCALE_FACTOR"] = str(manifest["scale"])
os.environ["QT_QPA_FONTDIR"] = str(dist / "fonts" / "ttf")
os.environ.setdefault("QT_QUICK_CONTROLS_STYLE", "Basic")

from PySide6.QtCore import QEventLoop, QObject, QTimer, QtMsgType, QUrl, qInstallMessageHandler  # noqa: E402
from PySide6.QtGui import QCursor, QFont, QGuiApplication  # noqa: E402
from PySide6.QtQml import QQmlComponent, QQmlEngine  # noqa: E402
from PySide6.QtQuick import QQuickWindow, QSGRendererInterface  # noqa: E402

# Longer than the slowest enter animation (duration-sleepy-long, 900ms) with room for slow CI runners.
SETTLE_MS = 1500

messages: list[str] = []


def on_message(kind: QtMsgType, context, text: str) -> None:
    if kind not in (QtMsgType.QtDebugMsg, QtMsgType.QtInfoMsg):
        messages.append(f"{kind.name}: {text}")


qInstallMessageHandler(on_message)
app = QGuiApplication(["purrimer-showcase"])
font = app.font()
font.setHintingPreference(QFont.HintingPreference.PreferVerticalHinting)
app.setFont(font)
engine = QQmlEngine()
engine.addImportPath(str(dist / "qtquick"))

FRAME = """
import QtQuick
import Purrimer

Window {
    width: %(w)d
    height: %(h)d
    color: Purrimer.bgColorDefault
    flags: Qt.FramelessWindowHint
    Binding { target: Purrimer; property: "theme"; value: "%(theme)s" }
    // Spinners and other loops stop on their first frame, so screenshots do not change from run to run.
    Binding { target: Purrimer; property: "pauseLoops"; value: true }
    Loader { objectName: "example"; %(place)s; source: "%(source)s" }
}
"""


def wait(ms: int) -> None:
    loop = QEventLoop()
    QTimer.singleShot(ms, loop.quit)
    loop.exec()


failures: list[str] = []
out = Path(manifest["out"]) / "qtquick"
out.mkdir(parents=True, exist_ok=True)
for theme in manifest["themes"]:
    for comp in manifest["components"]:
        label = f"qtquick/{comp['name']}/{theme}"
        messages.clear()
        source = QUrl.fromLocalFile(comp["files"]["qtquick"]).toString()
        qml = FRAME % {
            "w": comp["width"],
            "h": comp["height"],
            "theme": theme,
            "source": source,
            "place": "anchors.fill: parent" if comp["bleed"] else "x: %(p)d; y: %(p)d" % {"p": manifest["padding"]},
        }
        component = QQmlComponent(engine)
        component.setData(qml.encode(), QUrl.fromLocalFile(str(Path(manifest["out"]) / "frame.qml")))
        window = component.create()
        if component.isError() or not isinstance(window, QQuickWindow):
            messages += [e.toString() for e in component.errors()] or ["the frame did not create a window"]
        else:
            loader = window.findChild(QObject, "example")
            if loader.property("item") is None:
                messages.append("the example did not load")
            # A real window gets real hover: keep it clear of the pointer so nothing renders hovered.
            window.setPosition(0, 0)
            QCursor.setPos(window.screen().geometry().bottomRight())
            window.show()
            wait(SETTLE_MS)  # let enter transitions finish
            api = window.rendererInterface().graphicsApi()
            if api == QSGRendererInterface.GraphicsApi.Software:
                messages.append("Qt Quick fell back to the software renderer, which drops shadows; use a GPU or Mesa")
            image = window.grabWindow()
            if image.isNull() or not image.save(str(out / f"{comp['name']}-{theme}.png")):
                messages.append("could not grab the window")
            window.close()
            window.deleteLater()
        if messages:
            failures.append(f"{label}\n  " + "\n  ".join(messages))
        else:
            print(f"ok {label}")

if failures:
    print(f"\n{len(failures)} Qt Quick example(s) failed:\n" + "\n".join(failures), file=sys.stderr)
    sys.exit(1)
