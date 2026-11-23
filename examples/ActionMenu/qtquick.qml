import QtQuick
import Purrimer

Item {
    width: 328
    height: 268
    ActionMenu {
        label: "File"
        open: true
        items: [
            { label: "Edit file", leadingIcon: "pencil", trailingText: "E" },
            { label: "Copy permalink", leadingIcon: "link", trailingText: "Y" },
            { label: "View history", leadingIcon: "history" },
            { divider: true },
            { label: "Delete file", leadingIcon: "trash", variant: "danger" }
        ]
        onTriggered: (index, item) => console.log("picked", item.label)
    }
}
