# -*- coding: utf-8 -*-
"""v14：只改提示词 —— 修黄金集多轮用例暴露的四个真实缺陷。

依据（2026-10-20 全量 40 条实测）：
  E5  岗位分支不消费会话历史：上一轮刚说「重庆和成都」，追问「那这两个城市哪个更适合我」
      → 回「你这两个城市具体是哪两个、你什么专业」，条件全丢。
  E1  面试官把「技术性陈述式作答」当成知识库外问题踢出面试（约 2/7 次回「这个不在我的资料范围内」）。
  E3  「重练第 3 题」重出的是重新生成的第 3 题，不是原题（原题前 30 字重合度 0），属于打折。
  E4  「继续面试」偶发不回面试话术、丢进度行。

做法：往对应 LLM 节点的 system 提示词末尾追加纪律块（带幂等标记，重复执行不会叠加）。
然后照 v13 的教训：**先把草稿改好，再 copy 一次**，站点才会绑到新图。

用法：
    python build_v14.py --apply
    python build_v14.py --apply --src <应用ID>
"""
import argparse
import json
import os
import ssl
import sys
import time
import urllib.error
import urllib.request

BASE = "https://aiagent.cqut.edu.cn:31134"
HERE = os.path.dirname(os.path.abspath(__file__))
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

SRC = "accd6dd5-79f7-429c-8e11-a46a6f5e6e87"   # v13 草稿源（25 节点）
ICON = "ff8cb252-6223-4c43-9eb7-22844fd9adfa"

MARK = "〔v14 多轮纪律〕"

JOB_RULES = """

## 多轮追问纪律〔v14 多轮纪律〕（优先级高于本提示词里其它一切条目）

1. **历史里的条件默认沿用**：会话历史里已经出现过的城市、专业、目标岗位、薪资期望、技能，直接当已知条件用，不要重复询问。
2. **省略句追问要直接作答**：用户说「那这两个城市哪个更适合我」「这两个岗位选哪个」「哪个更好」时，从历史里取出对应的城市或岗位**直接比较**，给出判断维度（岗位数量、行业匹配度、生活成本、通勤、落户与补贴政策）和倾向性结论；**严禁**回「你指的是哪两个」「你是什么专业」这类把已知信息再问一遍的话。
3. 只有历史里确实找不到该信息时才追问，且一次最多问一项，问完就该给结论。
"""

IV_RULES = """

## 作答识别与重练纪律〔v14 多轮纪律〕（优先级最高，高于本提示词里其它一切条目）

1. **陈述自己的做法就是作答**：用户用第一人称描述流程、参数、项目细节（如「精馏塔设计我按分离要求先定回流比……」）时，一律按「作答」处理并推进进度；**严禁**回「这个不在我的资料范围内」「换个问题」「我没法回答」这类话，也严禁因此掉出面试。
2. **重练第 N 题 = 逐字重出原题**：先从会话历史里找回第 N 题的题干原文，原样重出（题号、题型、题干、作答要求都保留），再说「请重答一次」；**不许**换角度、不许重新生成新题、不许说「咱们换个角度再压一遍」。
3. **继续面试必须回到面试话术**：用户说「继续」「继续面试」「下一题」「接着来」时，一律当作「出下一题」处理，输出必须带第 N 题题型标记与面试进度行；不许回闲聊话术，不许丢进度行。
"""

RULES = {
    "1791552000011": JOB_RULES,   # 岗位匹配
    "1791552000021": IV_RULES,    # 模拟面试官
}


def tok():
    t = os.environ.get("CONSOLE_TOKEN", "").strip()
    if not t:
        raise SystemExit("需要 CONSOLE_TOKEN")
    return t


def api(path, method="GET", body=None):
    t = tok()
    h = {"Authorization": "Bearer " + t, "OperToken": t}
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        h["Content-Type"] = "application/json"
    req = urllib.request.Request(BASE + path, data=data, headers=h, method=method)
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=180) as r:
            raw = r.read().decode("utf-8")
            return r.status, (json.loads(raw) if raw.strip() else None)
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        try:
            return e.code, json.loads(raw)
        except Exception:
            return e.code, raw[:300]


