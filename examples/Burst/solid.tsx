import { createSignal } from "solid-js";
import { Burst, Card, MotionScope } from "~/purrimer";

export default function Example() {
  // setMerged(merged() + 1) bursts.
  const [merged] = createSignal(0);
  return (
    <MotionScope kind="playful">
      <Burst fire={merged()} style={{ display: "block" }}>
        <Card title="Pull request merged">
          <p style={{ margin: 0 }}>All checks passed.</p>
        </Card>
      </Burst>
    </MotionScope>
  );
}
