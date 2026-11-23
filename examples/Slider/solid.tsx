import { createSignal } from "solid-js";
import { Slider } from "~/purrimer";

export default function Example() {
  const [volume, setVolume] = createSignal(40);
  const [price, setPrice] = createSignal<[number, number]>([40, 120]);
  const sizes = [
    { value: 1, label: "S" },
    { value: 2, label: "M" },
    { value: 3, label: "L" },
    { value: 4, label: "XL" },
  ];
  return (
    <div style={{ display: "grid", gap: "12px" }}>
      <Slider label="Volume" value={volume()} onChange={(v) => setVolume(v as number)} showValue suffix="%" />
      <Slider label="Zoom" value={50} step={5} pageStep={25} tickPosition="below" />
      <Slider label="Balance" value={70} disabled />
      <Slider
        label="Price"
        range
        value={price()}
        onChange={(v) => setPrice(v as [number, number])}
        max={200}
        step={10}
        showValue
        suffix=" €"
      />
      <Slider label="Text size" value={2} min={1} max={4} marks={sizes} showValue />
    </div>
  );
}
