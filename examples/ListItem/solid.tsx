import { ListItem } from "~/purrimer";

export default function Example() {
  return (
    <div role="list">
      <ListItem
        icon="bell"
        headline="Notifications"
        supporting="Mentions and replies"
        trailing="On"
        chevron
        onClick={() => console.log("open notifications")}
      />
      <ListItem icon="globe" headline="Language" trailing="English" />
      <ListItem
        icon="mail"
        headline="Weekly digest"
        trailing="Mon"
        swipeStart={{ label: "Mark as read", icon: "check", tone: "accent", onSwipe: () => console.log("read") }}
        swipeEnd={{ label: "Archive", icon: "archive", tone: "success", onSwipe: () => console.log("archive") }}
      />
    </div>
  );
}
