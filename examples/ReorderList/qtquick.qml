import QtQuick
import Purrimer

Item {
    width: 358
    height: 268

    ReorderList {
        y: 16
        width: parent.width
        accessibleName: "Home sections"
        items: [
            { key: "today", headline: "Today", supporting: "Tasks due today", icon: "calendar" },
            { key: "inbox", headline: "Inbox", icon: "inbox" },
            { key: "starred", headline: "Starred", icon: "star" },
            { key: "shared", headline: "Shared with me", supporting: "From 3 people", icon: "people" }
        ]
        onReordered: (from, to) => console.log("moved", from, to)
    }
}
