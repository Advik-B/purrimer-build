from purrimer_qt.components import UnderlineNav
from purrimer_qt.components.underline_nav import NavItem
from PySide6.QtWidgets import QWidget


def example() -> QWidget:
    nav = UnderlineNav(
        [
            NavItem("Code", "code"),
            NavItem("Issues", "issue-opened", 12),
            NavItem("Pull requests", "git-pull-request", 3),
            NavItem("Actions", "play"),
        ]
    )
    nav.currentChanged.connect(lambda index: print("page", index))
    return nav
