<script lang="ts">
  import { TextField } from "$lib/purrimer";

  let email = $state("");
  let username = $state("purr");
</script>

<div style="display: grid; gap: 16px">
  <TextField
    label="Email"
    type="email"
    leadingIcon="mail"
    placeholder="you@example.com"
    caption="We never share it."
    bind:value={email}
  />
  <TextField label="Username" error={username === "purr" ? "That name is taken." : ""} bind:value={username} />
</div>
