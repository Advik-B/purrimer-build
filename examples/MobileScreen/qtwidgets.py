from purrimer_qt.components import FAB, AppBar, BottomNav, ListItem, MobileScreen
from purrimer_qt.components.bottom_nav import BottomNavItem
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QWidget

THREADS = [
    ("Mira Okafor", "Lunch on Friday?"),
    ("Design review", "Notes from today's crit"),
    ("Jonas Weber", "Sent you the photos"),
    ("Book club", "Next one is on the 12th"),
]


def example() -> QWidget:
    nav = BottomNav(
        [
            BottomNavItem("home", "Home"),
            BottomNavItem("search", "Search"),
            BottomNavItem("inbox", "Inbox", badge=3),
            BottomNavItem("person", "Profile"),
        ],
        selected=2,
    )
    screen = MobileScreen(
        app_bar=AppBar("Inbox", large=True, actions=[("search", "Search")]),
        bottom_nav=nav,
        fab=FAB("pencil", "Compose", extended=True),
        refreshable=True,
    )
    for headline, supporting in THREADS:
        screen.body.addWidget(ListItem(headline, supporting, icon="person", chevron=True, clickable=True))
    # Pretend to fetch for a moment, then end the refresh.
    screen.refresh_requested.connect(lambda: QTimer.singleShot(1200, screen.finish_refresh))
    return screen
