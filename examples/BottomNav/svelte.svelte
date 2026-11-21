<script lang="ts">
  import { BottomNav } from "$lib/purrimer";

  let tab = $state(0);
</script>

<div style="display: flex; flex-direction: column; justify-content: flex-end; height: 100%">
  <BottomNav
    showLabels
    bind:selected={tab}
    items={[
      { icon: "home", label: "Home" },
      { icon: "search", label: "Search" },
      { icon: "inbox", label: "Inbox", badge: 3 },
      { icon: "person", label: "Profile" },
    ]}
  />
</div>
