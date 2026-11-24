from purrimer_qt.components import Chip, Stagger
from PySide6.QtWidgets import QWidget


def example() -> QWidget:
    row = Stagger("pounce", horizontal=True, spacing=8)
    for text, tone in [("Design", "accent"), ("Shipped", "success"), ("Archive", "neutral"), ("Docs", "info")]:
        row.add_widget(Chip(text, tone))
    row.body.addStretch()
    return row
