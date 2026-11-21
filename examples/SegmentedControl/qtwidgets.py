from purrimer_qt.components import SegmentedControl
from PySide6.QtWidgets import QWidget


def example() -> QWidget:
    view = SegmentedControl(["Day", "Week", "Month"], selected=1)
    view.activated.connect(lambda index: print("view", index))
    return view
