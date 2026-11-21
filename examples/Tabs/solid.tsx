import { createSignal } from "solid-js";
import { Tabs } from "~/purrimer";

const panels = ["Three open issues, two in review.", "Updated 2 hours ago.", "Visible to your team."];

export default function Example() {
  const [tab, setTab] = createSignal(0);
  return (
    <Tabs items={["Overview", "Activity", "Settings"]} selected={tab()} onSelect={setTab} label="Project">
      {(i) => panels[i]}
    </Tabs>
  );
}
