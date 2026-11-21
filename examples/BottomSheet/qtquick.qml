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
        Component.onCompleted: open()

        Column {
            width: parent.width
            spacing: 16
            Text {
                width: parent.width
                wrapMode: Text.Wrap
                text: "Anyone with the link can view this photo."
                color: Purrimer.fgColorDefault
                font: Purrimer.textBodyMedium
            }
            Button { width: parent.width; text: "Copy link"; variant: "primary"; onClicked: sheet.close() }
        }
    }
}
