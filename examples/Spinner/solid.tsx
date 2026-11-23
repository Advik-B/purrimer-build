import { Spinner } from "~/purrimer";

export default function Example() {
  return (
    <div style={{ display: "flex", gap: "24px", "align-items": "center" }}>
      <Spinner size="small" />
      <Spinner />
      <Spinner size="large" label="Loading the report" />
      <Spinner kind="playful" />
    </div>
  );
}
