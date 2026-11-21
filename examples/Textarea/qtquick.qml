import QtQuick
import Purrimer

Column {
    width: 328
    spacing: 16
    Textarea {
        width: parent.width
        label: "Bio"
        placeholder: "Tell us a little about yourself"
        caption: "Shown on your public profile."
    }
    Textarea {
        width: parent.width
        label: "Why are you closing this?"
        rows: 2
        error: "Add a short reason."
    }
}
