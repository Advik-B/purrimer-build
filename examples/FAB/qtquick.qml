import QtQuick
import Purrimer

Row {
    spacing: 16
    FAB { label: "New note"; onClicked: console.log("new note") }
    FAB { iconName: "pencil"; label: "Compose"; extended: true }
}
