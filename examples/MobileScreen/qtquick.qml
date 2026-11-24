import QtQuick
import Purrimer

MobileScreen {
    id: screen
    refreshable: true
    // Pretend to fetch for a moment, then end the refresh.
    onRefreshRequested: done.start()
    Timer { id: done; interval: 1200; onTriggered: screen.finishRefresh() }

    appBar: AppBar { title: "Inbox"; large: true; actions: [{ icon: "search", label: "Search" }] }
    fab: FAB { iconName: "pencil"; label: "Compose"; extended: true }
    bottomNav: BottomNav {
        showLabels: true
        selected: 2
        items: [
            { icon: "home", label: "Home" },
            { icon: "search", label: "Search" },
            { icon: "inbox", label: "Inbox", badge: 3 },
            { icon: "person", label: "Profile" }
        ]
    }

    Repeater {
        model: [
            ["Mira Okafor", "Lunch on Friday?"],
            ["Design review", "Notes from today's crit"],
            ["Jonas Weber", "Sent you the photos"],
            ["Book club", "Next one is on the 12th"]
        ]
        ListItem {
            required property var modelData
            width: parent ? parent.width : 0
            iconName: "person"
            headline: modelData[0]
            supporting: modelData[1]
            chevron: true
        }
    }
}
