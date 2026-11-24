<script lang="ts">
  import { FAB } from "$lib/purrimer";
</script>

<div style="display: flex; gap: 16px; align-items: center">
  <FAB
    label="New note"
    onclick={() => console.log("new note")}
    actions={[
      { icon: "device-camera", label: "Take photo" },
      { icon: "checklist", label: "Checklist" },
    ]}
    onaction={(item) => console.log("chose", item.label)}
  />
  <FAB icon="pencil" label="Compose" extended />
</div>
