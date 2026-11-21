import { ProgressBar } from "~/purrimer";

// Set indeterminate to sweep while the amount is unknown.
export default function Example() {
  return (
    <div style={{ display: "grid", gap: "16px" }}>
      <ProgressBar value={40} label="Upload" />
      <ProgressBar value={75} tone="success" label="Storage" />
      <ProgressBar value={95} tone="danger" label="Quota" />
    </div>
  );
}
