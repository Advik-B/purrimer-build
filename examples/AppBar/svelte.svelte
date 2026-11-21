<script lang="ts">
  import { AppBar } from "$lib/purrimer";
</script>

<div>
  <AppBar
    title="Inbox"
    back
    large
    actions={[
      { icon: "search", label: "Search", onclick: () => console.log("search") },
      { icon: "kebab-horizontal", label: "More" },
    ]}
    onback={() => history.back()}
  />
</div>
