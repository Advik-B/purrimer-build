from purrimer_qt.components import Snackbar
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


def example() -> QWidget:
    screen = QWidget()
    layout = QVBoxLayout(screen)
    layout.setContentsMargins(16, 16, 16, 16)
    layout.addWidget(QLabel("Inbox"))
    layout.addStretch()
    snackbar = Snackbar()
    snackbar.actionTriggered.connect(lambda: print("undo"))
    layout.addWidget(snackbar)
    # Above the bottom bar, as on a phone screen.
    layout.addSpacing(56)
    QTimer.singleShot(0, lambda: snackbar.show_message("Message archived", "Undo"))
    return screen
