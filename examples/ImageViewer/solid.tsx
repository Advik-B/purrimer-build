import { ImageViewer } from "~/purrimer";
import photo from "./photo.jpg";

export default function Example() {
  return <ImageViewer inline src={photo} alt="Sunset over the lake" caption="Lake Ilgen, an hour before dark" onClose={() => console.log("close")} />;
}
