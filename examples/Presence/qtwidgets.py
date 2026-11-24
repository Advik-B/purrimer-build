from purrimer_qt.components import Card, Presence
from PySide6.QtWidgets import QLabel, QWidget


def example() -> QWidget:
    card = Card("Draft saved")
    body = QLabel("It leaves with lie-down when dismissed.")
    body.setWordWrap(True)
    card.body.addWidget(body)
    presence = Presence(collapse=True)
    presence.add_widget(card)
    # presence.set_show(False) plays the exit, then hides it and closes the gap.
    return presence
