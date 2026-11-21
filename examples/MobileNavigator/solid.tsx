import { For } from "solid-js";
import { AppBar, ListItem, MobileNavigator, MobileScreen, type ScreenProps } from "~/purrimer";

type Thread = { name: string; text: string };

const threads: Thread[] = [
  { name: "Mira Okafor", text: "Lunch on Friday?" },
  { name: "Design review", text: "Notes from today's crit" },
  { name: "Jonas Weber", text: "Sent you the photos" },
];

const screens = {
  inbox: ({ nav }: ScreenProps) => (
    <MobileScreen appBar={<AppBar title="Inbox" large />}>
      <div role="list">
        <For each={threads}>
          {(t) => <ListItem icon="person" headline={t.name} supporting={t.text} chevron onClick={() => nav.push("thread", t)} />}
        </For>
      </div>
    </MobileScreen>
  ),
  thread: ({ nav, params }: ScreenProps) => {
    const thread = params as Thread;
    return (
      <MobileScreen appBar={<AppBar title={thread.name} back onBack={() => nav.pop()} />}>
        <p class="text-body-medium" style={{ margin: "16px" }}>{thread.text}</p>
      </MobileScreen>
    );
  },
  settings: () => (
    <MobileScreen surface="inset" appBar={<AppBar title="Settings" large />}>
      <div role="list">
        <ListItem icon="bell" headline="Notifications" trailing="On" chevron />
      </div>
    </MobileScreen>
  ),
};

export default function Example() {
  return (
    <MobileNavigator
      screens={screens}
      tabs={[
        { screen: "inbox", label: "Inbox", icon: "inbox", badge: 3 },
        { screen: "settings", label: "Settings", icon: "gear" },
      ]}
    />
  );
}
