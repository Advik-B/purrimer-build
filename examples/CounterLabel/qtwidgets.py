from purrimer_qt.components import CounterLabel
from PySide6.QtWidgets import QHBoxLayout, QLabel, QWidget


def example() -> QWidget:
    row = QWidget()
    layout = QHBoxLayout(row)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(6)
    for text, count, variant in (
        ("Issues", "12", "secondary"),
        ("Pull requests", "1.2k", "secondary"),
        ("Review", 3, "primary"),
    ):
        layout.addWidget(QLabel(text))
        layout.addWidget(CounterLabel(count, variant))
        layout.addSpacing(10)
    layout.addStretch()
    return row
