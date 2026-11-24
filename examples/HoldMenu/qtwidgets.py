from purrimer_qt.components import FAB, HoldMenu
from purrimer_qt.components.hold_menu import HoldMenuItem
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QLabel, QWidget


def example() -> QWidget:
    screen = QWidget()
    layout = QGridLayout(screen)
    layout.setContentsMargins(16, 16, 16, 16)
    layout.addWidget(QLabel("Hold the button for more ways to start a note."), 0, 0)
    layout.setRowStretch(1, 1)
    fab = FAB(label="New note")
    fab.clicked.connect(lambda: print("new note"))
    menu = HoldMenu(
        fab,
        [
            HoldMenuItem("New note", "note"),
            HoldMenuItem("Take photo", "device-camera"),
            HoldMenuItem("Checklist", "checklist"),
        ],
        accessible_name="Start something",
        default_open=True,
    )
    menu.selected.connect(lambda index: print("chose", index))
    layout.addWidget(fab, 2, 0, Qt.AlignmentFlag.AlignRight)
    return screen
