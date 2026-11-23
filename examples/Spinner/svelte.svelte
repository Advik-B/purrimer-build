<script lang="ts">
  import { Spinner } from "$lib/purrimer";
</script>

<div style="display: flex; gap: 24px; align-items: center">
  <Spinner size="small" />
  <Spinner />
  <Spinner size="large" label="Loading the report" />
  <Spinner kind="playful" />
</div>
