import QtQuick
import Purrimer

MotionScope {
    kind: "playful"
    // burst.fire += 1 (or burst.burst()) throws confetti from the card.
    Burst {
        id: burst
        Card {
            width: 328
            title: "Pull request merged"
            Text { text: "All checks passed."; color: Purrimer.fgColorDefault; font: Purrimer.textBodyMedium }
        }
    }
}
