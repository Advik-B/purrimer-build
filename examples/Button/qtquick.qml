import QtQuick
import Purrimer

Column {
    spacing: 12
    Row {
        spacing: 8
        Button { text: "Save"; variant: "primary"; leadingIcon: "check"; onClicked: console.log("saved") }
        Button { text: "Cancel" }
        Button { text: "Delete"; variant: "danger" }
        Button { text: "Disabled"; enabled: false }
    }
    Row {
        spacing: 8
        Button { text: "Small"; size: "small"; anchors.verticalCenter: parent.verticalCenter }
        Button { text: "Medium"; anchors.verticalCenter: parent.verticalCenter }
        Button { text: "Large"; size: "large" }
    }
}
