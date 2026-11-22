<script lang="ts">
  import { FAB, HoldMenu } from "$lib/purrimer";
</script>

<div style="position: relative; height: 420px">
  <p class="text-body-medium" style="margin: 0; padding: 16px">Hold the button for more ways to start a note.</p>
  <div style="position: absolute; right: 16px; bottom: 16px">
    <HoldMenu
      defaultOpen
      ariaLabel="Start something"
      items={[
        { label: "New note", icon: "note" },
        { label: "Take photo", icon: "device-camera" },
        { label: "Checklist", icon: "checklist" },
      ]}
      onselect={(item) => console.log("chose", item.label)}
    >
      <FAB label="New note" onclick={() => console.log("new note")} />
    </HoldMenu>
  </div>
</div>
