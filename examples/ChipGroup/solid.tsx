import { ChipGroup } from "~/purrimer";

const options = [
  { value: "all", label: "All" },
  { value: "unread", label: "Unread", count: 12 },
  { value: "mentions", label: "Mentions", icon: "mention" },
  { value: "snoozed", label: "Snoozed", disabled: true },
];

export default function Example() {
  return <ChipGroup ariaLabel="Filter inbox" options={options} value="unread" onChange={(v) => console.log("filter", v)} />;
}
