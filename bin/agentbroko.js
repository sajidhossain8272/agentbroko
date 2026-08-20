#!/usr/bin/env node
const { spawnSync } = require("node:child_process");
const path = require("node:path");
const args = process.argv.slice(2);
const candidates = process.platform === "win32" ? ["python", "py"] : ["python3", "python"];
const bundledSrc = path.resolve(__dirname, "..", "src");
const separator = process.platform === "win32" ? ";" : ":";
const env = { ...process.env, PYTHONPATH: process.env.PYTHONPATH ? `${bundledSrc}${separator}${process.env.PYTHONPATH}` : bundledSrc };
let result;
for (const python of candidates) { result = spawnSync(python, ["-m", "agentbroko", ...args], { stdio: "inherit", env }); if (!result.error) break; }
if (result?.error) { console.error("AgentBroko needs Python 3.10+ installed. See docs/INSTALL.md."); process.exit(1); }
process.exit(result.status ?? 1);
