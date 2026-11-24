<script lang="ts">
  import { Card, Motion } from "$lib/purrimer";
</script>

<div style="display: flex; flex-direction: column; gap: 12px">
  <Motion name="rise">
    <Card title="Saved to drafts"><p style="margin: 0">Your reply is waiting in Drafts.</p></Card>
  </Motion>
  <Motion name="pounce" index={1}>
    <Card title="New badge"><p style="margin: 0">You reviewed ten pull requests this week.</p></Card>
  </Motion>
  <Motion name="bask" index={2} style="border-radius: 12px">
    <Card title="Linked from the release notes"><p style="margin: 0">A halo shows where the link points.</p></Card>
  </Motion>
</div>
