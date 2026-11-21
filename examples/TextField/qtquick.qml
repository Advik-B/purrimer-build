import QtQuick
import Purrimer

Column {
    spacing: 16
    TextField {
        width: 328
        label: "Email"
        placeholder: "you@example.com"
        caption: "We never share it."
        leadingIcon: "mail"
        inputMethodHints: Qt.ImhEmailCharactersOnly
    }
    TextField {
        width: 328
        label: "Username"
        text: "purr"
        error: text === "purr" ? "That name is taken." : ""
    }
}
