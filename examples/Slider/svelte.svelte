<script lang="ts">
  import { Slider } from "$lib/purrimer";

  let volume = $state(40);
  let price: [number, number] = $state([40, 120]);
  const sizes = [
    { value: 1, label: "S" },
    { value: 2, label: "M" },
    { value: 3, label: "L" },
    { value: 4, label: "XL" },
  ];
</script>

<div style="display: grid; gap: 12px">
  <Slider label="Volume" bind:value={volume} showValue suffix="%" />
  <Slider label="Zoom" value={50} step={5} pageStep={25} tickPosition="below" />
  <Slider label="Balance" value={70} disabled />
  <Slider label="Price" range bind:value={price} max={200} step={10} showValue suffix=" €" />
  <Slider label="Text size" value={2} min={1} max={4} marks={sizes} showValue />
</div>
