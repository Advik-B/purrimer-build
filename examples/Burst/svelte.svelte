<script lang="ts">
  import { Burst, Card, MotionScope } from "$lib/purrimer";

  // Bump merged (merged += 1) to burst.
  let merged = $state(0);
</script>

<MotionScope kind="playful">
  <Burst fire={merged} style="display: block">
    <Card title="Pull request merged"><p style="margin: 0">All checks passed.</p></Card>
  </Burst>
</MotionScope>
