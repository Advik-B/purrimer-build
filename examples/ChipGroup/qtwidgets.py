from purrimer_qt.components import ChipGroup
from purrimer_qt.components.chip_group import ChipOption
from PySide6.QtWidgets import QWidget


def example() -> QWidget:
    chips = ChipGroup(
        [
            ChipOption("all", "All"),
            ChipOption("unread", "Unread", count=12),
            ChipOption("mentions", "Mentions", icon="mention"),
            ChipOption("snoozed", "Snoozed", disabled=True),
        ],
        value="unread",
        accessible_name="Filter inbox",
    )
    chips.changed.connect(lambda value: print("filter", value))
    return chips
