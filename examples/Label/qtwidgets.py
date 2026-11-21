from purrimer_qt.components import Label
from PySide6.QtWidgets import QHBoxLayout, QWidget


def example() -> QWidget:
    row = QWidget()
    layout = QHBoxLayout(row)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(8)
    for text, tone in [
        ("Draft", "default"),
        ("New", "accent"),
        ("Merged", "success"),
        ("Pending", "attention"),
        ("Failed", "danger"),
        ("Closed", "done"),
    ]:
        layout.addWidget(Label(text, tone))
    layout.addStretch()
    return row
