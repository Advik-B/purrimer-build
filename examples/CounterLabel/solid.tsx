import { CounterLabel } from "~/purrimer";

export default function Example() {
  const row = { display: "inline-flex", gap: "6px", "align-items": "center" };
  return (
    <div class="text-body-medium" style={{ display: "flex", gap: "16px", "align-items": "center" }}>
      <span style={row}>Issues <CounterLabel text="12" /></span>
      <span style={row}>Pull requests <CounterLabel text="1.2k" /></span>
      <span style={row}>Review <CounterLabel text={3} variant="primary" /></span>
    </div>
  );
}
