import QtQuick
import Purrimer

Row {
    spacing: 8
    topPadding: 40
    ToolTip { text: "Edit"; IconButton { iconName: "pencil"; label: "Edit" } }
    ToolTip { text: "Delete"; IconButton { iconName: "trash"; label: "Delete" } }
    ToolTip { text: "Copy to clipboard (Ctrl+C)"; open: true; IconButton { iconName: "copy"; label: "Copy" } }
    ToolTip {
        text: "Tokens are named design decisions that every target reads."
        whatsThis: true
        placement: "bottom"
        IconButton { iconName: "question"; label: "What is this?" }
    }
}
