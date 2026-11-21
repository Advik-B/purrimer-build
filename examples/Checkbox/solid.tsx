import { createSignal } from "solid-js";
import { Checkbox } from "~/purrimer";

export default function Example() {
  const [replies, setReplies] = createSignal(true);
  const [digest, setDigest] = createSignal(false);
  return (
    <div style={{ display: "grid", gap: "12px", "justify-items": "start" }}>
      <Checkbox label="Email me about replies" checked={replies()} onChange={setReplies} />
      <Checkbox label="Weekly digest" checked={digest()} onChange={setDigest} />
      <Checkbox label="Beta features (coming soon)" disabled />
    </div>
  );
}
