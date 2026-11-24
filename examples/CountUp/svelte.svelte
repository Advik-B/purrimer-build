<script lang="ts">
  import { CountUp } from "$lib/purrimer";
</script>

<div style="display: flex; gap: 32px; align-items: baseline">
  <CountUp to={1284} class="text-stat" />
  <CountUp to={3742.5} decimals={2} prefix="€" mode="roll" class="text-stat-small" />
</div>
