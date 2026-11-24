from purrimer_qt.components import Burst, Card, MotionScope
from PySide6.QtWidgets import QLabel, QWidget


def example() -> QWidget:
    scope = MotionScope("playful")
    burst = Burst()
    card = Card("Pull request merged")
    card.body.addWidget(QLabel("All checks passed."))
    burst.add_widget(card)
    scope.add_widget(burst)
    # burst.fire() throws confetti from the card.
    return scope
