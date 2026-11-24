from purrimer_qt.components import TextReveal
from PySide6.QtWidgets import QVBoxLayout, QWidget


def example() -> QWidget:
    column = QWidget()
    layout = QVBoxLayout(column)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(12)
    layout.addWidget(TextReveal("All caught up today."))
    layout.addWidget(TextReveal("Branch ready", effect="tangle", text_style="text-title-medium"))
    layout.addStretch()
    return column
