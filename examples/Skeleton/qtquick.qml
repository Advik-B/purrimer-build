import QtQuick
import Purrimer

Column {
    width: 328
    spacing: 16
    Row {
        width: parent.width
        spacing: 12
        Skeleton { id: avatar; variant: "circle"; anchors.verticalCenter: parent.verticalCenter }
        Skeleton { lines: 2; width: parent.width - avatar.width - parent.spacing }
    }
    Skeleton { variant: "block"; effect: "snore"; width: parent.width }
}
