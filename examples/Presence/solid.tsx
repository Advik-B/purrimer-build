import { createSignal } from "solid-js";
import { Card, Presence } from "~/purrimer";

export default function Example() {
  const [show] = createSignal(true);
  return (
    <Presence show={show()} collapse>
      <Card title="Draft saved">
        <p style={{ margin: 0 }}>It leaves with lie-down when dismissed.</p>
      </Card>
    </Presence>
  );
}
