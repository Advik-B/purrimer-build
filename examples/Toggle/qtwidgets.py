from purrimer_qt.components import Toggle
from PySide6.QtWidgets import QVBoxLayout, QWidget


def example() -> QWidget:
    column = QWidget()
    layout = QVBoxLayout(column)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(12)
    layout.addWidget(Toggle("Wi-Fi", checked=True))
    bluetooth = Toggle("Bluetooth")
    bluetooth.toggled.connect(lambda on: print("bluetooth", on))
    layout.addWidget(bluetooth)
    airplane = Toggle("Airplane mode")
    airplane.setEnabled(False)
    layout.addWidget(airplane)
    return column
