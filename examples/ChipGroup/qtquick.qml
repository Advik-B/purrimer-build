import QtQuick
import Purrimer

ChipGroup {
    width: 440
    accessibleName: "Filter inbox"
    options: [
        { value: "all", label: "All" },
        { value: "unread", label: "Unread", count: 12 },
        { value: "mentions", label: "Mentions", icon: "mention" },
        { value: "snoozed", label: "Snoozed", disabled: true }
    ]
    value: "unread"
    onChanged: (value) => console.log("filter", value)
}
