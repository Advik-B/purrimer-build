import QtQuick
import Purrimer

Column {
    spacing: 16
    SearchBar { width: 328; placeholderText: "Search messages"; onAccepted: console.log("search", text) }
    SearchBar { width: 328; text: "kittens" }
}
