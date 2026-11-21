<script lang="ts">
  import { Snackbar } from "$lib/purrimer";

  let open = $state(true);
</script>

<p class="text-body-medium" style="margin: 16px">Inbox</p>
<Snackbar bind:open message="Message archived" action="Undo" onaction={() => console.log("undo")} />
