import { ListItem, ListSection } from "~/purrimer";

export default function Example() {
  return (
    <div style={{ "padding-top": "16px" }}>
      <ListSection header="Account">
        <ListItem icon="person" headline="Profile" chevron />
        <ListItem icon="key" headline="Password" chevron />
      </ListSection>
    </div>
  );
}
