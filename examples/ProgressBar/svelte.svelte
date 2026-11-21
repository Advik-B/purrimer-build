<script lang="ts">
  import { ProgressBar } from "$lib/purrimer";
</script>

<!-- Set indeterminate to sweep while the amount is unknown. -->
<div style="display: grid; gap: 16px">
  <ProgressBar value={40} label="Upload" />
  <ProgressBar value={75} tone="success" label="Storage" />
  <ProgressBar value={95} tone="danger" label="Quota" />
</div>
