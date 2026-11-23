import { Skeleton } from "~/purrimer";

export default function Example() {
  return (
    <div aria-busy="true" style={{ display: "grid", gap: "16px" }}>
      <div style={{ display: "flex", gap: "12px", "align-items": "center" }}>
        <Skeleton variant="circle" />
        <div style={{ flex: "1" }}><Skeleton lines={2} /></div>
      </div>
      <Skeleton variant="block" effect="snore" />
    </div>
  );
}
