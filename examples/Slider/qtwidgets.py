from purrimer_qt.components import Slider
from PySide6.QtWidgets import QVBoxLayout, QWidget


def example() -> QWidget:
    column = QWidget()
    layout = QVBoxLayout(column)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(12)
    volume = Slider("Volume", 40, show_value=True, suffix="%")
    volume.valueChanged.connect(lambda value: print("volume", value))
    layout.addWidget(volume)
    layout.addWidget(Slider("Zoom", 50, step=5, page_step=25, tick_position="below"))
    balance = Slider("Balance", 70)
    balance.setEnabled(False)
    layout.addWidget(balance)
    return column
