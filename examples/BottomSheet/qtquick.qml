import QtQuick
import Purrimer

Item {
    Text {
        x: 16; y: 16
        text: "Photo.jpg"
        color: Purrimer.fgColorDefault
        font: Purrimer.textBodyMedium
    }

    BottomSheet {
        id: sheet
        title: "Share"
        description: "Photo.jpg, 2.4 MB"
        Component.onCompleted: open()

        Text {
            width: parent.width
            wrapMode: Text.Wrap
            text: "Anyone with the link can view this photo."
            color: Purrimer.fgColorDefault
            font: Purrimer.textBodyMedium
        }

        actions: [
            Button { text: "Copy link"; variant: "primary"; onClicked: sheet.close() }
        ]
    }
}
