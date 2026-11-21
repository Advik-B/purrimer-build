import { createSignal } from "solid-js";
import { Toggle } from "~/purrimer";

export default function Example() {
  const [wifi, setWifi] = createSignal(true);
  const [bluetooth, setBluetooth] = createSignal(false);
  return (
    <div style={{ display: "grid", gap: "12px", "justify-items": "start" }}>
      <Toggle label="Wi-Fi" checked={wifi()} onChange={setWifi} />
      <Toggle label="Bluetooth" checked={bluetooth()} onChange={setBluetooth} />
      <Toggle label="Airplane mode" disabled />
    </div>
  );
}
