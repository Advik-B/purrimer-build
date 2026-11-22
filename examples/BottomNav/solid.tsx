import { createSignal } from "solid-js";
import { BottomNav } from "~/purrimer";

export default function Example() {
  const [tab, setTab] = createSignal(0);
  return (
    <div style={{ display: "flex", "flex-direction": "column", "justify-content": "flex-end", height: "100%" }}>
      <BottomNav
        showLabels
        selected={tab()}
        onSelect={setTab}
        items={[
          { icon: "home", label: "Home" },
          { icon: "search", label: "Search" },
          { icon: "inbox", label: "Inbox", badge: 3 },
          { icon: "bell", label: "Activity", badge: true },
          { icon: "person", label: "Profile" },
        ]}
      />
    </div>
  );
}
