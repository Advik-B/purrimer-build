import QtQuick
import Purrimer

Column {
    spacing: 12
    Row {
        spacing: 8
        Text { text: "Connecting"; font: Purrimer.textBodyMedium; color: Purrimer.fgColorDefault; anchors.verticalCenter: parent.verticalCenter }
        LoadingDots { anchors.verticalCenter: parent.verticalCenter }
    }
    Row {
        spacing: 4
        Text { text: "Mona is typing"; font: Purrimer.textBodyMedium; color: Purrimer.fgColorDefault; anchors.verticalCenter: parent.verticalCenter }
        LoadingDots { variant: "snooze"; anchors.verticalCenter: parent.verticalCenter }
    }
    Row {
        spacing: 8
        Text { text: "Fetching treats"; font: Purrimer.textBodyMedium; color: Purrimer.fgColorDefault; anchors.verticalCenter: parent.verticalCenter }
        LoadingDots { kind: "playful"; anchors.verticalCenter: parent.verticalCenter }
    }
}
