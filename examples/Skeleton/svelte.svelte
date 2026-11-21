<script lang="ts">
  import { Skeleton } from "$lib/purrimer";
</script>

<div aria-busy="true" style="display: grid; gap: 16px">
  <div style="display: flex; gap: 12px; align-items: center">
    <Skeleton variant="circle" />
    <div style="flex: 1"><Skeleton lines={2} /></div>
  </div>
  <Skeleton variant="block" effect="snore" />
</div>
