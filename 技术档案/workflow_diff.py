# -*- coding: utf-8 -*-
"""线上草稿漂移检测 / 快照（workflow_diff.py）

为什么要有这个东西：
    站点跑的是「发布那一刻的草稿快照」，而 25 个节点的提示词是在平台控制台里手改的。
    控制台没有任何版本历史，改坏了只能靠记忆回滚——项目里唯一一份全量备份
    graph_backup_20261010.json 停在 10/10，早于 v19。
    所以：拿仓库里那份干净的 srcdraft.json（v19 真源）当基准，随时和线上比。

用法：
    python workflow_diff.py                # 线上草稿 vs srcdraft.json，有漂移退出 1
    python workflow_diff.py --dump         # 抓快照并比对（先存后比）
    python workflow_diff.py --dump-only --to snapshots/v19-draft.json   # 只建档，不比对
    python workflow_diff.py --list         # 列出历史快照
    python workflow_diff.py --ref 某快照.json   # 换基准
    python workflow_diff.py --ref snapshots/v19-draft.json --restore --yes
                                           # 把某快照写回线上草稿（灾难恢复）

输出契约（可被 grep）：
    ---WORKFLOW_DIFF---
    REF: srcdraft.json
    LIVE: <app_id 前 8 位>
    NODES: 29/29
    EDGES: 32/32
    DRIFT: no
    ---END---

退出码：0 = 一致；1 = 有漂移（新增/删除节点、提示词或配置变了）；2 = 取不到线上草稿。
"""
import hashlib
import json
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP_DIR = os.path.join(HERE, "snapshots")
LEGACY_REF = os.path.join(HERE, "srcdraft.json")   # 早期 29 节点的旧草稿，仅作兜底


def default_ref():
    """基准优先级：环境变量 DRAFT_REF > snapshots/ 里最新的 v*-draft.json > 旧 srcdraft.json。

    这样换版本时只要 dump 一份 v20-draft.json，检测就自动改用新基准，不用改代码。
    """
    env = os.environ.get("DRAFT_REF", "").strip()
    if env:
        return env if os.path.isabs(env) else os.path.join(HERE, env)
    if os.path.isdir(SNAP_DIR):
        cands = []
        for name in os.listdir(SNAP_DIR):
            m = re.match(r"v(\d+)-draft\.json$", name)
            if m:
                cands.append((int(m.group(1)), os.path.join(SNAP_DIR, name)))
        if cands:
            return max(cands)[1]
    return LEGACY_REF

sys.path.insert(0, HERE)
from release import api, load_token  # noqa: E402


def read_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def app_of(ref_path, override=None):
    if override:
        return override
    d = read_json(ref_path)
    return d.get("app_id") or d.get("id") or ""


def node_text(node):
    """把一个节点的可比较内容压成文本：标题 + 全部提示词 + 关键配置。

    只比 id 会漏掉"节点在、提示词被改了"这种最要命的漂移。
    """
    data = node.get("data") or {}
    bits = [str(data.get("title") or ""), str(data.get("type") or ""),
            str(data.get("desc") or "")]
    for item in data.get("prompt_template") or []:
        bits.append("%s:%s" % (item.get("role"), item.get("text")))
    for key in ("model", "variables", "prompt_config", "context", "iteration",
                "cases", "conditions"):
        v = data.get(key)
        if v not in (None, "", [], {}):
            bits.append("%s=%s" % (key, json.dumps(v, ensure_ascii=False, sort_keys=True)))
    return "\n".join(bits)


def digest(text):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:12]


def profile(draft):
    """草稿 -> {node_id: (title, digest, len)}。"""
    graph = (draft or {}).get("graph") or {}
    out = {}
    for node in graph.get("nodes") or []:
        nid = node.get("id")
        data = node.get("data") or {}
        text = node_text(node)
        out[nid] = (str(data.get("title") or data.get("type") or nid),
                    digest(text), len(text))
    return out, graph.get("edges") or []


