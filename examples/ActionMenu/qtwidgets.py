from purrimer_qt.components import ActionMenu
from purrimer_qt.components.action_list import ActionDivider, ActionItem
from PySide6.QtWidgets import QHBoxLayout, QWidget


def example() -> QWidget:
    items = [
        ActionItem("Edit file", leading_icon="pencil", trailing_text="E"),
        ActionItem("Copy permalink", leading_icon="link", trailing_text="Y"),
        ActionItem("View history", leading_icon="history"),
        ActionDivider(),
        ActionItem("Delete file", leading_icon="trash", danger=True),
    ]
    row = QWidget()
    layout = QHBoxLayout(row)
    layout.setContentsMargins(0, 0, 0, 0)
    menu = ActionMenu("File", items, open=True)
    menu.triggered.connect(lambda index: print("picked", items[index].label))
    layout.addWidget(menu)
    layout.addStretch()
    return row
