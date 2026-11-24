<script lang="ts">
  import { Swap } from "$lib/purrimer";

  let copied = $state(true);
</script>

<Swap swapKey={copied} class="text-body-medium" aria-live="polite">{copied ? "Copied to clipboard" : "Copy link"}</Swap>
