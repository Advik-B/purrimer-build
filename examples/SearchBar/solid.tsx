import { createSignal } from "solid-js";
import { SearchBar } from "~/purrimer";

export default function Example() {
  const [query, setQuery] = createSignal("");
  const [recent, setRecent] = createSignal("kittens");
  return (
    <div style={{ display: "grid", gap: "16px" }}>
      <SearchBar placeholder="Search messages" value={query()} onValue={setQuery} onSubmit={(q) => console.log("search", q)} />
      <SearchBar value={recent()} onValue={setRecent} />
    </div>
  );
}
