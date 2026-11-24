import QtQuick
import Purrimer

ImageViewer {
    width: 390
    height: 520
    inline: true
    source: Qt.resolvedUrl("photo.jpg")
    alt: "Sunset over the lake"
    caption: "Lake Ilgen, an hour before dark"
    onClosed: console.log("close")
}
