import { createSignal } from "solid-js";
import { BottomSheet, Button } from "~/purrimer";

export default function Example() {
  const [open, setOpen] = createSignal(true);
  return (
    <div>
      <p class="text-body-medium" style={{ margin: "16px" }}>Photo.jpg</p>
      <BottomSheet open={open()} title="Share" onClose={() => setOpen(false)}>
        <p style={{ margin: "0 0 16px" }}>Anyone with the link can view this photo.</p>
        <Button variant="primary" block label="Copy link" onClick={() => setOpen(false)} />
      </BottomSheet>
    </div>
  );
}
