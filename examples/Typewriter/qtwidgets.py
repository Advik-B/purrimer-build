from purrimer_qt.components import Typewriter
from PySide6.QtWidgets import QWidget


def example() -> QWidget:
    return Typewriter("Good morning. Ready when you are.", caret="always", text_style="text-body-large")
