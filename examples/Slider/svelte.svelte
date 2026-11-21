<script lang="ts">
  import { Slider } from "$lib/purrimer";

  let volume = $state(40);
</script>

<div style="display: grid; gap: 12px">
  <Slider label="Volume" bind:value={volume} showValue suffix="%" />
  <Slider label="Zoom" value={50} step={5} pageStep={25} tickPosition="below" />
  <Slider label="Balance" value={70} disabled />
</div>
