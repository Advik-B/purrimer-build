from purrimer_qt.components import Checkbox
from PySide6.QtWidgets import QVBoxLayout, QWidget


def example() -> QWidget:
    column = QWidget()
    layout = QVBoxLayout(column)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(12)
    replies = Checkbox("Email me about replies", checked=True)
    replies.toggled.connect(lambda on: print("replies", on))
    layout.addWidget(replies)
    layout.addWidget(Checkbox("Weekly digest"))
    beta = Checkbox("Beta features (coming soon)")
    beta.setEnabled(False)
    layout.addWidget(beta)
    return column
