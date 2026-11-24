import { createSignal } from "solid-js";
import { Swap } from "~/purrimer";

export default function Example() {
  const [copied] = createSignal(true);
  return (
    <Swap swapKey={copied()} class="text-body-medium" aria-live="polite">
      {copied() ? "Copied to clipboard" : "Copy link"}
    </Swap>
  );
}
