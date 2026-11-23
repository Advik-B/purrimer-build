from purrimer_qt.components import ActionList
from purrimer_qt.components.action_list import ActionDivider, ActionGroup, ActionItem
from PySide6.QtWidgets import QWidget


def example() -> QWidget:
    items = [
        ActionGroup("Repository"),
        ActionItem("Code", leading_icon="code", current=True),
        ActionItem("Issues", leading_icon="issue-opened", trailing_text="12"),
        ActionItem("Settings", "Branches, collaborators, webhooks", leading_icon="gear"),
        ActionDivider(),
        ActionItem("Archive repository", leading_icon="archive", disabled=True),
        ActionItem("Delete repository", leading_icon="trash", danger=True),
    ]
    actions = ActionList(items)
    actions.triggered.connect(lambda index: print("picked", items[index].label))
    return actions
