import QtQuick
import Purrimer

Row {
    readonly property var people: ["Mona Lisa", "Hubot", "Ada Lovelace", "Octo Cat", "Grace Hopper", "Linus Torvalds"]
    spacing: 32
    AvatarStack { people: parent.people; anchors.verticalCenter: parent.verticalCenter }
    AvatarStack { people: parent.people.slice(0, 3); size: 32 }
}
