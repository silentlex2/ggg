#!/usr/bin/env node
// owbc.js - thin CLI over the OWB daemon ctl channel.
// Why: owb's own CLI parses --args through PowerShell, which mangles nested JSON.
// Usage: node owbc.js <tool> [jsonFile|jsonString] [--timeout N]
import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
const require = createRequire(import.meta.url);
const WS = require("C:/Users/z/AppData/Roaming/npm/node_modules/open-web-bridge/node_modules/ws");

const argv = process.argv.slice(2);
if (!argv.length) { console.log("usage: node owbc.js <tool> [json] [--timeout N]"); process.exit(0); }
let timeout = 90;
const ti = argv.indexOf("--timeout");
if (ti >= 0) { timeout = parseFloat(argv[ti + 1]); argv.splice(ti, 2); }
const name = argv[0];
let args = {};
if (argv[1]) {
  const raw = fs.existsSync(argv[1]) ? fs.readFileSync(argv[1], "utf8") : argv[1];
  args = JSON.parse(raw);
}
const ws = new WS("ws://127.0.0.1:43917/ctl", { maxPayload: 256 * 1024 * 1024 });
ws.once("open", () => ws.send(JSON.stringify({ type: "call", id: "c1", name, args, timeout })));
ws.once("error", (e) => { console.error("CONNECT_ERROR " + e.message); process.exit(1); });
ws.on("message", (d) => {
  const m = JSON.parse(d.toString());
  if (m.type === "result" && m.id === "c1") {
    console.log(JSON.stringify(m.ok ? m.data : { ok: false, error: m.error, code: m.code }, null, 2));
    ws.close();
    process.exit(m.ok ? 0 : 1);
  }
});
