from purrimer_qt.components import Timeline
from purrimer_qt.components.timeline import TimelineBreak, TimelineEvent
from PySide6.QtWidgets import QWidget


def example() -> QWidget:
    return Timeline(
        [
            TimelineEvent("opened this pull request", "mona", "git-pull-request", "success"),
            TimelineEvent("added 3 commits", "hubot", "git-commit", condensed=True),
            TimelineEvent("approved these changes", "ada", "check", "accent"),
            TimelineBreak(),
            TimelineEvent("merged into main", "mona", "git-merge", "done"),
        ]
    )
