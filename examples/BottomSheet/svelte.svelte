<script lang="ts">
  import { BottomSheet, Button } from "$lib/purrimer";

  let open = $state(true);
</script>

<p class="text-body-medium" style="margin: 16px">Photo.jpg</p>
<BottomSheet bind:open title="Share">
  <p style="margin: 0 0 16px">Anyone with the link can view this photo.</p>
  <Button variant="primary" block label="Copy link" onclick={() => (open = false)} />
</BottomSheet>
