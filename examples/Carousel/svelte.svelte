<script lang="ts">
  import { Carousel } from "$lib/purrimer";

  const slides = [
    { title: "Morning walk", tone: "var(--bgColor-accent-muted)" },
    { title: "Market haul", tone: "var(--bgColor-success-muted)" },
    { title: "Rainy afternoon", tone: "var(--bgColor-attention-muted)" },
    { title: "Late train", tone: "var(--bgColor-done-muted)" },
  ];
</script>

<Carousel ariaLabel="Highlights" items={slides} peek height={220}>
  {#snippet slide(item)}
    <div class="text-body-large" style="display: flex; align-items: flex-end; height: 100%; padding: 16px; box-sizing: border-box; background: {item.tone}">
      {item.title}
    </div>
  {/snippet}
</Carousel>
