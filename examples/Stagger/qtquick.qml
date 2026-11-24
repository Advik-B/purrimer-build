import QtQuick
import Purrimer

Stagger {
    name: "pounce"
    horizontal: true
    spacing: 8
    model: [["Design", "accent"], ["Shipped", "success"], ["Archive", "neutral"], ["Docs", "info"]]
    delegate: Chip {
        property var modelData: ["", "accent"]
        text: modelData[0]
        tone: modelData[1]
    }
}
