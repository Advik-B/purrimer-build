<script lang="ts">
  import { ActionMenu } from "$lib/purrimer";

  let open = $state(true);
</script>

<ActionMenu
  label="File"
  bind:open
  items={[
    { label: "Edit file", leadingIcon: "pencil", trailingText: "E" },
    { label: "Copy permalink", leadingIcon: "link", trailingText: "Y" },
    { label: "View history", leadingIcon: "history" },
    { divider: true },
    { label: "Delete file", leadingIcon: "trash", variant: "danger" },
  ]}
  onselect={(item) => console.log("picked", item.label)}
/>
