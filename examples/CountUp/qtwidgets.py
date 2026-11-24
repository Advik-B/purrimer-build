from purrimer_qt.components import CountUp
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QWidget


def example() -> QWidget:
    row = QWidget()
    layout = QHBoxLayout(row)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(32)
    layout.addWidget(CountUp(1284), alignment=Qt.AlignmentFlag.AlignBottom)
    balance = CountUp(3742.5, decimals=2, prefix="€", mode="roll", text_style="text-stat-small")
    layout.addWidget(balance, alignment=Qt.AlignmentFlag.AlignBottom)
    layout.addStretch()
    return row
