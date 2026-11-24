import QtQuick
import Purrimer

Column {
    width: 328
    spacing: 8

    component Heading: Text {
        color: Purrimer.fgColorDefault
        font: Purrimer.textTitleSmall
    }
    component Body: Text {
        width: 328
        wrapMode: Text.Wrap
        color: Purrimer.fgColorDefault
        font: Purrimer.textBodyMedium
    }

    Heading { text: "Advanced options" }
    Collapse {
        width: 328
        open: true
        Body { text: "Signed commits, branch protection and merge queues." }
    }
    Heading { text: "Danger zone" }
    Collapse {
        width: 328
        Body { text: "Archive or delete this repository." }
    }
}
