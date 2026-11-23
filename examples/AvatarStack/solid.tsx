import { AvatarStack } from "~/purrimer";

const people = ["Mona Lisa", "Hubot", "Ada Lovelace", "Octo Cat", "Grace Hopper", "Linus Torvalds"];

export default function Example() {
  return (
    <div style={{ display: "flex", gap: "32px", "align-items": "center" }}>
      <AvatarStack people={people} />
      <AvatarStack people={people.slice(0, 3)} size={32} />
    </div>
  );
}