def edge_set(edges):
    s = set()
    for e in edges:
        s.add((e.get("source"), e.get("target"),
               e.get("sourceHandle") or e.get("source_handle") or ""))
    return s


def diff(ref, live):
    rn, re_ = profile(ref)
    ln, le = profile(live)
    added = sorted(set(ln) - set(rn))
    removed = sorted(set(rn) - set(ln))
    changed = []
    for nid in sorted(set(rn) & set(ln)):
        if rn[nid][1] != ln[nid][1]:
            changed.append((nid, rn[nid], ln[nid]))
    e_add = sorted(edge_set(le) - edge_set(re_))
    e_del = sorted(edge_set(re_) - edge_set(le))
    return dict(ref_nodes=len(rn), live_nodes=len(ln),
                ref_edges=len(re_), live_edges=len(le),
                added=added, removed=removed, changed=changed,
                e_add=e_add, e_del=e_del)


def fetch_draft(app_id):
    tok = load_token()
    if not tok:
        print("取不到控制台 token（跑 python tok.py 看取法）")
        return None
    status, obj = api("/console/api/apps/%s/workflows/draft" % app_id, "GET", None, tok)
    if status != 200 or not isinstance(obj, dict) or "graph" not in obj:
        print("取线上草稿失败：HTTP %s %s" % (status, str(obj)[:200]))
        return None
    return obj


def dump(draft, app_id, target):
    os.makedirs(os.path.dirname(target) or ".", exist_ok=True)
    with open(target, "w", encoding="utf-8") as f:
        json.dump(draft, f, ensure_ascii=False, indent=1)
    n = len((draft.get("graph") or {}).get("nodes") or [])
    print("快照已存：%s（%d 节点，%.1f KB）"
          % (os.path.relpath(target, HERE), n, os.path.getsize(target) / 1024.0))
    return target


def restore(draft_src, app_id, yes):
    """把快照里的图写回线上草稿。

    只动草稿，不动已发布站点——所以恢复完必须重新发布、再复制站点，
    公开地址才会变（站点绑快照，这一步绕不过去）。
    """
    if not yes:
        print("拒绝执行：这是覆盖线上草稿的写操作。确认要恢复就加 --yes。")
        print("要恢复到哪个版本：--ref snapshots/v19-draft.json --restore --yes")
        return 1
    tok = load_token()
    if not tok:
        print("取不到控制台 token")
        return 2
    status, live = api("/console/api/apps/%s/workflows/draft" % app_id, "GET", None, tok)
    if status != 200 or not isinstance(live, dict):
        print("取线上草稿失败：HTTP %s" % status)
        return 2
    src = read_json(draft_src)
    if "graph" not in src:
        print("快照里没有 graph，不敢写：%s" % draft_src)
        return 2
    src_nodes = len((src.get("graph") or {}).get("nodes") or [])
    live_nodes = len((live.get("graph") or {}).get("nodes") or [])
    print("线上 %d 节点 -> 快照 %d 节点（快照：%s）"
          % (live_nodes, src_nodes, os.path.basename(draft_src)))
    body = {"graph": src["graph"],
            "features": src.get("features") or live.get("features"),
            "environment_variables": src.get("environment_variables") or live.get("environment_variables") or {},
            "conversation_variables": src.get("conversation_variables") or live.get("conversation_variables") or [],
            "hash": live.get("hash")}
    status, obj = api("/console/api/apps/%s/workflows/draft" % app_id, "POST", body, tok, timeout=240)
    print("POST draft -> HTTP %s" % status)
    if status != 200:
        print("写回失败：%s" % str(obj)[:300])
        return 2
    print("草稿已恢复。**下一步必须做**：发布工作流 -> 重新复制站点 -> 改 readysite.txt"
          " -> 重出二维码 -> 同步提交表地址，否则线上还是旧快照。")
    return 0


