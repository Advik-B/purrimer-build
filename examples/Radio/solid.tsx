import { createSignal } from "solid-js";
import { Radio } from "~/purrimer";

export default function Example() {
  const [plan, setPlan] = createSignal("pro");
  return (
    <div style={{ display: "grid", gap: "12px", "justify-items": "start" }} role="radiogroup" aria-label="Plan">
      <Radio label="Free" name="plan" value="free" checked={plan() === "free"} onSelect={setPlan} />
      <Radio label="Pro" name="plan" value="pro" checked={plan() === "pro"} onSelect={setPlan} />
      <Radio label="Team (invite only)" name="plan" value="team" disabled />
    </div>
  );
}
