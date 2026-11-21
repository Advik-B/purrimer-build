pragma ComponentBehavior: Bound
import QtQuick
import Purrimer

Carousel {
    id: carousel
    width: 358
    accessibleName: "Highlights"
    peek: true
    slideHeight: 220
    model: [
        { title: "Morning walk", tone: Purrimer.bgColorAccentMuted },
        { title: "Market haul", tone: Purrimer.bgColorSuccessMuted },
        { title: "Rainy afternoon", tone: Purrimer.bgColorAttentionMuted },
        { title: "Late train", tone: Purrimer.bgColorDoneMuted }
    ]
    delegate: Rectangle {
        required property var modelData
        width: carousel.slideWidth
        height: carousel.slideHeight
        radius: 12
        color: modelData.tone
        Text {
            x: 16
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 16
            text: parent.modelData.title
            color: Purrimer.fgColorDefault
            font.pixelSize: 16
        }
    }
    onChanged: (index) => console.log("slide", index)
}
