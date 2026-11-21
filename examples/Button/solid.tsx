import { Button } from "~/purrimer";

export default function Example() {
  return (
    <div style={{ display: "grid", gap: "12px" }}>
      <div style={{ display: "flex", gap: "8px" }}>
        <Button variant="primary" leadingIcon="check" label="Save" onClick={() => console.log("saved")} />
        <Button label="Cancel" />
        <Button variant="danger" label="Delete" />
        <Button label="Disabled" disabled />
      </div>
      <div style={{ display: "flex", gap: "8px", "align-items": "center" }}>
        <Button size="small" label="Small" />
        <Button label="Medium" />
        <Button size="large" label="Large" />
      </div>
    </div>
  );
}
