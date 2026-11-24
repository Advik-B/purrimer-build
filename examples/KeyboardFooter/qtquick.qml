import QtQuick
import Purrimer

MobileScreen {
    appBar: AppBar { title: "New task"; back: true }
    footer: KeyboardFooter {
        Button { text: "Add task"; variant: "primary" }
    }

    Item {
        width: parent.width
        height: field.implicitHeight + 16
        TextField {
            id: field
            x: 16
            y: 16
            width: parent.width - 32
            label: "Title"
            text: "Water the plants"
        }
    }
}
