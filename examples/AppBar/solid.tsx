import { AppBar } from "~/purrimer";

export default function Example() {
  return (
    <div>
      <AppBar
        title="Inbox"
        back
        large
        actions={[
          { icon: "search", label: "Search", onClick: () => console.log("search") },
          { icon: "kebab-horizontal", label: "More" },
        ]}
        onBack={() => history.back()}
      />
    </div>
  );
}
