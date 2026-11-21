import { Timeline } from "~/purrimer";

export default function Example() {
  return (
    <Timeline
      items={[
        { actor: "mona", content: "opened this pull request", icon: "git-pull-request", tone: "success" },
        { actor: "hubot", content: "added 3 commits", icon: "git-commit", condensed: true },
        { actor: "ada", content: "approved these changes", icon: "check", tone: "accent" },
        { break: true },
        { actor: "mona", content: "merged into main", icon: "git-merge", tone: "done" },
      ]}
    />
  );
}
