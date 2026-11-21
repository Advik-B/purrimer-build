from purrimer_qt.components import FAB
from PySide6.QtWidgets import QHBoxLayout, QWidget


def example() -> QWidget:
    row = QWidget()
    layout = QHBoxLayout(row)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(16)
    note = FAB(label="New note")
    note.clicked.connect(lambda: print("new note"))
    layout.addWidget(note)
    layout.addWidget(FAB("pencil", "Compose", extended=True))
    layout.addStretch()
    return row
