import { createSignal } from "solid-js";
import { BottomSheet, Button } from "~/purrimer";

export default function Example() {
  const [open, setOpen] = createSignal(true);
  return (
    <div>
      <p class="text-body-medium" style={{ margin: "16px" }}>Photo.jpg</p>
      <BottomSheet
        open={open()}
        title="Share"
        description="Photo.jpg, 2.4 MB"
        onClose={() => setOpen(false)}
        actions={<Button variant="primary" block label="Copy link" onClick={() => setOpen(false)} />}
      >
        <p style={{ margin: "0" }}>Anyone with the link can view this photo.</p>
      </BottomSheet>
    </div>
  );
}
