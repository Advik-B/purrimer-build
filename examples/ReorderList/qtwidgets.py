from purrimer_qt.components import ReorderList
from purrimer_qt.components.reorder_list import ReorderItem
from PySide6.QtWidgets import QVBoxLayout, QWidget


def example() -> QWidget:
    page = QWidget()
    layout = QVBoxLayout(page)
    layout.setContentsMargins(0, 16, 0, 0)
    sections = ReorderList(
        [
            ReorderItem("today", "Today", "Tasks due today", icon="calendar"),
            ReorderItem("inbox", "Inbox", icon="inbox"),
            ReorderItem("starred", "Starred", icon="star"),
            ReorderItem("shared", "Shared with me", "From 3 people", icon="people"),
        ],
        accessible_name="Home sections",
    )
    sections.reordered.connect(lambda from_, to: print("moved", from_, to))
    layout.addWidget(sections)
    layout.addStretch()
    return page
