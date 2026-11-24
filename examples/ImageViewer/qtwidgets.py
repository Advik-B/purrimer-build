from pathlib import Path

from purrimer_qt.components import ImageViewer
from PySide6.QtWidgets import QVBoxLayout, QWidget


def example() -> QWidget:
    page = QWidget()
    layout = QVBoxLayout(page)
    layout.setContentsMargins(0, 0, 0, 0)
    viewer = ImageViewer(
        str(Path(__file__).with_name("photo.jpg")),
        alt="Sunset over the lake",
        caption="Lake Ilgen, an hour before dark",
        inline=True,
    )
    viewer.closed.connect(lambda: print("close"))
    layout.addWidget(viewer)
    return page
