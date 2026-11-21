import QtQuick
import Purrimer

// Radios in the same parent are exclusive; use a ButtonGroup to split them.
Column {
    spacing: 12
    Radio { text: "Free" }
    Radio { text: "Pro"; checked: true }
    Radio { text: "Team (invite only)"; enabled: false }
}
