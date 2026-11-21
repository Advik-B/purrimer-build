import QtQuick
import Purrimer

Item {
    width: 358
    height: 308

    Row {
        x: 16
        width: parent.width - 20
        Text {
            width: parent.width - info.width
            anchors.verticalCenter: parent.verticalCenter
            text: "Estimated delivery: Tue 14 Jan"
            color: Purrimer.fgColorDefault
            font: Purrimer.textBodyMedium
        }
        InfoButton {
            id: info
            defaultOpen: true
            title: "Estimated delivery"
            message: "We work it out from the courier's last scan and their usual times for your area, so it can move by a day."
        }
    }
}
