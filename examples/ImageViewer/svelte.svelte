<script lang="ts">
  import { ImageViewer } from "$lib/purrimer";
  import photo from "./photo.jpg";
</script>

<ImageViewer inline src={photo} alt="Sunset over the lake" caption="Lake Ilgen, an hour before dark" onclose={() => console.log("close")} />
