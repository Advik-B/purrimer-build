import { Show, createSignal } from "solid-js";
import { Banner } from "~/purrimer";

export default function Example() {
  const [shown, setShown] = createSignal(true);
  return (
    <div style={{ display: "grid", gap: "12px" }}>
      <Show when={shown()}>
        <Banner
          tone="success"
          title="Deployed"
          text="Version 2.4 is live for everyone."
          dismissible
          onDismiss={() => setShown(false)}
        />
      </Show>
      <Banner tone="danger" text="The build failed on two checks." />
    </div>
  );
}
