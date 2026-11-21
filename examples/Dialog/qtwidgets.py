from purrimer_qt.components import Button, Dialog
from PySide6.QtWidgets import QLabel, QWidget


def example() -> QWidget:
    # Dialog is a QDialog: show it with dialog.open() or dialog.exec().
    dialog = Dialog("Delete repository?", width=328)
    body = QLabel("This deletes purrimer-build and its history for good.")
    body.setWordWrap(True)
    dialog.body.addWidget(body)
    cancel = Button("Cancel")
    cancel.clicked.connect(dialog.reject)
    delete = Button("Delete", "danger")
    delete.clicked.connect(dialog.accept)
    dialog.footer.addWidget(cancel)
    dialog.footer.addWidget(delete)
    return dialog
