import { createSignal } from "solid-js";
import { Slider } from "~/purrimer";

export default function Example() {
  const [volume, setVolume] = createSignal(40);
  return (
    <div style={{ display: "grid", gap: "12px" }}>
      <Slider label="Volume" value={volume()} onChange={setVolume} showValue suffix="%" />
      <Slider label="Zoom" value={50} step={5} pageStep={25} tickPosition="below" />
      <Slider label="Balance" value={70} disabled />
    </div>
  );
}
