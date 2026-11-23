from purrimer_qt.components import AvatarStack
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QWidget

PEOPLE = ["Mona Lisa", "Hubot", "Ada Lovelace", "Octo Cat", "Grace Hopper", "Linus Torvalds"]


def example() -> QWidget:
    row = QWidget()
    layout = QHBoxLayout(row)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(32)
    layout.addWidget(AvatarStack(PEOPLE), alignment=Qt.AlignmentFlag.AlignVCenter)
    layout.addWidget(AvatarStack(PEOPLE[:3], size=32), alignment=Qt.AlignmentFlag.AlignVCenter)
    layout.addStretch()
    return row
