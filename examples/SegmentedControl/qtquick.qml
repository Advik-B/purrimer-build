import QtQuick
import Purrimer

SegmentedControl {
    items: ["Day", "Week", "Month"]
    selected: 1
    onActivated: index => selected = index
}
