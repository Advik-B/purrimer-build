import { createSignal } from "solid-js";
import { Select } from "~/purrimer";

export default function Example() {
  const [size, setSize] = createSignal(1);
  return <Select label="T-shirt size" options={["Small", "Medium", "Large"]} value={size()} onChange={setSize} />;
}
