from purrimer_qt.components import Radio
from PySide6.QtWidgets import QVBoxLayout, QWidget


def example() -> QWidget:
    # Radios with the same parent are exclusive; use a QButtonGroup to split them.
    group = QWidget()
    layout = QVBoxLayout(group)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(12)
    layout.addWidget(Radio("Free"))
    layout.addWidget(Radio("Pro", checked=True))
    team = Radio("Team (invite only)")
    team.setEnabled(False)
    layout.addWidget(team)
    return group
