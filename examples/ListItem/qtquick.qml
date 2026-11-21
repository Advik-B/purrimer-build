import QtQuick
import Purrimer

Column {
    width: 328
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
}
