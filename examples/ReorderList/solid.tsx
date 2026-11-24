import { ReorderList } from "~/purrimer";

export default function Example() {
  return (
    <div style={{ "padding-top": "16px" }}>
      <ReorderList
        ariaLabel="Home sections"
        items={[
          { key: "today", headline: "Today", supporting: "Tasks due today", icon: "calendar" },
          { key: "inbox", headline: "Inbox", icon: "inbox" },
          { key: "starred", headline: "Starred", icon: "star" },
          { key: "shared", headline: "Shared with me", supporting: "From 3 people", icon: "people" },
        ]}
        onReorder={(_, from, to) => console.log("moved", from, to)}
      />
    </div>
  );
}
