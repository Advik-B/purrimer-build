from purrimer_qt.components import Textarea
from PySide6.QtWidgets import QVBoxLayout, QWidget


def example() -> QWidget:
    column = QWidget()
    layout = QVBoxLayout(column)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(16)
    layout.addWidget(
        Textarea("Bio", placeholder="Tell us a little about yourself", caption="Shown on your public profile.")
    )
    layout.addWidget(Textarea("Why are you closing this?", rows=2, error="Add a short reason."))
    return column
