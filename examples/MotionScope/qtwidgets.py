from purrimer_qt.components import Card, Motion, MotionScope
from PySide6.QtWidgets import QLabel, QWidget


def card(title: str, text: str) -> Card:
    c = Card(title)
    body = QLabel(text)
    body.setWordWrap(True)
    c.body.addWidget(body)
    return c


def example() -> QWidget:
    playful = MotionScope("playful")
    playful.body.setSpacing(12)
    merged = Motion("pounce")
    merged.add_widget(card("Pull request merged", "All checks passed. Enjoy the quiet."))
    playful.add_widget(merged)
    # The closest scope wins: this one is calm again.
    sleepy = MotionScope("sleepy")
    billing = Motion("rise", index=1)
    billing.add_widget(card("Billing stays sleepy", "Settings and errors never bounce."))
    sleepy.add_widget(billing)
    playful.add_widget(sleepy)
    playful.body.addStretch()
    return playful
