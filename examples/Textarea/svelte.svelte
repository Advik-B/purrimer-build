<script lang="ts">
  import { Textarea } from "$lib/purrimer";

  let bio = $state("");
</script>

<div style="display: grid; gap: 16px">
  <Textarea label="Bio" bind:value={bio} placeholder="Tell us a little about yourself" caption="Shown on your public profile." />
  <Textarea label="Why are you closing this?" rows={2} error="Add a short reason." />
</div>
