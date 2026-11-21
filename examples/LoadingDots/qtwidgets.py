from purrimer_qt.components import LoadingDots
from PySide6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget


def row(text: str, dots: LoadingDots, gap: int) -> QWidget:
    widget = QWidget()
    layout = QHBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(gap)
    layout.addWidget(QLabel(text))
    layout.addWidget(dots)
    layout.addStretch()
    return widget


def example() -> QWidget:
    column = QWidget()
    layout = QVBoxLayout(column)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(12)
    layout.addWidget(row("Connecting", LoadingDots(), 8))
    layout.addWidget(row("Mona is typing", LoadingDots("snooze"), 4))
    layout.addWidget(row("Fetching treats", LoadingDots(kind="playful"), 8))
    return column
