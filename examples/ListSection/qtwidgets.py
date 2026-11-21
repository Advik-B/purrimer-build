from purrimer_qt.components import ListItem, ListSection
from PySide6.QtWidgets import QVBoxLayout, QWidget


def example() -> QWidget:
    screen = QWidget()
    layout = QVBoxLayout(screen)
    layout.setContentsMargins(0, 16, 0, 0)
    account = ListSection("Account")
    account.add_item(ListItem("Profile", icon="person", chevron=True))
    account.add_item(ListItem("Password", icon="key", chevron=True))
    layout.addWidget(account)
    layout.addStretch()
    return screen
