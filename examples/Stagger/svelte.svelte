<script lang="ts">
  import { Chip, Stagger } from "$lib/purrimer";
</script>

<Stagger name="pounce" style="display: flex; flex-wrap: wrap; gap: 8px">
  <Chip text="Design" />
  <Chip text="Shipped" tone="success" />
  <Chip text="Archive" tone="neutral" />
  <Chip text="Docs" tone="info" />
</Stagger>
