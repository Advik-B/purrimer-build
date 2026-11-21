import { createSignal } from "solid-js";
import { WheelPicker } from "~/purrimer";

const pad = (n: number) => String(n).padStart(2, "0");

export default function Example() {
  const [time, setTime] = createSignal({ hour: "07", minute: "30", half: "AM" });
  const keys = ["hour", "minute", "half"] as const;
  return (
    <WheelPicker
      columns={[
        { label: "Hour", options: Array.from({ length: 12 }, (_, i) => pad(i + 1)), value: time().hour, align: "end" },
        { label: "Minute", options: Array.from({ length: 12 }, (_, i) => pad(i * 5)), value: time().minute },
        { label: "AM or PM", options: ["AM", "PM"], value: time().half, align: "start" },
      ]}
      onChange={(c, v) => setTime({ ...time(), [keys[c]]: v })}
    />
  );
}
