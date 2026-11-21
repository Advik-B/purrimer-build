<script lang="ts">
  import { AppBar, ListItem, MobileNavigator, MobileScreen } from "$lib/purrimer";

  const threads = [
    { name: "Mira Okafor", text: "Lunch on Friday?" },
    { name: "Design review", text: "Notes from today's crit" },
    { name: "Jonas Weber", text: "Sent you the photos" },
  ];
  const tabs = [
    { screen: "inbox", label: "Inbox", icon: "inbox", badge: 3 },
    { screen: "settings", label: "Settings", icon: "gear" },
  ];
</script>

<MobileNavigator {tabs}>
  {#snippet screen(name, nav, params)}
    {#if name === "inbox"}
      <MobileScreen>
        {#snippet appBar()}<AppBar title="Inbox" large />{/snippet}
        <div role="list">
          {#each threads as thread (thread.name)}
            <ListItem icon="person" headline={thread.name} supporting={thread.text} chevron onclick={() => nav.push("thread", thread)} />
          {/each}
        </div>
      </MobileScreen>
    {:else if name === "thread"}
      {@const thread = params as { name: string; text: string }}
      <MobileScreen>
        {#snippet appBar()}<AppBar title={thread.name} back onback={() => nav.pop()} />{/snippet}
        <p class="text-body-medium" style="margin: 16px">{thread.text}</p>
      </MobileScreen>
    {:else}
      <MobileScreen surface="inset">
        {#snippet appBar()}<AppBar title="Settings" large />{/snippet}
        <div role="list">
          <ListItem icon="bell" headline="Notifications" trailing="On" chevron />
        </div>
      </MobileScreen>
    {/if}
  {/snippet}
</MobileNavigator>
