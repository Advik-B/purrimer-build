<script lang="ts">
  import { Tabs } from "$lib/purrimer";

  const panels = ["Three open issues, two in review.", "Updated 2 hours ago.", "Visible to your team."];
  let tab = $state(0);
</script>

<Tabs items={["Overview", "Activity", "Settings"]} bind:selected={tab} label="Project">
  {#snippet panel(i)}{panels[i]}{/snippet}
</Tabs>
