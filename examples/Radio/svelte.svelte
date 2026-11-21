<script lang="ts">
  import { Radio } from "$lib/purrimer";

  let plan = $state("pro");
</script>

<div style="display: grid; gap: 12px; justify-items: start" role="radiogroup" aria-label="Plan">
  <Radio label="Free" name="plan" value="free" bind:group={plan} />
  <Radio label="Pro" name="plan" value="pro" bind:group={plan} />
  <Radio label="Team (invite only)" name="plan" value="team" bind:group={plan} disabled />
</div>
