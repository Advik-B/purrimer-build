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
  <ListItem
    icon="mail"
    headline="Weekly digest"
    trailing="Mon"
    swipeStart={{ label: "Mark as read", icon: "check", tone: "accent", onswipe: () => console.log("read") }}
    swipeEnd={{ label: "Archive", icon: "archive", tone: "success", onswipe: () => console.log("archive") }}
  />
</div>
