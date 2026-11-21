<script lang="ts">
  import { Banner } from "$lib/purrimer";

  let shown = $state(true);
</script>

<div style="display: grid; gap: 12px">
  {#if shown}
    <Banner
      tone="success"
      title="Deployed"
      text="Version 2.4 is live for everyone."
      dismissible
      ondismiss={() => (shown = false)}
    />
  {/if}
  <Banner tone="danger" text="The build failed on two checks." />
</div>
