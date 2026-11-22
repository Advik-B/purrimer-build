import QtQuick
import Purrimer

Item {
    width: 390
    height: 420

    Text {
        x: 16
        y: 16
        text: "Hold the button for more ways to start a note."
        color: Purrimer.fgColorDefault
        font: Purrimer.textBodyMedium
    }

    HoldMenu {
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.margins: 16
        defaultOpen: true
        accessibleName: "Start something"
        items: [
            { label: "New note", icon: "note" },
            { label: "Take photo", icon: "device-camera" },
            { label: "Checklist", icon: "checklist" }
        ]
        onSelected: (index) => console.log("chose", index)

        FAB {
            label: "New note"
            onClicked: console.log("new note")
        }
    }
}
