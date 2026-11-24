from purrimer_qt.components import ActionSheet
from purrimer_qt.components.action_sheet import ActionSheetItem
from PySide6.QtWidgets import QVBoxLayout, QWidget


def example() -> QWidget:
    page = QWidget()
    layout = QVBoxLayout(page)
    layout.setContentsMargins(0, 0, 0, 0)
    items = [
        ActionSheetItem("Share", icon="share-android"),
        ActionSheetItem("Copy link", "Anyone with the link can view", icon="link"),
        ActionSheetItem(
            "Move to", icon="file-directory", items=[ActionSheetItem("Holidays"), ActionSheetItem("Family")]
        ),
        ActionSheetItem("Favourite", icon="star", checked=True),
        ActionSheetItem(divider=True),
        ActionSheetItem("Delete", icon="trash", variant="danger"),
    ]
    # inline draws the sheet in place, for docs; drop it and call open() in an app.
    sheet = ActionSheet(page, items, "Photo.jpg", inline=True)
    sheet.selected.connect(lambda item, _i: print("chose", item.label))
    layout.addWidget(sheet)
    layout.addStretch()
    return page
