from purrimer_qt.components import Card
from PySide6.QtWidgets import QLabel, QWidget


def example() -> QWidget:
    card = Card("Weekly digest")
    body = QLabel("Three new comments and one review are waiting for you.")
    body.setWordWrap(True)
    card.body.addWidget(body)
    return card
