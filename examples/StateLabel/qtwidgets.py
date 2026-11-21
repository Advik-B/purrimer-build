from purrimer_qt.components import StateLabel
from PySide6.QtWidgets import QHBoxLayout, QWidget


def example() -> QWidget:
    row = QWidget()
    layout = QHBoxLayout(row)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(8)
    layout.addWidget(StateLabel("Open", "open"))
    layout.addWidget(StateLabel("Closed", "closed"))
    layout.addWidget(StateLabel("Merged", "merged"))
    layout.addWidget(StateLabel("Draft", "draft", size="small"))
    layout.addStretch()
    return row
