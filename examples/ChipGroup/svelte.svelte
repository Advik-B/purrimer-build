<script lang="ts">
  import { ChipGroup } from "$lib/purrimer";

  const options = [
    { value: "all", label: "All" },
    { value: "unread", label: "Unread", count: 12 },
    { value: "mentions", label: "Mentions", icon: "mention" },
    { value: "snoozed", label: "Snoozed", disabled: true },
  ];
  let value: string | string[] | null = $state("unread");
</script>

<ChipGroup ariaLabel="Filter inbox" {options} bind:value />
