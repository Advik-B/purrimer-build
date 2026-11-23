import QtQuick
import Purrimer

Column {
    width: 328
    spacing: 12
    Slider { width: parent.width; label: "Volume"; value: 40; showValue: true; suffix: "%" }
    Slider { width: parent.width; label: "Zoom"; value: 50; stepSize: 5; pageStep: 25; tickPosition: "below" }
    Slider { width: parent.width; label: "Balance"; value: 70; disabled: true }
}
