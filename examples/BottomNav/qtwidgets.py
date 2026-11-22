from purrimer_qt.components import BottomNav
from purrimer_qt.components.bottom_nav import BottomNavItem
from PySide6.QtWidgets import QVBoxLayout, QWidget


def example() -> QWidget:
    screen = QWidget()
    layout = QVBoxLayout(screen)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addStretch()
    nav = BottomNav(
        [
            BottomNavItem("home", "Home"),
            BottomNavItem("search", "Search"),
            BottomNavItem("inbox", "Inbox", badge=3),
            BottomNavItem("bell", "Activity", dot=True),
            BottomNavItem("person", "Profile"),
        ]
    )
    nav.activated.connect(lambda index: print("tab", index))
    layout.addWidget(nav)
    return screen
