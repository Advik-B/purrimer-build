import { ActionMenu } from "~/purrimer";

export default function Example() {
  return (
    <ActionMenu
      label="File"
      open
      items={[
        { label: "Edit file", leadingIcon: "pencil", trailingText: "E" },
        { label: "Copy permalink", leadingIcon: "link", trailingText: "Y" },
        { label: "View history", leadingIcon: "history" },
        { divider: true },
        { label: "Delete file", leadingIcon: "trash", variant: "danger" },
      ]}
      onSelect={(item) => console.log("picked", item.label)}
    />
  );
}
