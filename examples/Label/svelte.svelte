<script lang="ts">
  import { Label } from "$lib/purrimer";
</script>

<div style="display: flex; flex-wrap: wrap; gap: 8px">
  <Label text="Draft" />
  <Label text="New" tone="accent" />
  <Label text="Merged" tone="success" />
  <Label text="Pending" tone="attention" />
  <Label text="Failed" tone="danger" />
  <Label tone="done">Closed</Label>
</div>
