import QtQuick
import Purrimer

Column {
    spacing: 12

    component Note: Text {
        width: 296
        wrapMode: Text.Wrap
        color: Purrimer.fgColorDefault
        font: Purrimer.textBodyMedium
    }

    Motion {
        name: "rise"
        Card { width: 328; title: "Saved to drafts"; Note { text: "Your reply is waiting in Drafts." } }
    }
    Motion {
        name: "pounce"
        index: 1
        Card { width: 328; title: "New badge"; Note { text: "You reviewed ten pull requests this week." } }
    }
    Motion {
        name: "bask"
        index: 2
        radius: 12
        Card { width: 328; title: "Linked from the release notes"; Note { text: "A halo shows where the link points." } }
    }
}
