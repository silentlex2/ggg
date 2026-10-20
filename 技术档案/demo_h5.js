#!/usr/bin/env node
// demo_h5.js — 把自建 H5 的演示动作脚本化：清场 -> 逐个场景跑到"可拍状态" -> 截图 + 记耗时。
// 目的不是替代录屏，而是让"录坏了重来"有确定动作：每一步做什么、等多久、画面长什么样都可复现。
// 用法：node demo_h5.js [--out 目录] [--tab N] [--only 问诊,岗位]
import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
const require = createRequire(import.meta.url);
const WS = require("C:/Users/z/AppData/Roaming/npm/node_modules/open-web-bridge/node_modules/ws");

const H5 = "file:///F:/zcode/suiyi/ggg/%E5%89%8D%E7%AB%AF/%E8%81%8C%E5%BC%95-H5.html";
const argv = process.argv.slice(2);
const argOf = (name, dflt) => { const i = argv.indexOf(name); return i >= 0 ? argv[i + 1] : dflt; };
const OUT = argOf("--out", "F:\\zcode\\suiyi\\ggg\\过程截图\\demo-rehearsal");
const ONLY = (argOf("--only", "") || "").split(",").filter(Boolean);
fs.mkdirSync(OUT, { recursive: true });

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
const shot = async (name, full) => {
  try { await call("cdp", T({ method: "Page.bringToFront", params: {} }), 30); } catch {}
  await sleep(400);
  const r = await call("screenshot", T({ format: "png", full_page: !!full }), 180);
  const b64 = r && (r.data || r.image || r.base64);
  if (!b64) throw new Error("截图失败：" + JSON.stringify(r).slice(0, 160));
  const p = path.join(OUT, name);
  fs.writeFileSync(p, Buffer.from(b64, "base64"));
  console.log("  SAVED " + name + "  " + (fs.statSync(p).size / 1024).toFixed(0) + "KB");
};

// 等一轮回答结束：H5 里 busy 为 false 表示可以再发
const waitDone = async (maxMs = 90000) => {
  const t0 = Date.now();
  await sleep(600);
  while (Date.now() - t0 < maxMs) {
    const busy = await ev("busy === true");
    if (busy === false) return (Date.now() - t0) / 1000;
    await sleep(700);
  }
  return -1;
};

const steps = [
  {
    key: "问诊", title: "① 三步问诊：专业 / 城市 / 最急的事",
    run: async () => {
      await ev("document.querySelector('.card[data-guide]') && document.querySelector('.card[data-guide]').click(); 'ok'");
      await sleep(600);
      await ev(`(function(){
        function byText(sel, t){ return Array.prototype.filter.call(document.querySelectorAll(sel), function(b){ return b.textContent.trim() === t; })[0]; }
        byText('#gmajor .chip', '化学工程与工艺').click();
        byText('#gcity .chip', '重庆两江新区').click();
        byText('#gneed .chip', '找对口岗位').click();
        return 'picked';
      })()`);
      await sleep(500);
      await shot("01-三步问诊.png");
    },
  },
  {
    key: "岗位", title: "② 直接问 -> 岗位表 + 溯源标签",
    run: async () => {
      await ev("document.getElementById('gmake').click(); 'sent'");
      const sec = await waitDone();
      await ev("var r=[...document.querySelectorAll('.row.bot')]; r.length && r[r.length-1].scrollIntoView({block:'start'}); 'ok'");
      await sleep(700);
      // 不要整页截图：页面用了 sticky 的头部和输入框，整页模式会把它们重复画在页面中段，
      // 看起来像"表头浮在内容上"。录屏本来就是视口，这里也只拍视口。
      await shot("02-岗位匹配.png");
      return sec;
    },
  },
  {
    key: "面试", title: "③ 模拟面试首题 + 快捷按钮",
    run: async () => {
      await ev("document.getElementById('newChat').onclick = null; localStorage.removeItem('zhiyin.v1'); location.reload(); 'reset'");
      await sleep(3500);
      await ev("send('来一场模拟面试，目标岗位是化工工艺工程师'); 'sent'");
      const sec = await waitDone();
      await ev("var r=[...document.querySelectorAll('.row.bot')]; r.length && r[r.length-1].scrollIntoView({block:'start'}); 'ok'");
      await sleep(700);
      await shot("03-模拟面试.png");
      return sec;
    },
  },
];

try {
  await new Promise((res, rej) => { ws.once("open", res); ws.once("error", rej); });
  // 注意：页面地址里的中文是百分号编码的（…%E8%81%8C%E5%BC%95-H5.html），
  // 拿中文去匹配永远匹配不上，只能用 ASCII 片段。
  let tabs = await call("find_tab", { url_pattern: "H5.html" });
  if (!tabs || (Array.isArray(tabs) && !tabs.length)) {
    tabs = await call("find_tab", { url_pattern: "file://" });
  }
  // find_tab 返回的是 { tabs: [...], count: n }，不是裸数组
  const list = Array.isArray(tabs) ? tabs : (tabs && tabs.tabs) || [];
  const first = list[0];
  TAB = first && (first.tabId || first.id);
  if (!TAB) {
    console.log("没有打开的 H5 标签页，先自己开一次：");
    console.log("  owb open \"" + H5 + "\" --new-tab true");
    process.exit(2);
  }
  console.log("TAB = " + TAB + "  输出目录 " + OUT);
  const timings = [];
  for (const step of steps) {
    if (ONLY.length && !ONLY.includes(step.key)) continue;
    console.log("\n" + step.title);
    const t0 = Date.now();
    const waited = await step.run();
    const total = (Date.now() - t0) / 1000;
    timings.push({ key: step.key, total, answer: waited === undefined ? "-" : waited.toFixed(1) });
    console.log("  用时 " + total.toFixed(1) + "s" + (waited >= 0 ? "（其中等回答 " + waited.toFixed(1) + "s）" : ""));
  }
  console.log("\n---DEMO_SUMMARY---");
  for (const t of timings) console.log(t.key + ": " + t.total.toFixed(1) + "s  等回答 " + t.answer + "s");
  console.log("OUT: " + OUT);
  console.log("---END---");
} catch (e) {
  console.error("失败：" + (e && e.message ? e.message : e));
  process.exitCode = 1;
} finally {
  ws.close();
}
