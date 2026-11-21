import QtQuick
import Purrimer

Item {
    Text {
        x: 16; y: 16
        text: "Repository settings"
        color: Purrimer.fgColorDefault
        font: Purrimer.textBodyMedium
    }

    Dialog {
        id: dialog
        title: "Delete repository?"
        Component.onCompleted: open()

        Text {
            width: parent.width
            wrapMode: Text.Wrap
            text: "This deletes purrimer-build and its history for good."
            color: Purrimer.fgColorDefault
            font: Purrimer.textBodyMedium
        }

        footer: [
            Button { text: "Cancel"; onClicked: dialog.close() },
            Button { text: "Delete"; variant: "danger"; onClicked: dialog.close() }
        ]
    }
}
