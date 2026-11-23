from purrimer_qt.components import Spinner
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QWidget


def example() -> QWidget:
    row = QWidget()
    layout = QHBoxLayout(row)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(24)
    layout.addWidget(Spinner("small"), alignment=Qt.AlignmentFlag.AlignVCenter)
    layout.addWidget(Spinner(), alignment=Qt.AlignmentFlag.AlignVCenter)
    layout.addWidget(Spinner("large", label="Loading the report"), alignment=Qt.AlignmentFlag.AlignVCenter)
    layout.addWidget(Spinner(kind="playful"), alignment=Qt.AlignmentFlag.AlignVCenter)
    layout.addStretch()
    return row
