from purrimer_qt.components import Collapse
from purrimer_qt.theme import theme
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


def heading(text: str) -> QLabel:
    label = QLabel(text)
    label.setStyleSheet(theme.text_css("text-title-small"))
    return label


def body(text: str) -> QLabel:
    label = QLabel(text)
    label.setWordWrap(True)
    return label


def example() -> QWidget:
    column = QWidget()
    layout = QVBoxLayout(column)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(8)
    layout.addWidget(heading("Advanced options"))
    advanced = Collapse(open=True)
    advanced.add_widget(body("Signed commits, branch protection and merge queues."))
    layout.addWidget(advanced)
    layout.addWidget(heading("Danger zone"))
    danger = Collapse()
    danger.add_widget(body("Archive or delete this repository."))
    layout.addWidget(danger)
    layout.addStretch()
    return column
