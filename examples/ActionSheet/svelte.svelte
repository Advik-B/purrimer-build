<script lang="ts">
  import { ActionSheet } from "$lib/purrimer";

  const items = [
    { label: "Share", icon: "share-android" },
    { label: "Copy link", icon: "link", description: "Anyone with the link can view" },
    { label: "Move to", icon: "file-directory", items: [{ label: "Holidays" }, { label: "Family" }] },
    { label: "Favourite", icon: "star", checked: true },
    { divider: true },
    { label: "Delete", icon: "trash", variant: "danger" as const },
  ];
</script>

<ActionSheet inline title="Photo.jpg" {items} onselect={(item) => console.log("chose", item.label)} />
