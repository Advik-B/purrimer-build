from purrimer_qt.components import Button
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget


def example() -> QWidget:
    column = QWidget()
    layout = QVBoxLayout(column)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(12)

    variants = QHBoxLayout()
    variants.setSpacing(8)
    save = Button("Save", "primary", leading_icon="check")
    save.clicked.connect(lambda: print("saved"))
    variants.addWidget(save)
    variants.addWidget(Button("Cancel"))
    variants.addWidget(Button("Delete", "danger"))
    disabled = Button("Disabled")
    disabled.setEnabled(False)
    variants.addWidget(disabled)
    variants.addStretch()
    layout.addLayout(variants)

    sizes = QHBoxLayout()
    sizes.setSpacing(8)
    sizes.setAlignment(Qt.AlignmentFlag.AlignVCenter)
    sizes.addWidget(Button("Small", size="small"))
    sizes.addWidget(Button("Medium"))
    sizes.addWidget(Button("Large", size="large"))
    sizes.addStretch()
    layout.addLayout(sizes)
    return column
