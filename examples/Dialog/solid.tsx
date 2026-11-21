import { createSignal } from "solid-js";
import { Button, Dialog } from "~/purrimer";

export default function Example() {
  const [open, setOpen] = createSignal(true);
  return (
    <div>
      <p class="text-body-medium" style={{ margin: "16px" }}>Repository settings</p>
      <Dialog
        open={open()}
        title="Delete repository?"
        onClose={() => setOpen(false)}
        footer={
          <>
            <Button label="Cancel" onClick={() => setOpen(false)} />
            <Button variant="danger" label="Delete" onClick={() => setOpen(false)} />
          </>
        }
      >
        This deletes purrimer-build and its history for good.
      </Dialog>
    </div>
  );
}
