import QtQuick
import Purrimer

MotionScope {
    kind: "playful"

    component Note: Text {
        width: 296
        wrapMode: Text.Wrap
        color: Purrimer.fgColorDefault
        font: Purrimer.textBodyMedium
    }

    Column {
        spacing: 12
        Motion {
            name: "pounce"
            Card { width: 328; title: "Pull request merged"; Note { text: "All checks passed. Enjoy the quiet." } }
        }
        // The closest scope wins: this one is calm again.
        MotionScope {
            kind: "sleepy"
            Motion {
                name: "rise"
                index: 1
                Card { width: 328; title: "Billing stays sleepy"; Note { text: "Settings and errors never bounce." } }
            }
        }
    }
}
