from purrimer_qt.components import Skeleton
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget


def example() -> QWidget:
    column = QWidget()
    layout = QVBoxLayout(column)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(16)
    row = QHBoxLayout()
    row.setSpacing(12)
    row.addWidget(Skeleton("circle"))
    row.addWidget(Skeleton(lines=2), 1)
    layout.addLayout(row)
    layout.addWidget(Skeleton("block", effect="snore"))
    return column
