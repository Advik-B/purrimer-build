<script lang="ts">
  import { AvatarStack } from "$lib/purrimer";

  const people = ["Mona Lisa", "Hubot", "Ada Lovelace", "Octo Cat", "Grace Hopper", "Linus Torvalds"];
</script>

<div style="display: flex; gap: 32px; align-items: center">
  <AvatarStack {people} />
  <AvatarStack people={people.slice(0, 3)} size={32} />
</div>
