from purrimer_qt.components import Chip
from PySide6.QtWidgets import QHBoxLayout, QWidget


def example() -> QWidget:
    row = QWidget()
    layout = QHBoxLayout(row)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(8)
    layout.addWidget(Chip("Design", icon="tag"))
    layout.addWidget(Chip("Shipped", "success"))
    archive = Chip("Archive", "neutral", removable=True)
    archive.removed.connect(archive.deleteLater)
    layout.addWidget(archive)
    layout.addWidget(Chip("Docs", "info"))
    layout.addStretch()
    return row
