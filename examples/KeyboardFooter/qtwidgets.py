from purrimer_qt.components import AppBar, Button, KeyboardFooter, MobileScreen, TextField
from PySide6.QtWidgets import QWidget


def example() -> QWidget:
    footer = KeyboardFooter()
    footer.add_button(Button("Add task", "primary", block=True))
    screen = MobileScreen(app_bar=AppBar("New task", back=True), footer=footer)
    field = TextField("Title", "Water the plants")
    field.setContentsMargins(16, 16, 16, 0)
    screen.body.addWidget(field)
    return screen
