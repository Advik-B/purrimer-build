import QtQuick
import Purrimer

Column {
    spacing: 12
    Toggle { text: "Wi-Fi"; checked: true }
    Toggle { text: "Bluetooth"; onToggled: console.log("bluetooth", checked) }
    Toggle { text: "Airplane mode"; enabled: false }
}
