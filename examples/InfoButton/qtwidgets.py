from purrimer_qt.components import InfoButton
from PySide6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget


def example() -> QWidget:
    screen = QWidget()
    column = QVBoxLayout(screen)
    column.setContentsMargins(16, 0, 4, 0)
    row = QHBoxLayout()
    row.addWidget(QLabel("Estimated delivery: Tue 14 Jan"), 1)
    row.addWidget(
        InfoButton(
            "Estimated delivery",
            "We work it out from the courier's last scan and their usual times for your area, so it can move by a day.",
            default_open=True,
        )
    )
    column.addLayout(row)
    column.addStretch()
    return screen
