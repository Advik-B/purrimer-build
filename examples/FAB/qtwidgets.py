from purrimer_qt.components import FAB
from purrimer_qt.components.hold_menu import HoldMenuItem
from PySide6.QtWidgets import QHBoxLayout, QWidget


def example() -> QWidget:
    row = QWidget()
    layout = QHBoxLayout(row)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(16)
    note = FAB(
        label="New note",
        actions=[HoldMenuItem("Take photo", "device-camera"), HoldMenuItem("Checklist", "checklist")],
    )
    note.clicked.connect(lambda: print("new note"))
    note.action_selected.connect(lambda index: print("chose", index))
    layout.addWidget(note)
    layout.addWidget(FAB("pencil", "Compose", extended=True))
    layout.addStretch()
    return row
