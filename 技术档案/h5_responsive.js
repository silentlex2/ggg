#!/usr/bin/env node
// h5_responsive.js — 五档视口下的布局回归：横向溢出、关键元素存在、截图留证。
// 只做布局测量，不发任何请求，所以可以随时跑、不烧平台额度。
import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
const require = createRequire(import.meta.url);
const WS = require("C:/Users/z/AppData/Roaming/npm/node_modules/open-web-bridge/node_modules/ws");

const OUT = process.argv.includes("--out")
  ? process.argv[process.argv.indexOf("--out") + 1]
  : "F:\\zcode\\suiyi\\ggg\\过程截图\\h5-responsive";
fs.mkdirSync(OUT, { recursive: true });

const VIEWPORTS = [
  { name: "320-小屏手机", width: 320, height: 640, dpr: 2 },
  { name: "390-主流手机", width: 390, height: 844, dpr: 2 },
  { name: "768-平板竖屏", width: 768, height: 1024, dpr: 1 },
  { name: "1024-平板横屏", width: 1024, height: 768, dpr: 1 },
  { name: "1440-桌面", width: 1440, height: 900, dpr: 1 },
];

const ws = new WS("ws://127.0.0.1:43917/ctl", { maxPayload: 256 * 1024 * 1024 });
let mid = 0;
const pend = new Map();
const call = (name, args = {}, timeout = 120) =>
  new Promise((res, rej) => {
    const id = "c" + ++mid;
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

let TAB = null;
const T = (a) => Object.assign({ tabId: TAB }, a);
const ev = async (expression) => {
  const r = await call("evaluate", T({ expression, return_by_value: true, await_promise: true }));
  return r && typeof r === "object" && "value" in r ? r.value : r;
};
const shot = async (name) => {
  try { await call("cdp", T({ method: "Page.bringToFront", params: {} }), 30); } catch {}
  await sleep(400);
  const r = await call("screenshot", T({ format: "png" }), 180);
  const b64 = r && (r.data || r.image || r.base64);
  if (b64) fs.writeFileSync(path.join(OUT, name), Buffer.from(b64, "base64"));
};

const MEASURE = `(function(){
  var doc = document.documentElement, body = document.body;
  var over = [];
  [].forEach.call(document.querySelectorAll('table,.bubble,.composer,.box,.guide,.footer,.foot'), function(el){
    var r = el.getBoundingClientRect();
    if (r.right > doc.clientWidth + 1 || r.left < -1) over.push((el.className||el.tagName) + ':' + Math.round(r.left) + '~' + Math.round(r.right));
  });
  return JSON.stringify({
    clientWidth: doc.clientWidth,
    scrollWidth: Math.max(doc.scrollWidth, body.scrollWidth),
    overflowX: Math.max(doc.scrollWidth, body.scrollWidth) - doc.clientWidth,
    offenders: over.slice(0, 5),
    headerWrapped: (function(){ var s=document.querySelector('.titles span'); return s ? s.getBoundingClientRect().height > 26 : null; })(),
    composerVisible: (function(){ var c=document.querySelector('.composer'); if(!c) return null; var r=c.getBoundingClientRect(); return r.height > 40 && r.bottom <= window.innerHeight + 2; })()
  });
})()`;

try {
  await new Promise((res, rej) => { ws.once("open", res); ws.once("error", rej); });
  const tabs = await call("find_tab", { url_pattern: "H5.html" });
  const list = Array.isArray(tabs) ? tabs : (tabs && tabs.tabs) || [];
  TAB = list[0] && (list[0].tabId || list[0].id);
  if (!TAB) { console.log("没有打开的 H5 标签页"); process.exit(2); }

  const rows = [];
  for (const vp of VIEWPORTS) {
    await call("cdp", T({
      method: "Emulation.setDeviceMetricsOverride",
      params: { width: vp.width, height: vp.height, deviceScaleFactor: vp.dpr, mobile: vp.width < 600 },
    }));
    await sleep(900);
    const m = JSON.parse(await ev(MEASURE));
    await shot("viewport-" + vp.name + ".png");
    rows.push(Object.assign({ name: vp.name, width: vp.width }, m));
    console.log(vp.name + "  溢出 " + m.overflowX + "px  输入框可见 " + m.composerVisible +
      "  头部折行 " + m.headerWrapped + (m.offenders.length ? "  越界元素 " + m.offenders.join(",") : ""));
  }
  await call("cdp", T({ method: "Emulation.clearDeviceMetricsOverride", params: {} }));

  const bad = rows.filter((r) => r.overflowX > 1 || r.offenders.length || r.composerVisible === false);
  console.log("");
  console.log("---RESPONSIVE_SUMMARY---");
  console.log("VIEWPORTS: " + rows.length);
  console.log("FAIL: " + bad.length);
  bad.forEach((r) => console.log("  - " + r.name + " 溢出" + r.overflowX + "px 越界" + r.offenders.join("|")));
  console.log("OUT: " + OUT);
  console.log("---END---");
  process.exitCode = bad.length ? 1 : 0;
} catch (e) {
  console.error("失败：" + (e && e.message ? e.message : e));
  process.exitCode = 1;
} finally {
  ws.close();
}
