import { For, createSignal } from "solid-js";
import { Chip } from "~/purrimer";

export default function Example() {
  const [tags, setTags] = createSignal(["Archive"]);
  return (
    <div style={{ display: "flex", "flex-wrap": "wrap", gap: "8px" }}>
      <Chip text="Design" icon="tag" />
      <Chip text="Shipped" tone="success" />
      <For each={tags()}>
        {(tag) => <Chip text={tag} tone="neutral" removable onRemove={() => setTags(tags().filter((t) => t !== tag))} />}
      </For>
      <Chip text="Docs" tone="info" />
    </div>
  );
}
