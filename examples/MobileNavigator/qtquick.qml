pragma ComponentBehavior: Bound
import QtQuick
import Purrimer

MobileNavigator {
    tabs: [
        { screen: "inbox", label: "Inbox", icon: "inbox", badge: 3 },
        { screen: "settings", label: "Settings", icon: "gear" }
    ]
    screens: ({ inbox: inbox, thread: thread, settings: settings })

    Component {
        id: inbox
        MobileScreen {
            id: inboxScreen
            property var nav
            property var params
            property bool active
            appBar: AppBar { title: "Inbox"; large: true }
            Repeater {
                model: [["Mira Okafor", "Lunch on Friday?"], ["Design review", "Notes from today's crit"], ["Jonas Weber", "Sent you the photos"]]
                ListItem {
                    required property var modelData
                    width: parent ? parent.width : 0
                    iconName: "person"
                    headline: modelData[0]
                    supporting: modelData[1]
                    chevron: true
                    clickable: true
                    onClicked: inboxScreen.nav.push("thread", modelData)
                }
            }
        }
    }

    Component {
        id: thread
        MobileScreen {
            id: threadScreen
            property var nav
            property var params
            property bool active
            appBar: AppBar { title: threadScreen.params[0]; back: true; onBackClicked: threadScreen.nav.pop() }
            Text {
                x: 16
                y: 16
                text: threadScreen.params[1]
                color: Purrimer.fgColorDefault
                font: Purrimer.textBodyMedium
            }
        }
    }

    Component {
        id: settings
        MobileScreen {
            property var nav
            property var params
            property bool active
            surface: "inset"
            appBar: AppBar { title: "Settings"; large: true }
            ListItem { width: parent ? parent.width : 0; iconName: "bell"; headline: "Notifications"; trailing: "On"; chevron: true }
        }
    }
}
