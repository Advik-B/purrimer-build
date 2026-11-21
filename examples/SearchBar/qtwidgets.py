from purrimer_qt.components import SearchBar
from PySide6.QtWidgets import QVBoxLayout, QWidget


def example() -> QWidget:
    column = QWidget()
    layout = QVBoxLayout(column)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(16)
    search = SearchBar(placeholder="Search messages")
    search.returnPressed.connect(lambda: print("search", search.text()))
    layout.addWidget(search)
    layout.addWidget(SearchBar("kittens"))
    return column
