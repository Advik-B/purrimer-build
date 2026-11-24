import { ActionSheet } from "~/purrimer";

const items = [
  { label: "Share", icon: "share-android" },
  { label: "Copy link", icon: "link", description: "Anyone with the link can view" },
  { label: "Move to", icon: "file-directory", items: [{ label: "Holidays" }, { label: "Family" }] },
  { label: "Favourite", icon: "star", checked: true },
  { divider: true },
  { label: "Delete", icon: "trash", variant: "danger" as const },
];

export default function Example() {
  return <ActionSheet open inline title="Photo.jpg" items={items} onSelect={(item) => console.log("chose", item.label)} />;
}
