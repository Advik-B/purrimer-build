import QtQuick
import Purrimer

Swap {
    swapKey: true
    delegate: Text {
        property var swapKey
        text: swapKey ? "Copied to clipboard" : "Copy link"
        color: Purrimer.fgColorDefault
        font: Purrimer.textBodyMedium
    }
}
