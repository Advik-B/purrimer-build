import { LoadingDots } from "~/purrimer";

export default function Example() {
  const row = (gap: string) => ({ display: "inline-flex", gap, "align-items": "center" });
  return (
    <div class="text-body-medium" style={{ display: "grid", gap: "12px", "justify-items": "start" }}>
      <span style={row("8px")}>Connecting <LoadingDots /></span>
      <span style={row("4px")}>Mona is typing <LoadingDots variant="snooze" /></span>
      <span style={row("8px")}>Fetching treats <LoadingDots kind="playful" /></span>
    </div>
  );
}
