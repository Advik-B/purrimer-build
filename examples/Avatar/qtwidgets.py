from purrimer_qt.components import Avatar
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QWidget


def example() -> QWidget:
    # Pass pixmap=QPixmap(path) for a picture.
    row = QWidget()
    layout = QHBoxLayout(row)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(12)
    layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
    layout.addWidget(Avatar("Ada Lovelace", size=24))
    layout.addWidget(Avatar("Grace Hopper"))
    layout.addWidget(Avatar("Alan Turing", size=40))
    layout.addWidget(Avatar("Purrimer", size=48, square=True))
    layout.addStretch()
    return row
