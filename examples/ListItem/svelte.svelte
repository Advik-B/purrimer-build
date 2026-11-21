<script lang="ts">
  import { ListItem } from "$lib/purrimer";
</script>

<div role="list">
  <ListItem
    icon="bell"
    headline="Notifications"
    supporting="Mentions and replies"
    trailing="On"
    chevron
    onclick={() => console.log("open notifications")}
  />
  <ListItem icon="globe" headline="Language" trailing="English" />
</div>
