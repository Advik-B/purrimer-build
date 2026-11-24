import { Card, Motion, MotionScope } from "~/purrimer";

export default function Example() {
  return (
    <MotionScope kind="playful">
      <div style={{ display: "flex", "flex-direction": "column", gap: "12px" }}>
        <Motion name="pounce">
          <Card title="Pull request merged">
            <p style={{ margin: 0 }}>All checks passed. Enjoy the quiet.</p>
          </Card>
        </Motion>
        <MotionScope kind="sleepy">
          <Motion name="rise" index={1}>
            <Card title="Billing stays sleepy">
              <p style={{ margin: 0 }}>Settings and errors never bounce.</p>
            </Card>
          </Motion>
        </MotionScope>
      </div>
    </MotionScope>
  );
}
