import QtQuick
import Purrimer

Row {
    spacing: 16
    Icon { name: "heart"; anchors.verticalCenter: parent.verticalCenter }
    Icon { name: "star"; anchors.verticalCenter: parent.verticalCenter }
    Icon { name: "bell"; anchors.verticalCenter: parent.verticalCenter }
    Icon { name: "bell"; size: 24 }
    Icon { name: "heart"; size: 24; color: Purrimer.fgColorDanger }
}
