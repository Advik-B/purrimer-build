from purrimer_qt.components import BottomSheet, Button
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


def example() -> QWidget:
    screen = QWidget()
    layout = QVBoxLayout(screen)
    layout.setContentsMargins(16, 16, 16, 16)
    layout.addWidget(QLabel("Photo.jpg"))
    layout.addStretch()

    # The sheet draws over its parent, so give it the screen widget.
    sheet = BottomSheet(screen, "Share", "Photo.jpg, 2.4 MB")
    note = QLabel("Anyone with the link can view this photo.")
    note.setWordWrap(True)
    sheet.body.addWidget(note)
    copy = Button("Copy link", "primary", block=True)
    copy.clicked.connect(sheet.close_sheet)
    sheet.add_action(copy)
    QTimer.singleShot(0, sheet.open)  # open once the screen is shown and has its size
    return screen
