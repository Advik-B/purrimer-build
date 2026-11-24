<script lang="ts">
  import { BottomSheet, Button } from "$lib/purrimer";

  let open = $state(true);
</script>

<p class="text-body-medium" style="margin: 16px">Photo.jpg</p>
<BottomSheet bind:open title="Share" description="Photo.jpg, 2.4 MB">
  <p style="margin: 0">Anyone with the link can view this photo.</p>
  {#snippet actions()}
    <Button variant="primary" block label="Copy link" onclick={() => (open = false)} />
  {/snippet}
</BottomSheet>
