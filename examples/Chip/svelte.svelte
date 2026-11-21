<script lang="ts">
  import { Chip } from "$lib/purrimer";

  let tags = $state(["Archive"]);
</script>

<div style="display: flex; flex-wrap: wrap; gap: 8px">
  <Chip text="Design" icon="tag" />
  <Chip text="Shipped" tone="success" />
  {#each tags as tag (tag)}
    <Chip text={tag} tone="neutral" removable onremove={() => (tags = tags.filter((t) => t !== tag))} />
  {/each}
  <Chip text="Docs" tone="info" />
</div>
