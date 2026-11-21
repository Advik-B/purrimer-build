from purrimer_qt.components import ProgressBar
from PySide6.QtWidgets import QVBoxLayout, QWidget


def example() -> QWidget:
    # ProgressBar(indeterminate=True) sweeps while the amount is unknown.
    column = QWidget()
    layout = QVBoxLayout(column)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(16)
    layout.addWidget(ProgressBar(40))
    layout.addWidget(ProgressBar(75, "success"))
    layout.addWidget(ProgressBar(95, "danger"))
    return column
