import QtQuick
import Purrimer

// Set indeterminate: true to sweep while the amount is unknown.
Column {
    spacing: 16
    ProgressBar { width: 328; value: 40 }
    ProgressBar { width: 328; value: 75; tone: "success" }
    ProgressBar { width: 328; value: 95; tone: "danger" }
}
