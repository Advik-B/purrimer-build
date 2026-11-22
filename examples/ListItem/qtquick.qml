import QtQuick
import Purrimer

Column {
    width: 328
    height: 168
    ListItem {
        width: parent.width
        iconName: "bell"
        headline: "Notifications"
        supporting: "Mentions and replies"
        trailing: "On"
        chevron: true
        clickable: true
        onClicked: console.log("open notifications")
    }
    ListItem { width: parent.width; iconName: "globe"; headline: "Language"; trailing: "English" }
    ListItem {
        width: parent.width
        iconName: "mail"
        headline: "Weekly digest"
        trailing: "Mon"
        swipeStart: ({ label: "Mark as read", icon: "check", tone: "accent" })
        swipeEnd: ({ label: "Archive", icon: "archive", tone: "success" })
        onSwiped: (side) => console.log(side === "start" ? "read" : "archive")
    }
}
