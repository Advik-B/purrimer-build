import QtQuick
import Purrimer

Row {
    spacing: 8
    IconButton { iconName: "pencil"; label: "Edit" }
    IconButton { iconName: "plus"; label: "Add"; variant: "primary" }
    IconButton { iconName: "trash"; label: "Delete"; variant: "danger" }
    IconButton { iconName: "kebab-horizontal"; label: "More"; variant: "invisible" }
    IconButton { iconName: "x"; label: "Close"; size: "small"; anchors.verticalCenter: parent.verticalCenter }
}
