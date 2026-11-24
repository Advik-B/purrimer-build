<script lang="ts">
  import { AppBar, Button, KeyboardFooter, MobileScreen, TextField } from "$lib/purrimer";

  let title = $state("Water the plants");
</script>

<MobileScreen>
  {#snippet appBar()}
    <AppBar title="New task" back />
  {/snippet}
  <div style="padding: 16px">
    <TextField label="Title" bind:value={title} />
  </div>
  {#snippet footer()}
    <KeyboardFooter>
      <Button variant="primary" block label="Add task" />
    </KeyboardFooter>
  {/snippet}
</MobileScreen>
