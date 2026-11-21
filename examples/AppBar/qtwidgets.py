from purrimer_qt.components import AppBar
from PySide6.QtWidgets import QVBoxLayout, QWidget


def example() -> QWidget:
    screen = QWidget()
    layout = QVBoxLayout(screen)
    layout.setContentsMargins(0, 0, 0, 0)
    bar = AppBar("Inbox", back=True, large=True, actions=[("search", "Search"), ("kebab-horizontal", "More")])
    bar.actionClicked.connect(lambda index: print("action", index))
    layout.addWidget(bar)
    layout.addStretch()
    return screen
