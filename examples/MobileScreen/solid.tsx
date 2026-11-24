import { For } from "solid-js";
import { AppBar, BottomNav, FAB, ListItem, MobileScreen } from "~/purrimer";

const threads = [
  { icon: "person", headline: "Mira Okafor", supporting: "Lunch on Friday?" },
  { icon: "person", headline: "Design review", supporting: "Notes from today's crit" },
  { icon: "person", headline: "Jonas Weber", supporting: "Sent you the photos" },
  { icon: "person", headline: "Book club", supporting: "Next one is on the 12th" },
];

export default function Example() {
  return (
    <MobileScreen
      onRefresh={() => new Promise((done) => setTimeout(done, 1200))}
      appBar={<AppBar title="Inbox" large actions={[{ icon: "search", label: "Search" }]} />}
      fab={<FAB icon="pencil" label="Compose" extended />}
      bottomNav={
        <BottomNav
          showLabels
          selected={2}
          items={[
            { icon: "home", label: "Home" },
            { icon: "search", label: "Search" },
            { icon: "inbox", label: "Inbox", badge: 3 },
            { icon: "person", label: "Profile" },
          ]}
        />
      }
    >
      <div role="list">
        <For each={threads}>{(t) => <ListItem icon={t.icon} headline={t.headline} supporting={t.supporting} chevron />}</For>
      </div>
    </MobileScreen>
  );
}
