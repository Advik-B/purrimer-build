import QtQuick
import Purrimer

WheelPicker {
    width: 288
    columns: [
        { label: "Hour", options: ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"], value: "07", align: "end" },
        { label: "Minute", options: ["00", "05", "10", "15", "20", "25", "30", "35", "40", "45", "50", "55"], value: "30" },
        { label: "AM or PM", options: ["AM", "PM"], value: "AM", align: "start" }
    ]
    onChanged: (column, value) => console.log("column", column, value)
}
