import { AppBar, Button, KeyboardFooter, MobileScreen, TextField } from "~/purrimer";

export default function Example() {
  return (
    <MobileScreen
      appBar={<AppBar title="New task" back />}
      footer={
        <KeyboardFooter>
          <Button variant="primary" block label="Add task" />
        </KeyboardFooter>
      }
    >
      <div style={{ padding: "16px" }}>
        <TextField label="Title" value="Water the plants" />
      </div>
    </MobileScreen>
  );
}
