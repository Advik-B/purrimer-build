<script lang="ts">
  import { SearchBar } from "$lib/purrimer";

  let query = $state("");
  let recent = $state("kittens");
</script>

<div style="display: grid; gap: 16px">
  <SearchBar placeholder="Search messages" bind:value={query} onsubmit={(q) => console.log("search", q)} />
  <SearchBar bind:value={recent} />
</div>
