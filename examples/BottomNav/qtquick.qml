import QtQuick
import Purrimer

Item {
    BottomNav {
        anchors.bottom: parent.bottom
        width: parent.width
        showLabels: true
        items: [
            { icon: "home", label: "Home" },
            { icon: "search", label: "Search" },
            { icon: "inbox", label: "Inbox", badge: 3 },
            { icon: "bell", label: "Activity", badge: true },
            { icon: "person", label: "Profile" }
        ]
        onActivated: index => selected = index
    }
}
