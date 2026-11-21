import QtQuick
import Purrimer

Item {
    AppBar {
        width: parent.width
        title: "Inbox"
        back: true
        large: true
        actions: [{ icon: "search", label: "Search" }, { icon: "kebab-horizontal", label: "More" }]
        onActionClicked: index => console.log("action", index)
    }
}
