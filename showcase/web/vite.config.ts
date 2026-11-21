// stage/ holds copies of the generated code and the examples, made by scripts/showcase.py.
// Builds one page that renders a single example: render.html?target=svelte&component=Button&theme=noir&w=360&h=120
import { fileURLToPath } from "node:url";
import solid from "@solidjs/vite-plugin";
import { svelte } from "@sveltejs/vite-plugin-svelte";
import { defineConfig } from "vite";

const here = (p: string) => fileURLToPath(new URL(p, import.meta.url));

export default defineConfig({
  root: here("."),
  base: "./",
  logLevel: "warn",
  plugins: [svelte(), solid({ include: /\.tsx$/ })],
  resolve: {
    alias: {
      "$lib/purrimer": here("stage/purrimer/svelte/index.ts"),
      "~/purrimer": here("stage/purrimer/solid/index.ts"),
    },
  },
  build: {
    outDir: here("../out/web-build"),
    emptyOutDir: true,
    chunkSizeWarningLimit: 4096,
    rollupOptions: { input: here("render.html") },
  },
});
