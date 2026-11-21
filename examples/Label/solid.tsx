import { Label } from "~/purrimer";

export default function Example() {
  return (
    <div style={{ display: "flex", "flex-wrap": "wrap", gap: "8px" }}>
      <Label text="Draft" />
      <Label text="New" tone="accent" />
      <Label text="Merged" tone="success" />
      <Label text="Pending" tone="attention" />
      <Label text="Failed" tone="danger" />
      <Label tone="done">Closed</Label>
    </div>
  );
}
