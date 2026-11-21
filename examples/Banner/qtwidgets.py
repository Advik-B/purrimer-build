from purrimer_qt.components import Banner
from PySide6.QtWidgets import QVBoxLayout, QWidget


def example() -> QWidget:
    column = QWidget()
    layout = QVBoxLayout(column)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(12)
    deployed = Banner("success", "Deployed", "Version 2.4 is live for everyone.", dismissible=True)
    deployed.dismissed.connect(deployed.hide)
    layout.addWidget(deployed)
    layout.addWidget(Banner("danger", text="The build failed on two checks."))
    return column
