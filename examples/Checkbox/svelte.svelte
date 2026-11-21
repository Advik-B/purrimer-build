<script lang="ts">
  import { Checkbox } from "$lib/purrimer";

  let replies = $state(true);
  let digest = $state(false);
</script>

<div style="display: grid; gap: 12px; justify-items: start">
  <Checkbox label="Email me about replies" bind:checked={replies} />
  <Checkbox label="Weekly digest" bind:checked={digest} />
  <Checkbox label="Beta features (coming soon)" disabled />
</div>
