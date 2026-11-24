from purrimer_qt.components import Slider
from purrimer_qt.components.slider import SliderMark
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
    price = Slider("Price", maximum=200, step=10, show_value=True, suffix=" €", range=True, low=40, high=120)
    price.rangeChanged.connect(lambda low, high: print("price", low, high))
    layout.addWidget(price)
    sizes = [SliderMark(1, "S"), SliderMark(2, "M"), SliderMark(3, "L"), SliderMark(4, "XL")]
    layout.addWidget(Slider("Text size", 2, minimum=1, maximum=4, show_value=True, marks=sizes))
    layout.addStretch()
    return column
