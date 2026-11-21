import QtQuick
import Purrimer

Flow {
    width: 368
    spacing: 8
    Label { text: "Draft" }
    Label { text: "New"; tone: "accent" }
    Label { text: "Merged"; tone: "success" }
    Label { text: "Pending"; tone: "attention" }
    Label { text: "Failed"; tone: "danger" }
    Label { text: "Closed"; tone: "done" }
}
