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
    </div>
  );
}
