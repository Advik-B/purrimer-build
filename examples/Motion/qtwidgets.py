from purrimer_qt.components import Card, Motion
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

CARDS = [
    ("rise", "Saved to drafts", "Your reply is waiting in Drafts."),
    ("pounce", "New badge", "You reviewed ten pull requests this week."),
    ("bask", "Linked from the release notes", "A halo shows where the link points."),
]


def example() -> QWidget:
    column = QWidget()
    layout = QVBoxLayout(column)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(12)
    for i, (name, title, text) in enumerate(CARDS):
        card = Card(title)
        body = QLabel(text)
        body.setWordWrap(True)
        card.body.addWidget(body)
        motion = Motion(name, index=i, radius=12)
        motion.add_widget(card)
        layout.addWidget(motion)
    layout.addStretch()
    return column
