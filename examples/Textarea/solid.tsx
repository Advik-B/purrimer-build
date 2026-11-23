import { createSignal } from "solid-js";
import { Textarea } from "~/purrimer";

export default function Example() {
  const [bio, setBio] = createSignal("");
  return (
    <div style={{ display: "grid", gap: "16px" }}>
      <Textarea
        label="Bio"
        value={bio()}
        onValue={setBio}
        placeholder="Tell us a little about yourself"
        caption="Shown on your public profile."
      />
      <Textarea label="Why are you closing this?" rows={2} error="Add a short reason." />
    </div>
  );
}
