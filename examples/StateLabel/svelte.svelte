<script lang="ts">
  import { StateLabel } from "$lib/purrimer";
</script>

<div style="display: flex; flex-wrap: wrap; gap: 8px; align-items: center">
  <StateLabel status="open" text="Open" />
  <StateLabel status="closed" text="Closed" />
  <StateLabel status="merged" text="Merged" />
  <StateLabel status="draft" size="small" text="Draft" />
</div>
