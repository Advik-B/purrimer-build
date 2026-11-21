import QtQuick
import Purrimer

Tabs {
    id: tabs
    width: 328
    height: 120
    items: ["Overview", "Activity", "Settings"]
    onActivated: index => selected = index

    Text {
        text: ["Three open issues, two in review.", "Updated 2 hours ago.", "Visible to your team."][tabs.selected]
        color: Purrimer.fgColorDefault
        font: Purrimer.textBodyMedium
    }
}
