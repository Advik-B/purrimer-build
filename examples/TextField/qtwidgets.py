from purrimer_qt.components import TextField
from PySide6.QtWidgets import QVBoxLayout, QWidget


def example() -> QWidget:
    column = QWidget()
    layout = QVBoxLayout(column)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(16)
    email = TextField("Email", placeholder="you@example.com", caption="We never share it.", leading_icon="mail")
    username = TextField("Username", "purr", error="That name is taken.")
    username.textChanged.connect(lambda text: username.set_error("That name is taken." if text == "purr" else ""))
    layout.addWidget(email)
    layout.addWidget(username)
    return column
