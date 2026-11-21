import { InfoButton } from "~/purrimer";

export default function Example() {
  return (
    <div class="text-body-medium" style={{ display: "flex", "align-items": "center", padding: "0 4px 0 16px" }}>
      <span style={{ flex: "1" }}>Estimated delivery: Tue 14 Jan</span>
      <InfoButton
        defaultOpen
        title="Estimated delivery"
        message="We work it out from the courier's last scan and their usual times for your area, so it can move by a day."
      />
    </div>
  );
}
