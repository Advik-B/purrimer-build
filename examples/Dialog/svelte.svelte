<script lang="ts">
  import { Button, Dialog } from "$lib/purrimer";

  let open = $state(true);
</script>

<p class="text-body-medium" style="margin: 16px">Repository settings</p>
<Dialog bind:open title="Delete repository?">
  This deletes purrimer-build and its history for good.
  {#snippet footer()}
    <Button label="Cancel" onclick={() => (open = false)} />
    <Button variant="danger" label="Delete" onclick={() => (open = false)} />
  {/snippet}
</Dialog>
