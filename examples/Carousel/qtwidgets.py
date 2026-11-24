from purrimer_qt import theme
from purrimer_qt.components import Carousel
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QWidget

SLIDES = [
    ("Morning walk", "bgColor-accent-muted"),
    ("Market haul", "bgColor-success-muted"),
    ("Rainy afternoon", "bgColor-attention-muted"),
    ("Late train", "bgColor-done-muted"),
]


def example() -> QWidget:
    carousel = Carousel("Highlights", peek=True, slide_height=220)
    for title, tone in SLIDES:
        slide = QLabel(title)
        slide.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
        slide.setIndent(0)
        background = theme.color(tone).name()
        slide.setStyleSheet(theme.text_css("text-body-large") + f"background: {background}; padding: 16px;")
        carousel.add_slide(slide)
    carousel.changed.connect(lambda index: print("slide", index))
    return carousel
