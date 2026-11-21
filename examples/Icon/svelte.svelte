<script lang="ts">
  import { Icon } from "$lib/purrimer";
</script>

<div style="display: flex; gap: 16px; align-items: center">
  <Icon name="heart" />
  <Icon name="star" />
  <Icon name="bell" />
  <Icon name="bell" size={24} label="Notifications" />
  <span style="color: var(--fgColor-danger)"><Icon name="heart" size={24} /></span>
</div>
