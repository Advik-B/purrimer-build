import { FAB, HoldMenu } from "~/purrimer";

export default function Example() {
  return (
    <div style={{ position: "relative", height: "420px" }}>
      <p class="text-body-medium" style={{ margin: 0, padding: "16px" }}>Hold the button for more ways to start a note.</p>
      <div style={{ position: "absolute", right: "16px", bottom: "16px" }}>
        <HoldMenu
          defaultOpen
          ariaLabel="Start something"
          items={[
            { label: "New note", icon: "note" },
            { label: "Take photo", icon: "device-camera" },
            { label: "Checklist", icon: "checklist" },
          ]}
          onSelect={(item) => console.log("chose", item.label)}
        >
          <FAB label="New note" onClick={() => console.log("new note")} />
        </HoldMenu>
      </div>
    </div>
  );
}
