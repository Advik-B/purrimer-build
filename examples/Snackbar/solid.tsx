import { createSignal } from "solid-js";
import { Snackbar } from "~/purrimer";

export default function Example() {
  const [open, setOpen] = createSignal(true);
  return (
    <div>
      <p class="text-body-medium" style={{ margin: "16px" }}>Inbox</p>
      <Snackbar
        open={open()}
        message="Message archived"
        action="Undo"
        onAction={() => console.log("undo")}
        onClose={() => setOpen(false)}
      />
    </div>
  );
}
