import { FAB } from "~/purrimer";

export default function Example() {
  return (
    <div style={{ display: "flex", gap: "16px", "align-items": "center" }}>
      <FAB
        label="New note"
        onClick={() => console.log("new note")}
        actions={[
          { icon: "device-camera", label: "Take photo" },
          { icon: "checklist", label: "Checklist" },
        ]}
        onAction={(item) => console.log("chose", item.label)}
      />
      <FAB icon="pencil" label="Compose" extended />
    </div>
  );
}
