import { Avatar } from "~/purrimer";

// Pass src for a picture; the initials show until it loads, or if it fails.
export default function Example() {
  return (
    <div style={{ display: "flex", gap: "12px", "align-items": "center" }}>
      <Avatar name="Ada Lovelace" size={24} />
      <Avatar name="Grace Hopper" />
      <Avatar name="Alan Turing" size={40} />
      <Avatar name="Purrimer" size={48} square />
    </div>
  );
}