def list_snaps():
    if not os.path.isdir(SNAP_DIR):
        print("还没有快照目录：%s" % SNAP_DIR)
        return 0
    files = sorted(f for f in os.listdir(SNAP_DIR) if f.endswith(".json"))
    if not files:
        print("快照目录是空的")
        return 0
    for name in files:
        path = os.path.join(SNAP_DIR, name)
        try:
            d = read_json(path)
            n = len((d.get("graph") or {}).get("nodes") or [])
        except ValueError:
            n = -1
        print("%-36s %5d 节点  %7.1f KB" % (name, n, os.path.getsize(path) / 1024.0))
    return 0


def main():
    args = sys.argv[1:]
    if "--list" in args:
        return list_snaps()

    ref_path = default_ref()
    if "--ref" in args:
        ref_path = args[args.index("--ref") + 1]
        if not os.path.isabs(ref_path):
            ref_path = os.path.join(HERE, ref_path)
    app_override = args[args.index("--app") + 1] if "--app" in args else None
    if app_override:
        app_id = app_override
    elif os.path.exists(ref_path):
        app_id = app_of(ref_path)
    else:
        sys.exit("基准文件不存在：%s（首次建档请用 --app 指定应用 ID 并 --dump）" % ref_path)
    if not app_id:
        sys.exit("基准文件里没有 app_id，用 --app 指定")

    if "--restore" in args:
        if not os.path.exists(ref_path):
            sys.exit("要恢复的快照不存在：%s" % ref_path)
        return restore(ref_path, app_id, "--yes" in args)

    live = fetch_draft(app_id)
    if live is None:
        return 2

    if "--dump" in args or "--dump-only" in args:
        target = (args[args.index("--to") + 1] if "--to" in args
                  else os.path.join(SNAP_DIR, "live-%s.json" % time.strftime("%Y%m%d-%H%M")))
        if not os.path.isabs(target):
            target = os.path.join(HERE, target)
        dump(live, app_id, target)
        if "--dump-only" in args:
            return 0

    if not os.path.exists(ref_path):
        sys.exit("基准文件不存在：%s（已单独抓快照，再跑一次做比对）" % ref_path)
    ref = read_json(ref_path)
    d = diff(ref, live)

    drift = bool(d["added"] or d["removed"] or d["changed"] or d["e_add"] or d["e_del"])
    print("基准：%s" % os.path.relpath(ref_path, HERE))
    print("线上：app %s…" % app_id[:8])
    print("节点 %d -> %d　连线 %d -> %d"
          % (d["ref_nodes"], d["live_nodes"], d["ref_edges"], d["live_edges"]))
    if d["added"]:
        print("\n新增节点 %d 个（线上有、基准没有）：" % len(d["added"]))
        for nid in d["added"]:
            print("  + %s" % nid)
    if d["removed"]:
        print("\n丢失节点 %d 个（基准有、线上没有）：" % len(d["removed"]))
        for nid in d["removed"]:
            print("  - %s" % nid)
    if d["changed"]:
        print("\n内容被改的节点 %d 个：" % len(d["changed"]))
        for nid, before, after in d["changed"]:
            print("  ~ %-28s %s  %s→%s 字" % (before[0][:28], nid[:12], before[2], after[2]))
    if d["e_add"] or d["e_del"]:
        print("\n连线变化：新增 %d 条，减少 %d 条" % (len(d["e_add"]), len(d["e_del"])))
        for e in d["e_add"][:8]:
            print("  + %s -> %s" % (e[0], e[1]))
        for e in d["e_del"][:8]:
            print("  - %s -> %s" % (e[0], e[1]))
    if not drift:
        print("\n线上草稿与基准完全一致，没有人在控制台手改过。")

    print("\n---WORKFLOW_DIFF---")
    print("REF: %s" % os.path.basename(ref_path))
    print("LIVE: %s" % app_id[:8])
    print("NODES: %d/%d" % (d["live_nodes"], d["ref_nodes"]))
    print("EDGES: %d/%d" % (d["live_edges"], d["ref_edges"]))
    print("DRIFT: %s" % ("yes" if drift else "no"))
    print("---END---")
    return 1 if drift else 0


if __name__ == "__main__":
    sys.exit(main())
