from purrimer_qt.components import Tabs
from PySide6.QtWidgets import QLabel, QWidget


def example() -> QWidget:
    tabs = Tabs()
    for title, text in [
        ("Overview", "Three open issues, two in review."),
        ("Activity", "Updated 2 hours ago."),
        ("Settings", "Visible to your team."),
    ]:
        tabs.addTab(QLabel(text), title)
    tabs.setFixedHeight(120)
    return tabs
