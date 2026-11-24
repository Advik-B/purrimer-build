import QtQuick
import Purrimer

Item {
    width: 358
    height: 480

    // inline draws the sheet in place, for docs; drop it and call open() in an app.
    ActionSheet {
        inline: true
        title: "Photo.jpg"
        items: [
            { label: "Share", icon: "share-android" },
            { label: "Copy link", icon: "link", description: "Anyone with the link can view" },
            { label: "Move to", icon: "file-directory", items: [{ label: "Holidays" }, { label: "Family" }] },
            { label: "Favourite", icon: "star", checked: true },
            { divider: true },
            { label: "Delete", icon: "trash", variant: "danger" }
        ]
        onSelected: (item) => console.log("chose", item.label)
    }
}
