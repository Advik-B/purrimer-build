from purrimer_qt.components import ListItem
from purrimer_qt.components.list_item import SwipeAction
from PySide6.QtWidgets import QVBoxLayout, QWidget


def example() -> QWidget:
    rows = QWidget()
    layout = QVBoxLayout(rows)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)
    notifications = ListItem(
        "Notifications", "Mentions and replies", icon="bell", trailing="On", chevron=True, clickable=True
    )
    notifications.clicked.connect(lambda: print("open notifications"))
    layout.addWidget(notifications)
    layout.addWidget(ListItem("Language", icon="globe", trailing="English"))
    layout.addWidget(
        ListItem(
            "Weekly digest",
            icon="mail",
            trailing="Mon",
            swipe_start=SwipeAction("Mark as read", "check", "accent", lambda: print("read")),
            swipe_end=SwipeAction("Archive", "archive", "success", lambda: print("archive")),
        )
    )
    return rows
