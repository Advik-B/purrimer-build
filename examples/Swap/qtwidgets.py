from purrimer_qt.components import Swap
from PySide6.QtWidgets import QLabel, QWidget


def example() -> QWidget:
    # swap.swap(QLabel("Copy link")) would play this label out and the new one in.
    return Swap(QLabel("Copied to clipboard"))
