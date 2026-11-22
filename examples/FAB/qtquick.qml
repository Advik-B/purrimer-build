import QtQuick
import Purrimer

Row {
    spacing: 16
    FAB {
        label: "New note"
        actions: [
            { icon: "device-camera", label: "Take photo" },
            { icon: "checklist", label: "Checklist" }
        ]
        onClicked: console.log("new note")
        onActionSelected: (index) => console.log("chose", index)
    }
    FAB { iconName: "pencil"; label: "Compose"; extended: true }
}
