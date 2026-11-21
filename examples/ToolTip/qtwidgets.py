from purrimer_qt.components import IconButton, ToolTip
from PySide6.QtWidgets import QHBoxLayout, QWidget


def example() -> QWidget:
    row = QWidget()
    layout = QHBoxLayout(row)
    layout.setContentsMargins(0, 40, 0, 0)
    layout.setSpacing(8)
    edit = IconButton("pencil", "Edit")
    copy = IconButton("copy", "Copy")
    delete = IconButton("trash", "Delete")
    help_button = IconButton("question", "What is this?")
    for button in (edit, delete, copy, help_button):
        layout.addWidget(button)
    layout.addStretch()
    # The tips stay attached to their buttons; keep a reference only if you need to change them later.
    ToolTip(edit, "Edit")
    ToolTip(copy, "Copy to clipboard (Ctrl+C)", open=True)
    ToolTip(delete, "Delete")
    ToolTip(help_button, "Tokens are named design decisions that every target reads.", "bottom", whats_this=True)
    return row
