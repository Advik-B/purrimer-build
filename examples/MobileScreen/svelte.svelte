<script lang="ts">
  import { AppBar, BottomNav, FAB, ListItem, MobileScreen } from "$lib/purrimer";

  let tab = $state(2);
  const threads = [
    { icon: "person", headline: "Mira Okafor", supporting: "Lunch on Friday?" },
    { icon: "person", headline: "Design review", supporting: "Notes from today's crit" },
    { icon: "person", headline: "Jonas Weber", supporting: "Sent you the photos" },
    { icon: "person", headline: "Book club", supporting: "Next one is on the 12th" },
  ];
</script>

<MobileScreen onrefresh={() => new Promise((done) => setTimeout(done, 1200))}>
  {#snippet appBar()}
    <AppBar title="Inbox" large actions={[{ icon: "search", label: "Search" }]} />
  {/snippet}
  <div role="list">
    {#each threads as thread (thread.headline)}
      <ListItem icon={thread.icon} headline={thread.headline} supporting={thread.supporting} chevron />
    {/each}
  </div>
  {#snippet fab()}
    <FAB icon="pencil" label="Compose" extended />
  {/snippet}
  {#snippet bottomNav()}
    <BottomNav
      showLabels
      bind:selected={tab}
      items={[
        { icon: "home", label: "Home" },
        { icon: "search", label: "Search" },
        { icon: "inbox", label: "Inbox", badge: 3 },
        { icon: "person", label: "Profile" },
      ]}
    />
  {/snippet}
</MobileScreen>
