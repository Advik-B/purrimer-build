import QtQuick
import Purrimer

Select {
    width: 328
    label: "T-shirt size"
    options: ["Small", "Medium", "Large"]
    currentIndex: 1
    onActivated: index => console.log("size", index)
}
