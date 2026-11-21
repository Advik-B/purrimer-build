import QtQuick
import Purrimer

Row {
    spacing: 24
    Spinner { size: "small"; anchors.verticalCenter: parent.verticalCenter }
    Spinner { anchors.verticalCenter: parent.verticalCenter }
    Spinner { size: "large"; label: "Loading the report" }
    Spinner { kind: "playful"; anchors.verticalCenter: parent.verticalCenter }
}
