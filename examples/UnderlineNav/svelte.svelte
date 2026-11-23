<script lang="ts">
  import { UnderlineNav } from "$lib/purrimer";

  const items = [
    { label: "Code", icon: "code" },
    { label: "Issues", icon: "issue-opened", count: 12 },
    { label: "Pull requests", icon: "git-pull-request", count: 3 },
    { label: "Actions", icon: "play" },
  ];
  let current = $state(0);
</script>

<UnderlineNav ariaLabel="Repository" {items} bind:current />
