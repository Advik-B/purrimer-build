import QtQuick
import Purrimer

Row {
    spacing: 16
    Repeater {
        model: [["Issues", "12", "secondary"], ["Pull requests", "1.2k", "secondary"], ["Review", "3", "primary"]]
        Row {
            required property var modelData
            spacing: 6
            Text {
                text: parent.modelData[0]
                font: Purrimer.textBodyMedium
                color: Purrimer.fgColorDefault
                anchors.verticalCenter: parent.verticalCenter
            }
            CounterLabel { text: parent.modelData[1]; variant: parent.modelData[2]; anchors.verticalCenter: parent.verticalCenter }
        }
    }
}
