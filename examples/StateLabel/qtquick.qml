import QtQuick
import Purrimer

Row {
    spacing: 8
    StateLabel { status: "open"; text: "Open" }
    StateLabel { status: "closed"; text: "Closed" }
    StateLabel { status: "merged"; text: "Merged" }
    StateLabel { status: "draft"; size: "small"; text: "Draft"; anchors.verticalCenter: parent.verticalCenter }
}
