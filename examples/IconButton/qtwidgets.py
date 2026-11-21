from purrimer_qt.components import IconButton
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QWidget


def example() -> QWidget:
    row = QWidget()
    layout = QHBoxLayout(row)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(8)
    layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
    layout.addWidget(IconButton("pencil", "Edit"))
    layout.addWidget(IconButton("plus", "Add", "primary"))
    layout.addWidget(IconButton("trash", "Delete", "danger"))
    layout.addWidget(IconButton("kebab-horizontal", "More", "invisible"))
    layout.addWidget(IconButton("x", "Close", size="small"))
    layout.addStretch()
    return row
