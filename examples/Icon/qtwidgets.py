from purrimer_qt.components import Icon
from PySide6.QtWidgets import QHBoxLayout, QWidget


def example() -> QWidget:
    row = QWidget()
    layout = QHBoxLayout(row)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(16)
    layout.addWidget(Icon("heart"))
    layout.addWidget(Icon("star"))
    layout.addWidget(Icon("bell"))
    layout.addWidget(Icon("bell", 24))
    layout.addWidget(Icon("heart", 24, color="fgColor-danger"))
    layout.addStretch()
    return row
