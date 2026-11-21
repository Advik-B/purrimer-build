<script lang="ts">
  import { IconButton } from "$lib/purrimer";
</script>

<div style="display: flex; gap: 8px; align-items: center">
  <IconButton icon="pencil" label="Edit" />
  <IconButton icon="plus" label="Add" variant="primary" />
  <IconButton icon="trash" label="Delete" variant="danger" />
  <IconButton icon="kebab-horizontal" label="More" variant="invisible" />
  <IconButton icon="x" label="Close" size="small" />
</div>
