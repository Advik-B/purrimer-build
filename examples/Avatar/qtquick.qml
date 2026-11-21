import QtQuick
import Purrimer

// Set source for a picture.
Row {
    spacing: 12
    Avatar { name: "Ada Lovelace"; size: 24; anchors.verticalCenter: parent.verticalCenter }
    Avatar { name: "Grace Hopper"; anchors.verticalCenter: parent.verticalCenter }
    Avatar { name: "Alan Turing"; size: 40; anchors.verticalCenter: parent.verticalCenter }
    Avatar { name: "Purrimer"; size: 48; square: true }
}
