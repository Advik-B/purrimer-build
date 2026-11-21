from purrimer_qt.components import AlertSheet
from PySide6.QtWidgets import QVBoxLayout, QWidget


def example() -> QWidget:
    page = QWidget()
    layout = QVBoxLayout(page)
    layout.setContentsMargins(0, 0, 0, 0)
    # inline draws the sheet in place, for docs; drop it and call open() in an app.
    sheet = AlertSheet(
        page,
        "Delete 3 photos?",
        "They stay in Recently deleted for 30 days, then they are gone for good.",
        icon="critical",
        buttons=[("Cancel", "default"), ("Delete", "danger")],
        inline=True,
    )
    sheet.button_clicked.connect(lambda i: print("button", i))
    layout.addWidget(sheet)
    layout.addStretch()
    return page
