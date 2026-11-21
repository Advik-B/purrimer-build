import { createSignal } from "solid-js";
import { SegmentedControl } from "~/purrimer";

export default function Example() {
  const [view, setView] = createSignal(1);
  return <SegmentedControl items={["Day", "Week", "Month"]} selected={view()} onSelect={setView} label="Calendar view" />;
}
