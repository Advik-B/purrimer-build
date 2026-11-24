import QtQuick
import Purrimer

Row {
    spacing: 32
    CountUp { to: 1284 }
    CountUp {
        anchors.bottom: parent.bottom
        to: 3742.5
        decimals: 2
        prefix: "€"
        mode: "roll"
        font: Purrimer.textStatSmall
        lineHeight: Purrimer.textStatSmallLineHeight
    }
}
