import { createSignal } from "solid-js";
import { TextField } from "~/purrimer";

export default function Example() {
  const [email, setEmail] = createSignal("");
  const [username, setUsername] = createSignal("purr");
  return (
    <div style={{ display: "grid", gap: "16px" }}>
      <TextField
        label="Email"
        type="email"
        leadingIcon="mail"
        placeholder="you@example.com"
        caption="We never share it."
        value={email()}
        onValue={setEmail}
      />
      <TextField
        label="Username"
        error={username() === "purr" ? "That name is taken." : ""}
        value={username()}
        onValue={setUsername}
      />
    </div>
  );
}
