import QtQuick
import Purrimer

Flow {
    width: 368
    spacing: 8
    Chip { text: "Design"; iconName: "tag" }
    Chip { text: "Shipped"; tone: "success" }
    Chip { id: archive; text: "Archive"; tone: "neutral"; removable: true; onRemoved: archive.visible = false }
    Chip { text: "Docs"; tone: "info" }
}
