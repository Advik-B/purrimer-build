import { UnderlineNav } from "~/purrimer";

const items = [
  { label: "Code", icon: "code" },
  { label: "Issues", icon: "issue-opened", count: 12 },
  { label: "Pull requests", icon: "git-pull-request", count: 3 },
  { label: "Actions", icon: "play" },
];

export default function Example() {
  return <UnderlineNav ariaLabel="Repository" items={items} current={0} onSelect={(i) => console.log("page", i)} />;
}
