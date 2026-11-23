<script lang="ts">
  import { CounterLabel } from "$lib/purrimer";
</script>

<div class="text-body-medium" style="display: flex; gap: 16px; align-items: center">
  <span style="display: inline-flex; gap: 6px; align-items: center">Issues <CounterLabel text="12" /></span>
  <span style="display: inline-flex; gap: 6px; align-items: center">Pull requests <CounterLabel text="1.2k" /></span>
  <span style="display: inline-flex; gap: 6px; align-items: center">Review <CounterLabel text={3} variant="primary" /></span>
</div>
