#!/usr/bin/env node
/* 自建前端的纯逻辑单元测试（h5_unit.js）
 *
 * 为什么要有：h5_lint.py 能查语法和站点码，但查不了「进度会不会倒退」「历史串拼得对不对」，
 * 而这两块恰好是 v19 唯一自研的部分，也是最容易改坏的地方。它们不碰渲染，只读写 state，
 * 所以可以按函数名把源码抠出来、给几个 stub 直接在 node 里跑断言——不用浏览器、不用网络。
 *
 * 用法：
 *   node h5_unit.js            # 跑断言，失败退出 1
 *   node h5_unit.js --quiet    # 只打汇总行（给 h5_lint.py 调）
 */
const fs = require("fs");
const path = require("path");

const HTML = path.join(__dirname, "..", "前端", "职引-H5.html");
const quiet = process.argv.includes("--quiet");

/* 按函数名从 <script> 里抠出整段源码：从 "function NAME(" 起做花括号配对 */
function extract(js, name) {
  const start = js.indexOf("function " + name + "(");
  if (start < 0) throw new Error("没找到函数 " + name);
  let depth = 0;
  for (let k = js.indexOf("{", start); k < js.length; k++) {
    if (js[k] === "{") depth++;
    else if (js[k] === "}") { depth--; if (depth === 0) return js.slice(start, k + 1); }
  }
  throw new Error("函数 " + name + " 的花括号没闭合");
}

const html = fs.readFileSync(HTML, "utf8");
const m = html.match(/<script>([\s\S]*?)<\/script>/);
if (!m) { console.error("H5 里没有 <script> 块"); process.exit(1); }
const js = m[1];

/* const 字面量同理：从 "const NAME =" 抠到与之配对的 ";\n" */
function extractConst(js, name) {
  const start = js.indexOf("const " + name + " =");
  if (start < 0) throw new Error("没找到常量 " + name);
  let depth = 0;
  for (let k = js.indexOf("{", start); k < js.length; k++) {
    if (js[k] === "{") depth++;
    else if (js[k] === "}") { depth--; if (depth === 0) return js.slice(start, js.indexOf(";", k) + 1); }
  }
  throw new Error("常量 " + name + " 没闭合");
}

const consts = extractConst(js, "CN_NUM");
const body = ["setProgress", "applyProgress", "resetInterview", "scanProgress", "ctxOf"]
  .map((n) => extract(js, n)).join("\n\n");

const prelude = `
let state = { cid: "", uid: "u1", msgs: [], progress: 0, g: {}, file: null };
const saves = [];
function save(){ saves.push(state.progress); }
const bar = { id: "", className: "", innerHTML: "" };
const document = {
  getElementById(id){ return (id === "pv" && state.progress) ? bar : null; },
  createElement(){ return { id: "", className: "", innerHTML: "", remove(){} }; }
};
const $ = () => ({ appendChild(){}, classList: { add(){}, remove(){} }, style: {} });
`;

const factory = new Function(prelude + "\n" + consts + "\n" + body +
  "\nreturn { get state(){ return state; }, saves, bar, applyProgress, resetInterview, scanProgress, ctxOf };");
const api = factory();

let pass = 0, fail = 0;
function check(name, cond, got) {
  if (cond) { pass++; if (!quiet) console.log("  PASS  " + name); }
  else { fail++; console.log("  FAIL  " + name + (got === undefined ? "" : "  实际：" + JSON.stringify(got))); }
}

const S = api.state;

api.scanProgress("📊 面试进度：3/5");
check("进度行 3/5 -> 3", S.progress === 3, S.progress);

api.scanProgress("第 4 题 · 项目经历，讲一个你主导的事");
check("缺进度行时从「第 4 题」反推 -> 4", S.progress === 4, S.progress);

/* 最关键的一条：倒退必须被挡住（黄金集 E7 实测过 [1,2,3,2]） */
api.scanProgress("📊 面试进度：2/5");
check("进度行倒退 2/5 被挡（仍为 4）", S.progress === 4, S.progress);
api.scanProgress("第 2 题 · 继续");
check("「第 2 题」也被挡（仍为 4）", S.progress === 4, S.progress);

api.scanProgress("模拟面试复盘：第 1 题回答偏浅，第 3 题结构不错");
check("复盘文本里的「第 N 题」不推进度（仍为 4）", S.progress === 4, S.progress);

api.resetInterview();
check("resetInterview 归零", S.progress === 0, S.progress);
api.scanProgress("第 1 题 · 自我介绍");
check("归零后「第 1 题」可正常设为 1", S.progress === 1, S.progress);

api.scanProgress("第 二 题 · 说说你的项目");
check("中文数字「二」-> 2", S.progress === 2, S.progress);

S.msgs = [
  { role: "me", text: "我是化工专业" },
  { role: "bot", text: "好的，想找什么岗位" },
  { role: "me", text: "想找   重庆   的校招岗位" },
  { role: "me", text: "A".repeat(200) },
];
const ctx = api.ctxOf();
check("历史串以〔历史〕开头", ctx.startsWith("〔历史〕用户此前说过："), ctx.slice(0, 16));
check("历史串不含机器人发言", ctx.indexOf("想找什么岗位") < 0);
check("历史串压缩了连续空格", ctx.indexOf("想找 重庆 的校招岗位") >= 0, ctx.slice(0, 60));
check("超长发言被截到 90 字", ctx.indexOf("A".repeat(91)) < 0);
check("最多只取 3 条本人发言", (ctx.match(/；/g) || []).length <= 2);

S.msgs = [{ role: "bot", text: "你好" }];
check("无本人发言时历史串为空串", api.ctxOf() === "", api.ctxOf());

console.log((quiet ? "" : "\n") + "H5 单元测试：" + pass + " 过 / " + fail + " 失败");
process.exit(fail ? 1 : 0);