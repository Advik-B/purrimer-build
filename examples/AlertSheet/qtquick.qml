import QtQuick
import Purrimer

Item {
    width: 358
    height: 300
    // inline draws the sheet in place, for docs; drop it and call open() in an app.
    AlertSheet {
        inline: true
        icon: "critical"
        title: "Delete 3 photos?"
        message: "They stay in Recently deleted for 30 days, then they are gone for good."
        buttons: [{ label: "Cancel" }, { label: "Delete", variant: "danger" }]
        onButtonClicked: (index) => console.log("button", index)
    }
}
