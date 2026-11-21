<script lang="ts">
  import { AlertSheet } from "$lib/purrimer";
</script>

<AlertSheet
  inline
  icon="critical"
  title="Delete 3 photos?"
  message="They stay in Recently deleted for 30 days, then they are gone for good."
  buttons={[{ label: "Cancel" }, { label: "Delete", variant: "danger" }]}
  onbutton={(i) => console.log("button", i)}
/>
