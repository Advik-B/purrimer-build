import QtQuick
import Purrimer

Item {
    ListSection {
        y: 16
        width: parent.width
        header: "Account"
        ListItem { width: parent.width; iconName: "person"; headline: "Profile"; chevron: true }
        ListItem { width: parent.width; iconName: "key"; headline: "Password"; chevron: true }
    }
}
