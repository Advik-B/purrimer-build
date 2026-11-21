import QtQuick
import Purrimer

Column {
    spacing: 12
    Banner {
        width: 368
        tone: "success"
        title: "Deployed"
        text: "Version 2.4 is live for everyone."
        dismissible: true
        onDismissed: visible = false
    }
    Banner { width: 368; tone: "danger"; text: "The build failed on two checks." }
}
