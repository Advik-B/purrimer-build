<script lang="ts">
  import { ReorderList, type ReorderItem } from "$lib/purrimer";

  let sections: ReorderItem[] = $state([
    { key: "today", headline: "Today", supporting: "Tasks due today", icon: "calendar" },
    { key: "inbox", headline: "Inbox", icon: "inbox" },
    { key: "starred", headline: "Starred", icon: "star" },
    { key: "shared", headline: "Shared with me", supporting: "From 3 people", icon: "people" },
  ]);
</script>

<div style="padding-top: 16px">
  <ReorderList ariaLabel="Home sections" bind:items={sections} onreorder={(_, from, to) => console.log("moved", from, to)} />
</div>
