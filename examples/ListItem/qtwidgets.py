from purrimer_qt.components import ListItem
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
    return rows