def patch_prompts(graph):
    report = []
    nodes = {n["id"]: n for n in graph["nodes"]}
    for nid, block in RULES.items():
        n = nodes.get(nid)
        if not n:
            raise SystemExit("找不到节点 %s" % nid)
        pt = n["data"].get("prompt_template") or []
        sys_msg = next((p for p in pt if p.get("role") == "system"), None)
        if sys_msg is None:
            raise SystemExit("节点 %s 没有 system 提示词" % nid)
        if MARK in sys_msg.get("text", ""):
            report.append("%s 已含 v14 纪律块，跳过" % n["data"].get("title"))
            continue
        before = len(sys_msg["text"])
        sys_msg["text"] = sys_msg["text"].rstrip() + block
        report.append("%s system 提示词 %d -> %d 字" % (
            n["data"].get("title"), before, len(sys_msg["text"])))
    return report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--src", default=SRC)
    ap.add_argument("--name", default="职引 · 校园就业智能体 v14")
    a = ap.parse_args()
    if not a.apply:
        print(__doc__)
        return 0

    print("== 1. 拉草稿源 %s ==" % a.src)
    s, draft = api("/console/api/apps/%s/workflows/draft" % a.src)
    if s != 200:
        raise SystemExit("拉草稿失败 %s" % s)
    print("   nodes=%d edges=%d" % (len(draft["graph"]["nodes"]), len(draft["graph"]["edges"])))

    print("== 2. 追加纪律块 ==")
    for line in patch_prompts(draft["graph"]):
        print("   -", line)

    print("== 3. 保存并发布草稿源 ==")
    body = {"graph": draft["graph"], "viewport": draft.get("viewport"),
            "features": draft.get("features"),
            "environment_variables": draft.get("environment_variables"),
            "conversation_variables": draft.get("conversation_variables")}
    s, _ = api("/console/api/apps/%s/workflows/draft" % a.src, "POST", body)
    print("   save ->", s)
    if s != 200:
        raise SystemExit("保存失败")
    s, _ = api("/console/api/apps/%s/workflows/publish" % a.src, "POST",
               {"marked_name": "", "marked_comment": "v14 多轮纪律"})
    print("   publish ->", s)
    if s != 200:
        raise SystemExit("发布失败")

    print("== 4. 复制成新对外应用（站点绑复制瞬间的草稿快照）==")
    s, j = api("/console/api/apps/%s/copy" % a.src, "POST",
               {"name": a.name, "icon_type": None, "icon": None,
                "icon_background": None, "mode": "advanced-chat"})
    if s not in (200, 201):
        raise SystemExit("copy 失败 %s %s" % (s, j))
    app = j["id"]
    code = (j.get("site") or {}).get("code")
    print("   NEW_APP =", app, "| SITE =", code)

    s, _ = api("/console/api/apps/%s" % app, "PUT", {
        "name": "职引 · 校园就业智能体",
        "description": "校园就业智能体：简历诊断 / 岗位匹配 / 模拟面试 / 政策咨询 · 重庆理工大学",
        "icon_type": "image", "icon": ICON, "icon_background": "",
        "use_icon_as_answer_icon": True})
    print("   改名+图标 ->", s)
    s, _ = api("/console/api/apps/%s/workflows/publish" % app, "POST",
               {"marked_name": "", "marked_comment": "v14 对外发布"})
    print("   publish ->", s)
    s, _ = api("/console/api/apps/%s/site-enable" % app, "POST", {"enable_site": True})
    print("   site-enable ->", s)

    print("== 5. 等站点可用 ==")
    for i in range(12):
        time.sleep(8)
        try:
            req = urllib.request.Request(BASE + "/api/passport", headers={"X-App-Code": code})
            with urllib.request.urlopen(req, context=CTX, timeout=20) as r:
                if r.status == 200:
                    print("   就绪")
                    break
        except Exception as e:
            print("   第 %d 次探测：%s" % (i + 1, e))

    print()
    print("NEW_APP =", app)
    print("SITE    =", code)
    print("URL     = https://aiagent.cqut.edu.cn:31134/chat/%s" % code)
    with open(os.path.join(HERE, "v14-result.json"), "w", encoding="utf-8") as f:
        json.dump({"app": app, "site": code}, f, ensure_ascii=False, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
