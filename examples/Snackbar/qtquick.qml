import QtQuick
import Purrimer

Item {
    Text {
        x: 16; y: 16
        text: "Inbox"
        color: Purrimer.fgColorDefault
        font: Purrimer.textBodyMedium
    }

    Snackbar {
        message: "Message archived"
        action: "Undo"
        onActionTriggered: console.log("undo")
        Component.onCompleted: open()
    }
}
