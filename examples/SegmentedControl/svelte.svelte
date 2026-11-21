<script lang="ts">
  import { SegmentedControl } from "$lib/purrimer";

  let view = $state(1);
</script>

<SegmentedControl items={["Day", "Week", "Month"]} bind:selected={view} label="Calendar view" />
