from purrimer_qt.components import AppBar, ListItem, MobileNavigator, MobileScreen
from purrimer_qt.components.mobile_navigator import NavTab
from PySide6.QtWidgets import QLabel, QWidget

THREADS = [
    ("Mira Okafor", "Lunch on Friday?"),
    ("Design review", "Notes from today's crit"),
    ("Jonas Weber", "Sent you the photos"),
]


def inbox(nav: MobileNavigator, _params: object) -> QWidget:
    screen = MobileScreen(app_bar=AppBar("Inbox", large=True))
    for name, text in THREADS:
        item = ListItem(name, text, icon="person", chevron=True, clickable=True)
        item.clicked.connect(lambda n=name, t=text: nav.push("thread", (n, t)))
        screen.body.addWidget(item)
    return screen


def thread(nav: MobileNavigator, params: object) -> QWidget:
    name, text = params
    bar = AppBar(name, back=True)
    bar.backClicked.connect(nav.pop)
    screen = MobileScreen(app_bar=bar)
    note = QLabel(text)
    note.setContentsMargins(16, 16, 16, 16)
    screen.body.addWidget(note)
    return screen


def settings(_nav: MobileNavigator, _params: object) -> QWidget:
    screen = MobileScreen(app_bar=AppBar("Settings", large=True), surface="inset")
    screen.body.addWidget(ListItem("Notifications", icon="bell", trailing="On", chevron=True))
    return screen


def example() -> QWidget:
    return MobileNavigator(
        {"inbox": inbox, "thread": thread, "settings": settings},
        tabs=[NavTab("inbox", "Inbox", "inbox", badge=3), NavTab("settings", "Settings", "gear")],
    )
