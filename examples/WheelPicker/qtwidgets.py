from purrimer_qt.components import WheelPicker
from purrimer_qt.components.wheel_picker import WheelColumn
from PySide6.QtWidgets import QWidget


def example() -> QWidget:
    hours = [f"{h:02d}" for h in range(1, 13)]
    minutes = [f"{m:02d}" for m in range(0, 60, 5)]
    picker = WheelPicker(
        [
            WheelColumn("Hour", hours, "07", align="end"),
            WheelColumn("Minute", minutes, "30"),
            WheelColumn("AM or PM", ["AM", "PM"], "AM", align="start"),
        ]
    )
    picker.changed.connect(lambda column, value: print("column", column, value))
    return picker
