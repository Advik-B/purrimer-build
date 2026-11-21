// Renders every example of the web targets in Chromium and screenshots it.
// Usage: node shoot.ts <manifest.json>   (written by scripts/showcase.py; Node 24 runs TypeScript directly)
// Exits 1 if any example logs a console error or warning, throws, fails a request,
// or uses a pm-* class that no stylesheet defines.
import { mkdirSync, readFileSync } from "node:fs";
import type { AddressInfo } from "node:net";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { chromium } from "playwright";
import { preview } from "vite";

interface ManifestComponent {
  name: string;
  width: number;
  height: number;
  bleed: boolean;
}

interface Manifest {
  out: string;
  scale: number;
  targets: string[];
  themes: string[];
  components: ManifestComponent[];
}

const here = dirname(fileURLToPath(import.meta.url));
const manifest = JSON.parse(readFileSync(process.argv[2], "utf-8")) as Manifest;
const server = await preview({
  root: here,
  configFile: join(here, "vite.config.ts"),
  logLevel: "warn",
  preview: { port: 0, strictPort: false, host: "127.0.0.1" },
});
const { port } = server.httpServer.address() as AddressInfo;
const base = `http://127.0.0.1:${port}/`;
const browser = await chromium.launch();
const context = await browser.newContext({ deviceScaleFactor: manifest.scale, reducedMotion: "reduce" });
const failures: string[] = [];

// Runs in the page: pm-* classes inside #frame that no loaded stylesheet mentions.
function undefinedPmClasses(): string[] {
  const selectors: string[] = [];
  const collect = (rule: CSSRule): void => {
    if (rule instanceof CSSStyleRule) selectors.push(rule.selectorText);
    if ("cssRules" in rule) for (const r of Array.from((rule as CSSGroupingRule).cssRules)) collect(r);
  };
  for (const sheet of Array.from(document.styleSheets)) for (const rule of Array.from(sheet.cssRules)) collect(rule);
  const all = selectors.join(" ");
  const used = new Set<string>();
  for (const el of Array.from(document.querySelectorAll("#frame [class]"))) {
    for (const c of Array.from(el.classList)) if (c.startsWith("pm-")) used.add(c);
  }
  return [...used].filter((c) => !new RegExp(`\.${c}(?![\w-])`).test(all));
}

for (const target of manifest.targets) {
  for (const comp of manifest.components) {
    for (const theme of manifest.themes) {
      const label = `${target}/${comp.name}/${theme}`;
      const problems: string[] = [];
      const page = await context.newPage();
      // The viewport is the frame, so overlays that portal to <body> or use 100vw land inside the screenshot.
      await page.setViewportSize({ width: comp.width, height: comp.height });
      page.on("console", (msg) => {
        if (msg.type() === "error" || msg.type() === "warning") problems.push(`console.${msg.type()}: ${msg.text()}`);
      });
      page.on("pageerror", (err) => problems.push(`page error: ${err.message}`));
      page.on("requestfailed", (req) => problems.push(`request failed: ${req.url()}`));
      page.on("response", (res) => {
        if (res.status() >= 400) problems.push(`HTTP ${res.status()}: ${res.url()}`);
      });
      const query = new URLSearchParams({
        target,
        component: comp.name,
        theme,
        w: String(comp.width),
        h: String(comp.height),
        bleed: comp.bleed ? "1" : "0",
      });
      await page.goto(`${base}render.html?${query}`);
      await page.waitForSelector("body[data-ready], body[data-error]", { timeout: 15000 });
      const error = await page.getAttribute("body", "data-error");
      if (error) problems.push(error);
      const missing = await page.evaluate(undefinedPmClasses);
      if (missing.length) problems.push(`classes with no CSS rule: ${missing.join(", ")}`);
      const empty = await page.evaluate(() => document.getElementById("frame")?.children.length === 0);
      if (empty) problems.push("rendered nothing");
      const file = join(manifest.out, target, `${comp.name}-${theme}.png`);
      mkdirSync(dirname(file), { recursive: true });
      await page.locator("#frame").screenshot({ path: file, animations: "disabled", caret: "hide" });
      await page.close();
      if (problems.length) failures.push(`${label}\n  ${problems.join("\n  ")}`);
      else console.log(`ok ${label}`);
    }
  }
}

await browser.close();
await new Promise<void>((resolve) => server.httpServer.close(() => resolve()));
if (failures.length) {
  console.error(`\n${failures.length} web example(s) failed:\n${failures.join("\n")}`);
  process.exit(1);
}
