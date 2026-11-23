<script lang="ts">
  import { IconButton, ToolTip } from "$lib/purrimer";
</script>

<div style="display: flex; gap: 8px; margin-top: 40px">
  <ToolTip text="Edit"><IconButton icon="pencil" label="Edit" /></ToolTip>
  <ToolTip text="Delete"><IconButton icon="trash" label="Delete" /></ToolTip>
  <ToolTip text="Copy to clipboard (Ctrl+C)" open><IconButton icon="copy" label="Copy" /></ToolTip>
  <ToolTip text="Tokens are named design decisions that every target reads." whatsThis placement="bottom">
    <IconButton icon="question" label="What is this?" />
  </ToolTip>
</div>
