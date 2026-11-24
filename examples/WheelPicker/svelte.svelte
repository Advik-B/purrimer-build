<script lang="ts">
  import { WheelPicker, type WheelColumn } from "$lib/purrimer";

  const pad = (n: number) => String(n).padStart(2, "0");
  let time = $state({ hour: "07", minute: "30", half: "AM" });
  const columns: WheelColumn[] = $derived([
    { label: "Hour", options: Array.from({ length: 12 }, (_, i) => pad(i + 1)), value: time.hour, align: "end" },
    { label: "Minute", options: Array.from({ length: 12 }, (_, i) => pad(i * 5)), value: time.minute },
    { label: "AM or PM", options: ["AM", "PM"], value: time.half, align: "start" },
  ]);
  const keys = ["hour", "minute", "half"] as const;
</script>

<WheelPicker {columns} onchange={(c, v) => (time[keys[c]] = v)} />
