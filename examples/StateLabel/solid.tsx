import { StateLabel } from "~/purrimer";

export default function Example() {
  return (
    <div style={{ display: "flex", "flex-wrap": "wrap", gap: "8px", "align-items": "center" }}>
      <StateLabel status="open" text="Open" />
      <StateLabel status="closed" text="Closed" />
      <StateLabel status="merged" text="Merged" />
      <StateLabel status="draft" size="small" text="Draft" />
    </div>
  );
}
