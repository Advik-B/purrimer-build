import QtQuick
import Purrimer

ActionList {
    width: 288
    items: [
        { group: "Repository" },
        { label: "Code", leadingIcon: "code", current: true },
        { label: "Issues", leadingIcon: "issue-opened", trailingText: "12" },
        { label: "Settings", leadingIcon: "gear", description: "Branches, collaborators, webhooks" },
        { divider: true },
        { label: "Archive repository", leadingIcon: "archive", disabled: true },
        { label: "Delete repository", leadingIcon: "trash", variant: "danger" }
    ]
    onTriggered: (index, item) => console.log("picked", item.label)
}
