import { lstatSync, rmSync } from "node:fs";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import path from "node:path";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const output = path.resolve(root, "dist");
if (path.dirname(output) !== root || path.basename(output) !== "dist") {
  throw new Error("Neověřená cesta výstupu.");
}
try {
  if (lstatSync(output).isSymbolicLink()) throw new Error("dist nesmí být symbolický odkaz.");
  rmSync(output, { recursive: true, force: true });
} catch (error) {
  if (error.code !== "ENOENT") throw error;
}

const cli = path.join(root, "node_modules", "@11ty", "eleventy", "cmd.cjs");
const result = spawnSync(process.execPath, [cli, "--config=.eleventy.cjs"], {
  cwd: root,
  stdio: "inherit"
});
if (result.error) throw result.error;
process.exit(result.status ?? 1);
