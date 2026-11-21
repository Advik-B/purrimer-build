import { AlertSheet } from "~/purrimer";

export default function Example() {
  return (
    <AlertSheet
      open
      inline
      icon="critical"
      title="Delete 3 photos?"
      message="They stay in Recently deleted for 30 days, then they are gone for good."
      buttons={[{ label: "Cancel" }, { label: "Delete", variant: "danger" }]}
      onButton={(i) => console.log("button", i)}
    />
  );
}
