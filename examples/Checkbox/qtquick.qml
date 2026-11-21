import QtQuick
import Purrimer

Column {
    spacing: 12
    Checkbox { text: "Email me about replies"; checked: true; onToggled: console.log("replies", checked) }
    Checkbox { text: "Weekly digest" }
    Checkbox { text: "Beta features (coming soon)"; enabled: false }
}
