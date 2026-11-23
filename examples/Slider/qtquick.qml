import QtQuick
import Purrimer

Column {
    width: 328
    spacing: 12
    Slider { width: parent.width; label: "Volume"; value: 40; showValue: true; suffix: "%" }
    Slider { width: parent.width; label: "Zoom"; value: 50; stepSize: 5; pageStep: 25; tickPosition: "below" }
    Slider { width: parent.width; label: "Balance"; value: 70; disabled: true }
    Slider {
        width: parent.width
        label: "Price"
        range: true
        to: 200
        stepSize: 10
        low: 40
        high: 120
        showValue: true
        suffix: " €"
        onRangeMoved: (low, high) => console.log("price", low, high)
    }
    Slider {
        width: parent.width
        label: "Text size"
        from: 1
        to: 4
        value: 2
        showValue: true
        marks: [{ value: 1, label: "S" }, { value: 2, label: "M" }, { value: 3, label: "L" }, { value: 4, label: "XL" }]
    }
}
