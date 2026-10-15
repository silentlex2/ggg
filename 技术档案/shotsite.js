#!/usr/bin/env node
// shotsite.js - drive the live 职引 site through the OWB daemon and capture screenshots.
// Why: owb's own CLI mangles nested JSON through PowerShell; talk to the ctl channel directly.
// Usage: node shotsite.js <plan.json> [--tab N]
import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
const require = createRequire(import.meta.url);
const WS = require("C:/Users/z/AppData/Roaming/npm/node_modules/open-web-bridge/node_modules/ws");

const argv = process.argv.slice(2);
const planPath = argv[0];
const tabArg = argv.indexOf("--tab");
let TAB = tabArg >= 0 ? Number(argv[tabArg + 1]) : null;
const plan = JSON.parse(fs.readFileSync(planPath, "utf8"));
const OUT = plan.out || "F:\\zcode\\suiyi\\ggg\\过程截图\\v12";
fs.mkdirSync(OUT, { recursive: true });

const ws = new WS("ws://127.0.0.1:43917/ctl", { maxPayload: 256 * 1024 * 1024 });
let mid = 0;
const pend = new Map();
const call = (name, args = {}, timeout = 120) =>
  new Promise((res, rej) => {
    const id = "c" + (++mid);
    pend.set(id, { res, rej });
    ws.send(JSON.stringify({ type: "call", id, name, args, timeout }));
  });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

ws.on("message", (d) => {
  const m = JSON.parse(d.toString());
  if (m.type === "result" && pend.has(m.id)) {
    const { res, rej } = pend.get(m.id);
    pend.delete(m.id);
    m.ok ? res(m.data) : rej(new Error(JSON.stringify(m.error || m)));
  }
});

const T = (a) => Object.assign({ tabId: TAB }, a);
const ev = async (expression) => {
  const r = await call("evaluate", T({ expression, return_by_value: true, await_promise: true }));
  return r && typeof r === "object" && "value" in r ? r.value : r;
};

const bodyLen = () => ev("document.body.innerText.length");

const shot = async (name, full) => {
  // BUG: captureScreenshot times out unless the tab is the active one.
  try { await call("cdp", T({ method: "Page.bringToFront", params: {} }), 30); } catch {}
  await sleep(400);
  const r = await call("screenshot", T({ format: "png", full_page: !!full }), 180);
  const b64 = r && (r.data || r.image || r.base64);
  if (!b64) throw new Error("no image data: " + JSON.stringify(r).slice(0, 200));
  const p = path.join(OUT, name);
  fs.writeFileSync(p, Buffer.from(b64, "base64"));
  console.log("SAVED " + name + " " + fs.statSync(p).size + "B");
};

const waitIdle = async (maxMs, minLen) => {
  const t0 = Date.now();
  // 起始长度：必须先超过它 +300 才算「开始有输出」，否则会在页面本来就静止时立刻误判为空闲。
  const base = await bodyLen();
  const floor = minLen || base + 120;
  let prev = -1, stable = 0;
  await sleep(2500);
  while (Date.now() - t0 < maxMs) {
    const n = await bodyLen();
    if (n < floor) { prev = -1; await sleep(1500); continue; }
    if (n === prev) { stable++; if (stable >= 4) return n; } else { stable = 0; prev = n; }
    await sleep(1500);
  }
  console.log("   (waitIdle 超时，最后长度 " + prev + ")");
  return prev;
};

const ask = async (text) => {
  console.log(">> " + text.slice(0, 44));
  try { await call("cdp", T({ method: "Page.bringToFront", params: {} }), 30); } catch {}
  // 变量面板只在空对话时可见；对话开始后会折叠，这里必须容错。
  try { await call("fill", T({ selector: "textarea[placeholder*='用户问题']", value: text })); } catch {}
  await call("mouse_click", T({ selector: "textarea[placeholder*='输入问题']", mouse: true }));
  await sleep(300);
  await ev("(() => { const t = document.querySelector(\"textarea[placeholder*='输入问题']\"); t.select(); return 1; })()");
  await call("send_keys", T({ text }));
  await sleep(400);
  await call("send_keys", T({ keys: "Enter" }));
};

const newConv = async () => {
  await ev("(() => { const e = Array.from(document.querySelectorAll('div,button,a,span')).find(x => (x.innerText||'').trim() === '创建新对话'); if (e) e.click(); return !!e; })()");
  await sleep(3000);
};

try {
  await new Promise((res, rej) => { ws.once("open", res); ws.once("error", rej); });
  if (!TAB) {
    const tabs = await call("find_tab", { url_pattern: "chat/" + plan.site });
    TAB = Array.isArray(tabs) ? (tabs[0] && (tabs[0].tabId || tabs[0].id)) : (tabs && (tabs.tabId || tabs.id));
  }
  console.log("TAB = " + TAB);
  if (plan.emulate) { await call("emulate", T({ device: plan.emulate })); await sleep(800); }
  for (const step of plan.steps) {
    if (step.cdp) { await call("cdp", T({ method: step.cdp.method, params: step.cdp.params }), 40); await sleep(500); }
    if (step.navigate) { await call("navigate", T({ url: step.navigate, wait_until: "load" }), 120); await sleep(3000); }
    if (step.newConv) await newConv();
    if (step.fillVar) await call("fill", T({ selector: "textarea[placeholder*='用户问题']", value: step.fillVar }));
    if (step.fillMajor) await call("fill", T({ selector: "input.ant-input", value: step.fillMajor }));
    if (step.upload) {
      const b = fs.readFileSync(step.upload);
      await call("upload", T({ selector: "input[type=file]", files: [{ name: path.basename(step.upload), base64: b.toString("base64"), mime: step.mime || "application/pdf" }] }), 180);
      await sleep(2500);
    }
    if (step.ask) { await ask(step.ask); await waitIdle(step.maxMs || 60000, step.minLen); await sleep(1500); }
    if (step.sleep) await sleep(step.sleep);
    if (step.scrollTo) {
      await ev("(() => { const t = " + JSON.stringify(step.scrollTo) + "; const els = Array.from(document.querySelectorAll('*')).filter(e => (e.innerText||'').startsWith(t) && e.children.length < 400); const el = els[els.length-1]; if (el) { el.scrollIntoView({block:'start'}); return 1; } return 0; })()");
      await sleep(900);
    }
    if (step.scrollContains) {
      const r = await ev("(() => { const t = " + JSON.stringify(step.scrollContains) + "; const els = Array.from(document.querySelectorAll('div,p,span,li,td')).filter(e => (e.innerText||'').includes(t) && e.children.length < 60); const el = els[0]; if (el) { el.scrollIntoView({block:'start'}); return 1; } return 0; })()");
      console.log("   scrollContains=" + r);
      await sleep(900);
    }
    if (step.scrollTop !== undefined) {
      await ev("(() => { const c = Array.from(document.querySelectorAll('*')).find(e => String(e.className).includes('overflow-y-auto') && e.clientHeight > 100); if (c) { c.scrollTop = " + step.scrollTop + "; return c.scrollTop; } return -1; })()");
      await sleep(700);
    }
    if (step.emulate) { await call("emulate", T({ device: step.emulate })); await sleep(1200); }
    if (step.shot) await shot(step.shot, step.full);
    if (step.log) console.log("   len=" + (await bodyLen()));
  }
  console.log("DONE");
} catch (e) {
  console.log("ERR " + e.message);
  process.exitCode = 1;
} finally { try { ws.close(); } catch {} }
