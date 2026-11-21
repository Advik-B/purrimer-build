from purrimer_qt.components import Select
from PySide6.QtWidgets import QWidget


def example() -> QWidget:
    size = Select("T-shirt size", ["Small", "Medium", "Large"], current_index=1)
    size.currentIndexChanged.connect(lambda index: print("size", index))
    return size
