<script lang="ts">
  import { Toggle } from "$lib/purrimer";

  let wifi = $state(true);
  let bluetooth = $state(false);
</script>

<div style="display: grid; gap: 12px; justify-items: start">
  <Toggle label="Wi-Fi" bind:checked={wifi} />
  <Toggle label="Bluetooth" bind:checked={bluetooth} onchange={(on) => console.log("bluetooth", on)} />
  <Toggle label="Airplane mode" disabled />
</div>
