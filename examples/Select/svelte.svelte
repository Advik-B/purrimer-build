<script lang="ts">
  import { Select } from "$lib/purrimer";

  let size = $state(1);
</script>

<Select label="T-shirt size" options={["Small", "Medium", "Large"]} bind:value={size} />
