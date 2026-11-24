import { TextReveal } from "~/purrimer";

export default function Example() {
  return (
    <div style={{ display: "flex", "flex-direction": "column", gap: "12px" }}>
      <TextReveal text="All caught up today." class="text-title-large" />
      <TextReveal text="Branch ready" effect="tangle" class="text-title-medium" />
    </div>
  );
}
