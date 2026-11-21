// Mounts one example into #frame, then sets data-ready (or data-error) on <body> for shoot.ts.
// Each page loads one flavour: the class-based sheets, or the classless one on its own.
import baseCss from "../stage/purrimer/css/purrimer.css?inline";
import componentsCss from "../stage/purrimer/css/purrimer-components.css?inline";
import classlessCss from "../stage/purrimer/css/purrimer-classless.css?inline";

const params = new URLSearchParams(location.search);
const target = params.get("target") ?? "css";
const component = params.get("component") ?? "";
const theme = params.get("theme") ?? "blanc";
const style = document.createElement("style");
style.textContent = target === "classless" ? classlessCss : baseCss + componentsCss;
document.head.prepend(style);
const frame = document.getElementById("frame")!;
frame.style.width = `${params.get("w") ?? 360}px`;
frame.style.height = `${params.get("h") ?? 120}px`;
if (params.get("bleed") === "1") frame.classList.add("bleed");
if (theme !== "blanc") document.documentElement.setAttribute("data-theme", theme);

const cssExamples = import.meta.glob<string>("../stage/examples/*/css.html", { query: "?raw", import: "default" });
const classlessExamples = import.meta.glob<string>("../stage/examples/*/classless.html", {
  query: "?raw",
  import: "default",
});
const svelteExamples = import.meta.glob("../stage/examples/*/svelte.svelte");
const solidExamples = import.meta.glob("../stage/examples/*/solid.tsx");

function pick<T>(glob: Record<string, () => Promise<T>>, file: string): () => Promise<T> {
  const key = `../stage/examples/${component}/${file}`;
  const load = glob[key];
  if (!load) throw new Error(`No ${file} example for ${component}`);
  return load;
}

async function mount(): Promise<void> {
  if (target === "css") {
    frame.innerHTML = await pick(cssExamples, "css.html")();
  } else if (target === "classless") {
    frame.innerHTML = await pick(classlessExamples, "classless.html")();
  } else if (target === "svelte") {
    const { mount } = await import("svelte");
    const mod = (await pick(svelteExamples, "svelte.svelte")()) as { default: never };
    mount(mod.default, { target: frame });
  } else if (target === "solid") {
    const { render } = await import("@solidjs/web");
    const mod = (await pick(solidExamples, "solid.tsx")()) as { default: () => never };
    render(mod.default, frame);
  } else {
    throw new Error(`Unknown target ${target}`);
  }
  await document.fonts.ready;
  await new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)));
}

mount().then(
  () => document.body.setAttribute("data-ready", ""),
  (err) => {
    console.error(err);
    document.body.setAttribute("data-error", String(err?.stack ?? err));
  },
);
