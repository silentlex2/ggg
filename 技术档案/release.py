# -*- coding: utf-8 -*-
"""职引 · 换站发布流水线（release.py）

把 clone_v12.py 的 8 步手工换站（复制→改草稿→发布→轮询→开站→改真源→重出二维码→跑回归）
收敛成一条命令，并且带 --dry-run：先在纸面上把整套动作看一遍再决定要不要动线上。

用法：
    python release.py --from <源应用ID> --name "职引 · 校园就业智能体 v13" --dry-run
    python release.py --from <源应用ID> --name "职引 · 校园就业智能体 v13" --graph patch.json
    python release.py --from <源应用ID> --name "..." --graph patch.json --retire-old <旧应用ID>

    --dry-run          只打印计划，不发任何写请求（默认连读请求也不发，见 --check-src）
    --check-src        dry-run 时额外 GET 源应用做存在性校验（需要 token）
    --graph PATCH      补丁 JSON；不给则把源应用原样复制发布（纯换站，不改进任何节点）
    --icon HASH        新应用头像（默认沿用 v12 的 image 哈希）
    --comment TEXT     发布备注（默认 = 应用名）
    --retire-old APP   收尾时把旧应用改名标注「回退」，默认不动（保留回退路径）
    --skip-qr          不重出二维码
    --skip-regression  不跑 run_all.py
    --refresh-brand    额外跑 参赛方案/素材/make-png.py（LOGO / 背景，与站点码无关，较慢）
    --wait-site SEC    等 live workflow 生效的上限（默认 180）
    --interval SEC     轮询间隔（默认 10）

补丁 JSON 结构（只写要动的那几项，其余省略）：
    {
      "delete_nodes":          ["1791600000015"],
      "set_completion_params": {"1791550106443": {"temperature": 0.3, "max_tokens": 2000}},
      "rewire":                [{"from": "1791544053269", "to": "1791552000001", "handle": "false"}],
      "set_variables":         {"1791542455112": ["..."]},
      "set_node_fields":       {"1791544053269": {"instructions": "..."}},
      "set_app_fields":        {"description": "..."}
    }

    · set_completion_params 落在 node.data.model.completion_params（合并，不清空原有键）。
      注意：这就是「长答案偶发截断」的修法——六个 LLM 节点补 max_tokens。
    · rewire 默认语义 mode="downstream"：把所有 source==from 的边的 target 改成 to；
      给 "mode": "incoming" 则改「所有 target==from 的边」；给 "handle" 只改该 sourceHandle 的边。
    · set_variables：值是 list 就整段替换 node.data.variables；值是 dict 就按键合并。
    · set_node_fields：支持点号路径，如 "memory.window.size"。
    · set_app_fields：写在草稿顶层（description / conversation_variables / environment_variables）。

失败即停：任何一步非 2xx 都会打印「停在第 N 步」+ 回滚方式，退出码 1。
删除节点后若还有变量选择器引用它，只告警不拦截（平台容忍悬空引用，运行时取空）。

退出码：0 = 全部完成（或 dry-run 正常结束）；1 = 有步骤失败 / 回归未过；2 = 参数或凭据问题。
"""
import argparse
import json
import os
import ssl
import subprocess
import sys
import time
import urllib.error
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
if HERE not in sys.path:
    sys.path.insert(0, HERE)

BASE = "https://aiagent.cqut.edu.cn:31134"
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

READY = os.path.join(HERE, "readysite.txt")
ASSET_DIR = os.path.join(ROOT, "参赛方案", "素材")
QR_PATH = os.path.join(ASSET_DIR, "职引-二维码-公开站点.png")
BRAND_SCRIPT = os.path.join(ASSET_DIR, "make-png.py")
QR_SCRIPT = os.path.join(HERE, "make_qr.py")
RUN_ALL = os.path.join(HERE, "run_all.py")
DEFAULT_ICON = "ff8cb252-6223-4c43-9eb7-22844fd9adfa"
DEFAULT_DESC = "校园就业智能体：简历诊断 / 岗位匹配 / 模拟面试 / 政策咨询 · 重庆理工大学"
TOTAL = 9

PATCH_KEYS = ("delete_nodes", "set_completion_params", "rewire", "set_variables",
              "set_node_fields", "set_app_fields")


# ---------------------------------------------------------------- 基础工具
def head(n, title):
    print()
    print("=" * 72)
    print("[%d/%d] %s" % (n, TOTAL, title))
    print("=" * 72)


def read_site(path=READY):
    """读站点码唯一真源。"""
    try:
        with open(path, encoding="utf-8") as f:
            return f.read().strip()
    except OSError:
        return ""


def write_site(code, path=READY):
    """写站点码唯一真源（单行）。"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(code)
    return path


def token_available():
    """不抛异常地问一句 token 在不在——dry-run 用。"""
    if os.environ.get("CONSOLE_TOKEN", "").strip():
        return True
    for rel in (".token", os.path.join("scratch", ".token")):
        if os.path.exists(os.path.join(HERE, rel)):
            return True
    return False


def load_token():
    """取控制台 token；没有就返回 None 并把 tok.py 的取法提示原样打出来。"""
    from tok import token as _token
    try:
        return _token()
    except SystemExit as e:
        print(str(e))
        return None


def api(path, method="GET", body=None, token=None, timeout=180):
    """调控制台接口 -> (status, payload)。payload 能解析成 JSON 就是对象，否则是文本。"""
    data = json.dumps(body).encode() if body is not None else None
    headers = {"Authorization": "Bearer " + (token or ""), "OperToken": token or ""}
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(BASE + path, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", "replace")
            status = resp.status
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        status = e.code
    except Exception as e:                                   # 网络层
        return -1, {"error": repr(e)}
    try:
        return status, (json.loads(raw) if raw.strip() else None)
    except ValueError:
        return status, raw


def pick(obj, *names, **kw):
    """从响应里按顺序取第一个非空字段（支持 a.b 路径）。"""
    default = kw.get("default", "")
    if not isinstance(obj, dict):
        return default
    for name in names:
        cur = obj
        for part in name.split("."):
            cur = cur.get(part) if isinstance(cur, dict) else None
            if cur is None:
                break
        if cur not in (None, "", [], {}):
            return cur
    return default


def brief(obj, limit=220):
    """响应摘要，用于每步打印「关键字段」。"""
    if isinstance(obj, dict):
        keys = ("id", "name", "status", "result", "code", "message", "workflow", "site",
                "access_token", "enable_site", "workflow_id", "version", "hash", "error")
        slim = {k: obj[k] for k in keys if k in obj}
        return json.dumps(slim, ensure_ascii=False)[:limit]
    return str(obj)[:limit]


def abort(stage, msg, ctx):
    """任一步失败：说清停在哪、已经发生了什么、怎么退回去。"""
    print()
    print("!" * 72)
    print("FAILED at step %d/%d — %s" % (stage, TOTAL, msg))
    print("!" * 72)
    print("已发生的写操作：")
    print("  · 新应用      %s" % (ctx.get("new_app") or "（未创建）"))
    print("  · 新草稿写入  %s" % ("是" if ctx.get("draft_saved") else "否"))
    print("  · 已发布      %s" % ("是" if ctx.get("published") else "否"))
    print("  · readysite   %s" % ("已改写为 %s" % ctx["site"] if ctx.get("site_written")
                                  else "未改（仍是 %s）" % ctx.get("old_site", "?")))
    print("  · 二维码      %s" % ("已重出" if ctx.get("qr_done") else "未动"))
    print()
    print("回滚方式：")
    if not ctx.get("site_written"):
        print("  1. 线上公开地址没变，旧站仍是当前站——什么都不用做，直接丢掉新应用即可。")
        if ctx.get("new_app"):
            print("  2. 想清理：控制台删掉应用 %s（它没开站点，没人能访问）。" % ctx["new_app"])
    else:
        print("  1. 把 %s 写回旧站点码 %s（release.py 未关停旧站，旧地址仍然 live）。"
              % (READY, ctx.get("old_site", "?")))
        print("  2. 二维码：素材目录里有 *.oldN.png.bak 备份，覆盖回去。")
        print("  3. 若已发材料：以 readysite.txt 为准，重新生成二维码 + 重出提交表。")
    print("  4. 旧应用：release.py 默认不改名不关停，回退路径一直在。")
    return 1


# ---------------------------------------------------------------- 补丁
def load_patch(path):
    """读补丁 JSON -> dict。"""
    with open(path, encoding="utf-8") as f:
        patch = json.load(f)
    if not isinstance(patch, dict):
        raise ValueError("补丁顶层必须是 JSON 对象")
    return patch


def validate_patch(patch):
    """静态校验补丁结构，返回 (errors, warnings)。"""
    errors, warns = [], []
    for key in patch:
        if key not in PATCH_KEYS:
            warns.append("未知操作键 %r 会被忽略（支持：%s）" % (key, ", ".join(PATCH_KEYS)))
    dn = patch.get("delete_nodes") or []
    if not isinstance(dn, list) or any(not isinstance(x, str) for x in dn):
        errors.append("delete_nodes 必须是字符串数组")
    scp = patch.get("set_completion_params") or {}
    if not isinstance(scp, dict) or any(not isinstance(v, dict) for v in scp.values()):
        errors.append("set_completion_params 必须是 {节点id: {参数: 值}}")
    for i, item in enumerate(patch.get("rewire") or []):
        if not isinstance(item, dict) or "from" not in item or "to" not in item:
            errors.append("rewire[%d] 必须含 from / to" % i)
        elif item.get("mode", "downstream") not in ("downstream", "incoming"):
            errors.append("rewire[%d].mode 只能是 downstream / incoming" % i)
    for key in ("set_variables", "set_node_fields", "set_app_fields"):
        if key in patch and not isinstance(patch[key], dict):
            errors.append("%s 必须是对象" % key)
    return errors, warns


def describe_patch(patch):
    """dry-run 用：把补丁翻成人话（没取图，节点只有 id）。"""
    lines = []
    dn = patch.get("delete_nodes") or []
    if dn:
        lines.append("delete_nodes           删 %d 个节点：%s" % (len(dn), ", ".join(dn)))
    scp = patch.get("set_completion_params") or {}
    if scp:
        detail = "；".join("%s←%s" % (k, "/".join(sorted(v))) for k, v in scp.items())
        lines.append("set_completion_params  %d 个节点补参数：%s" % (len(scp), detail))
    rw = patch.get("rewire") or []
    if rw:
        detail = "；".join("%s → %s%s" % (i["from"], i["to"],
                                          "(handle %s)" % i["handle"] if i.get("handle") else "")
                           for i in rw)
        lines.append("rewire                 %d 条连线：%s" % (len(rw), detail))
    sv = patch.get("set_variables") or {}
    if sv:
        lines.append("set_variables          %d 个节点：%s" % (
            len(sv), "；".join("%s(%s)" % (k, "整段替换" if isinstance(v, list) else "按键合并")
                              for k, v in sv.items())))
    snf = patch.get("set_node_fields") or {}
    if snf:
        lines.append("set_node_fields        %d 个节点：%s" % (
            len(snf), "；".join("%s←%s" % (k, ",".join(v)) for k, v in snf.items())))
    saf = patch.get("set_app_fields") or {}
    if saf:
        lines.append("set_app_fields         草稿顶层：%s" % ", ".join(saf))
    return lines


def _set_path(obj, dotted, value):
    """按点号路径写值：a.b.c <- value。"""
    parts = dotted.split(".")
    for part in parts[:-1]:
        obj = obj.setdefault(part, {})
    obj[parts[-1]] = value


def apply_patch(draft, patch):
    """在草稿副本上执行补丁 -> (draft, log_lines)。纯函数，不发请求。"""
    graph = draft.setdefault("graph", {})
    nodes = graph.setdefault("nodes", [])
    edges = graph.setdefault("edges", [])
    idx = {n.get("id"): n for n in nodes}
    log = []

    for nid in patch.get("delete_nodes") or []:
        node = idx.pop(nid, None)
        if node is None:
            log.append("  ! 删除 %s：节点不存在，跳过" % nid)
            continue
        nodes.remove(node)
        keep = [e for e in edges if e.get("source") != nid and e.get("target") != nid]
        log.append("  - 删除节点 %s（%s），连带删 %d 条边"
                   % (nid, (node.get("data") or {}).get("title", "?"), len(edges) - len(keep)))
        edges[:] = keep

    for nid, params in (patch.get("set_completion_params") or {}).items():
        node = idx.get(nid)
        if node is None:
            log.append("  ! set_completion_params %s：节点不存在，跳过" % nid)
            continue
        data = node.setdefault("data", {})
        model = data.setdefault("model", {})
        cur = model.setdefault("completion_params", {})
        before = dict(cur)
        cur.update(params)
        log.append("  ~ %s（%s）completion_params %s -> %s"
                   % (nid, data.get("title", "?"), before, cur))

    for item in patch.get("rewire") or []:
        src, dst = item["from"], item["to"]
        mode = item.get("mode", "downstream")
        handle = item.get("handle") or item.get("sourceHandle")
        changed = 0
        for edge in edges:
            if mode == "incoming":
                if edge.get("target") == src:
                    edge["target"] = dst
                    changed += 1
            elif edge.get("source") == src and (handle is None or edge.get("sourceHandle") == handle):
                edge["target"] = dst
                changed += 1
        log.append("  ~ rewire %s -> %s（%s%s）改了 %d 条边"
                   % (src, dst, mode, "，handle=" + str(handle) if handle else "", changed))
        if not changed:
            log.append("  ! rewire 没匹配到任何边，检查 from / handle 是否写对")
        if dst not in idx:
            log.append("  ! rewire 目标 %s 不在图里（会变成悬空边）" % dst)

    for nid, value in (patch.get("set_variables") or {}).items():
        node = idx.get(nid)
        if node is None:
            log.append("  ! set_variables %s：节点不存在，跳过" % nid)
            continue
        data = node.setdefault("data", {})
        old = data.get("variables")
        if isinstance(value, list):
            data["variables"] = value
            log.append("  ~ %s variables 整段替换（%d 项）" % (nid, len(value)))
        elif isinstance(old, list):
            names = []
            for item in old:
                name = item.get("variable") or item.get("label")
                if name in value:
                    patch_val = value[name]
                    item.update(patch_val if isinstance(patch_val, dict) else {"value": patch_val})
                    names.append(str(name))
            log.append("  ~ %s variables 按名合并：%s" % (nid, ", ".join(names) or "（无匹配）"))
        else:
            merged = dict(old or {}) if isinstance(old, dict) else {}
            merged.update(value)
            data["variables"] = merged
            log.append("  ~ %s variables 合并键：%s" % (nid, ", ".join(value)))

    for nid, fields in (patch.get("set_node_fields") or {}).items():
        node = idx.get(nid)
        if node is None:
            log.append("  ! set_node_fields %s：节点不存在，跳过" % nid)
            continue
        data = node.setdefault("data", {})
        for dotted, value in fields.items():
            _set_path(data, dotted, value)
        log.append("  ~ %s 字段改写：%s" % (nid, ", ".join(fields)))

    for key, value in (patch.get("set_app_fields") or {}).items():
        draft[key] = value
        log.append("  ~ 草稿顶层 %s 改写" % key)

    return draft, log


def validate_graph(draft):
    """补丁后的图完整性：边不能指向不存在的节点。"""
    problems = []
    ids = {n.get("id") for n in draft.get("graph", {}).get("nodes", [])}
    for edge in draft.get("graph", {}).get("edges", []):
        if edge.get("source") not in ids or edge.get("target") not in ids:
            problems.append("边 %s 悬空：%s -> %s"
                            % (edge.get("id"), edge.get("source"), edge.get("target")))
    return problems


def dangling_refs(draft, removed_ids):
    """被删掉但仍被变量选择器引用的节点（只告警）。"""
    blob = json.dumps(draft.get("graph", {}), ensure_ascii=False)
    return [nid for nid in removed_ids if nid in blob]


# ---------------------------------------------------------------- 各步骤
def step_copy(tok, src, name, icon, ctx):
    head(2, "复制源应用 -> 新应用")
    # 在任何写操作之前先记下旧站此刻在跑的 workflow_id：这是「新站是否真的切过去」的基准。
    ctx["old_live"] = live_workflow(ctx.get("old_site", ""))
    print("  旧站 live workflow_id = %s（切换基准）" % (ctx["old_live"] or "（取不到，改用「非空」判据）"))
    status, obj = api("/console/api/apps/%s/copy" % src, "POST",
                      {"name": name, "icon_type": None, "icon": None,
                       "icon_background": None, "mode": "advanced-chat"}, tok)
    print("  POST /console/api/apps/%s/copy -> HTTP %s" % (src[:8], status))
    print("  %s" % brief(obj))
    new_id = pick(obj, "id")
    if status not in (200, 201) or not new_id:
        abort(2, "复制失败（HTTP %s）" % status, ctx)
        return ""
    ctx["new_app"] = new_id
    print("  新应用 ID = %s" % new_id)

    status, obj = api("/console/api/apps/%s" % new_id, "PUT",
                      {"name": name, "description": DEFAULT_DESC,
                       "icon_type": "image", "icon": icon, "icon_background": ""}, tok)
    print("  PUT 改名/描述/图标 -> HTTP %s  name=%s" % (status, pick(obj, "name", default="?")))
    return new_id


def step_draft(tok, src, new_id, patch, ctx):
    head(3, "取草稿 -> 应用补丁 -> 保存草稿")
    status, src_draft = api("/console/api/apps/%s/workflows/draft" % src, "GET", None, tok)
    if status == 200 and isinstance(src_draft, dict):
        print("  源草稿：%d 节点 / %d 边"
              % (len(src_draft.get("graph", {}).get("nodes", [])),
                 len(src_draft.get("graph", {}).get("edges", []))))
    else:
        print("  源草稿读取失败（HTTP %s），不影响后续（补丁打在新草稿上）" % status)

    status, draft = api("/console/api/apps/%s/workflows/draft" % new_id, "GET", None, tok)
    if status != 200 or not isinstance(draft, dict) or "graph" not in draft:
        abort(3, "取新草稿失败（HTTP %s）" % status, ctx)
        return False
    print("  新草稿：%d 节点 / %d 边"
          % (len(draft["graph"].get("nodes", [])), len(draft["graph"].get("edges", []))))
    h_before = draft.get("hash", "")

    removed = []
    if patch:
        print("  应用补丁：")
        draft, log = apply_patch(draft, patch)
        for line in log:
            print(line)
        removed = list(patch.get("delete_nodes") or [])
        print("  补丁后：%d 节点 / %d 边"
              % (len(draft["graph"].get("nodes", [])), len(draft["graph"].get("edges", []))))
        problems = validate_graph(draft)
        for p in problems:
            print("  ! 图完整性：%s" % p)
        if problems:
            abort(3, "补丁把图改坏了（%d 条悬空边）" % len(problems), ctx)
            return False
        dangling = dangling_refs(draft, removed)
        if dangling:
            print("  ! 告警：这些被删节点仍被引用（平台容忍，运行时取空）：%s" % ", ".join(dangling))
    else:
        print("  未提供 --graph：原样保存（等于纯换站，不改进任何节点）")

    body = {"graph": draft["graph"],
            "features": draft.get("features"),
            "environment_variables": draft.get("environment_variables") or {},
            "conversation_variables": draft.get("conversation_variables") or [],
            "hash": draft.get("hash")}
    status, obj = api("/console/api/apps/%s/workflows/draft" % new_id, "POST", body, tok, timeout=240)
    print("  POST draft -> HTTP %s  %s" % (status, brief(obj)))
    if status != 200:
        abort(3, "保存草稿失败（HTTP %s）" % status, ctx)
        return False
    ctx["draft_saved"] = True
    print("  hash %s -> %s" % (str(h_before)[:8], str(pick(obj, "hash", default=draft.get("hash")))[:8]))
    return True


def step_publish(tok, new_id, comment, ctx):
    head(4, "发布工作流")
    status, obj = api("/console/api/apps/%s/workflows/publish" % new_id, "POST",
                      {"marked_name": "", "marked_comment": comment}, tok, timeout=240)
    print("  POST publish -> HTTP %s  %s" % (status, brief(obj)))
    if status != 200:
        abort(4, "发布失败（HTTP %s）" % status, ctx)
        return False
    ctx["published"] = True
    return True


def live_workflow(site):
    """问一次公开站点：当前实际在跑的 workflow_id（照 poll.py 的做法）。"""
    if not site:
        return ""
    access = ""
    for _ in range(3):
        try:
            req = urllib.request.Request(BASE + "/api/passport", headers={"X-App-Code": site})
            with urllib.request.urlopen(req, context=CTX, timeout=30) as r:
                access = json.loads(r.read().decode()).get("access_token", "")
        except Exception:
            access = ""
        if access:
            break
        time.sleep(2)
    if not access:
        return ""
    body = json.dumps({"response_mode": "streaming", "conversation_id": "",
                       "query": "你好", "inputs": {"user_input": "你好"},
                       "parent_message_id": None}).encode()
    req = urllib.request.Request(BASE + "/api/chat-messages", data=body, method="POST",
                                 headers={"Content-Type": "application/json",
                                          "X-App-Code": site,
                                          "authorization": "Bearer " + access,
                                          "auth-token": "Bearer " + access})
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=240) as r:
            raw = r.read().decode("utf-8", "replace")
    except Exception:
        return ""
    for blk in raw.replace("\r\n", "\n").split("\n\n"):
        if not blk.startswith("data:"):
            continue
        try:
            event = json.loads(blk[5:].strip())
        except ValueError:
            continue
        if event.get("event") == "workflow_finished":
            return (event.get("data") or {}).get("workflow_id", "")
    return ""


def step_poll_console(tok, new_id, ctx):
    """GET 应用的 workflow.id / site，并记下旧站此刻的 live workflow_id 作为切换基准。"""
    head(5, "轮询发布态（workflow.id / site）")
    status, app = api("/console/api/apps/%s" % new_id, "GET", None, tok)
    if status != 200:
        abort(5, "取应用信息失败（HTTP %s）" % status, ctx)
        return ""
    want_wf = pick(app, "workflow.id")
    print("  发布后 workflow.id = %s" % (want_wf or "（平台没返回）"))
    print("  enable_site = %s  site = %s"
          % (pick(app, "enable_site", default="?"), pick(app, "site.access_token", default="（未建站）")))
    status, site = api("/console/api/apps/%s/site" % new_id, "GET", None, tok)
    print("  GET /site -> HTTP %s  %s" % (status, brief(site)))
    # 平台的 live workflow_id 是「发布版本 id」，不一定等于应用 workflow.id，
    # 所以判据用「新站 live id 非空且 != 旧站基准」——基准在 step 2 之前就取好了。
    print("  旧站基准 live workflow_id = %s" % (ctx.get("old_live") or "（无，改用「非空」判据）"))
    ctx["want_wf"] = want_wf
    return want_wf


def step_site_enable(tok, new_id, ctx):
    head(6, "打开站点 -> 取站点码 -> 写 readysite.txt")
    status, obj = api("/console/api/apps/%s/site-enable" % new_id, "POST",
                      {"enable_site": True}, tok)
    print("  POST site-enable {enable_site:true} -> HTTP %s  %s" % (status, brief(obj)))
    if status != 200:
        abort(6, "开启站点失败（HTTP %s）" % status, ctx)
        return ""
    code = pick(obj, "access_token", "site.access_token", "code")
    if not code:
        status, app = api("/console/api/apps/%s" % new_id, "GET", None, tok)
        code = pick(app, "site.access_token")
        print("  从 GET app 补取站点码 -> HTTP %s  %s" % (status, code or "（仍为空）"))
    if not code:
        status, site = api("/console/api/apps/%s/site" % new_id, "GET", None, tok)
        code = pick(site, "access_token", "code")
        print("  从 GET /site 补取站点码 -> HTTP %s  %s" % (status, code or "（仍为空）"))
    if not code:
        abort(6, "拿不到站点码：平台没在响应里回 access_token", ctx)
        return ""
    old = ctx.get("old_site", "")
    print("  站点码 = %s（旧 %s）" % (code, old))
    print("  公开地址 = %s/chat/%s" % (BASE, code))
    write_site(code)
    ctx["site"] = code
    ctx["site_written"] = True
    print("  已写入 %s" % READY)
    return code


def poll_live(code, want_wf, old_live, wait_s, interval):
    """开站后确认新站跑的是新发布：live workflow_id 非空、且与旧站不同。"""
    print("  live 校验：X-App-Code=%s，旧站基准=%s" % (code, old_live or "（无）"))
    deadline = time.time() + wait_s
    n = 0
    while time.time() < deadline:
        n += 1
        live = live_workflow(code)
        if live and (not old_live or live != old_live):
            tail = "（与应用 workflow.id 一致）" if want_wf and live == want_wf else ""
            print("    poll%d live workflow_id = %s  != 旧站  OK%s" % (n, live, tail))
            return True
        print("    poll%d live=%s  %s" % (
            n, live or "（空）",
            "还是旧站版本，等" if live == old_live else "站点还没生效，等"))
        time.sleep(interval)
    return False


def step_qr(code, refresh_brand=False):
    """重出二维码并解码回验。

    优先复用 技术档案/make_qr.py（它只认 readysite.txt 一个真源，且自己回验）；
    没有那个脚本时退回本文件内置出图（同参数：M 级纠错 / box 10 / border 4 / #1d4ed8）。
    注意 make-png.py 只渲染 LOGO / 会话背景，不生成二维码——别拿它当二维码生成器。
    """
    head(7, "重出二维码")
    url = "%s/chat/%s" % (BASE, code)
    print("  目标 %s" % url)
    if refresh_brand:
        print("  --refresh-brand：跑 make-png.py（LOGO / 会话背景，约 25 秒）")
        try:
            subprocess.run([sys.executable, BRAND_SCRIPT], cwd=ASSET_DIR, timeout=300)
        except Exception as e:
            print("  ! make-png.py 失败：%s（不影响二维码）" % e)
    else:
        print("  提示：make-png.py 只渲染 LOGO/背景，不生成二维码（已核对源码）；"
              "需要品牌图加 --refresh-brand。")

    if os.path.exists(QR_SCRIPT):
        print("  用 %s 出图（真源 readysite.txt，刚由第 6 步写入）"
              % os.path.relpath(QR_SCRIPT, ROOT))
        env = dict(os.environ, PYTHONIOENCODING="utf-8")
        try:
            proc = subprocess.run([sys.executable, QR_SCRIPT], cwd=HERE, env=env,
                                  capture_output=True, timeout=300)
        except Exception as e:
            print("  ! make_qr.py 起不来：%s" % e)
            return False
        out = decode_console((proc.stdout or b"") + (proc.stderr or b""))
        for line in out.rstrip().splitlines():
            print("    %s" % line)
        if proc.returncode != 0:
            print("  ! make_qr.py 退出码 %s（二维码可能没更新）" % proc.returncode)
            return False
    else:
        try:
            import qrcode
        except ImportError:
            print("  ! 缺 qrcode 库：pip install qrcode pillow")
            return False
        import shutil
        if os.path.exists(QR_PATH):
            n = 1
            while os.path.exists(QR_PATH.replace(".png", ".old%d.png.bak" % n)):
                n += 1
            backup = QR_PATH.replace(".png", ".old%d.png.bak" % n)
            shutil.copy2(QR_PATH, backup)
            print("  旧图备份 -> %s（素材 PNG 若已被 git 跟踪，也可 git 回滚）"
                  % os.path.basename(backup))
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M,
                           box_size=10, border=4)
        qr.add_data(url)
        qr.make(fit=True)
        qr.make_image(fill_color="#1d4ed8", back_color="white").save(QR_PATH)
        print("  写出 %s（%d 字节）" % (QR_PATH, os.path.getsize(QR_PATH)))

    try:
        import check_assets
        data, shape = check_assets.decode_qr(QR_PATH)
        print("  解码复核 %s×%s -> %s  %s"
              % (shape[1] if shape else "?", shape[0] if shape else "?",
                 data or "（解不出）", "OK" if code in data else "MISMATCH"))
        return code in data
    except Exception as e:
        print("  解码复核跳过：%s" % e)
        return True


def decode_console(raw):
    """子进程输出解码：优先 UTF-8，退回 GBK（Windows 控制台默认代码页）。"""
    for enc in ("utf-8", "gbk"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", "replace")


def step_regression(code):
    """跑 run_all.py，打印它的 SCORE 契约块。"""
    head(8, "回归（run_all.py）")
    print("  SITE=%s python 技术档案/run_all.py" % code)
    # 强制子进程用 UTF-8 输出，否则 Windows 上 run_all.py 走 cp936，抓回来是乱码
    env = dict(os.environ, SITE=code, PYTHONIOENCODING="utf-8")
    try:
        proc = subprocess.run([sys.executable, RUN_ALL], cwd=HERE, env=env,
                              capture_output=True, timeout=3600)
    except Exception as e:
        print("  ! run_all.py 起不来：%s" % e)
        return 1
    out = decode_console((proc.stdout or b"") + (proc.stderr or b""))
    print(out.rstrip())
    block, keep = [], False
    for line in out.splitlines():
        if line.strip() == "---SCORE_SUMMARY---":
            keep, block = True, [line.strip()]
            continue
        if keep:
            block.append(line.strip())
            if line.strip() == "---END---":
                break
    print()
    if block:
        print("  SCORE 契约块：")
        for line in block:
            print("    %s" % line)
    else:
        print("  ! 没抓到 SCORE 契约块，直接看上面 run_all.py 的输出")
    print("  退出码 %s" % proc.returncode)
    return proc.returncode


def step_checklist(code, old_site, ctx):
    head(9, "还需要人工改哪些地方")
    print("  新公开地址：%s/chat/%s" % (BASE, code))
    print("  旧地址    ：%s/chat/%s（仍在线，作回退）" % (BASE, old_site))
    print()
    print("  A. 交接说明.md（第 1 节关键标识表，5 格要改）")
    print("     · 公开站点 / 站点码 / 所属应用 ID / 应用侧工作流 ID / 二维码尺寸与字节数")
    print("     · 站点历史链末尾追加：%s → %s" % (old_site, code))
    print("  B. 参赛方案/提交材料/作品提交表-职引.docx")
    print("     · 「作品地址」段落改成 %s/chat/%s" % (BASE, code))
    print("     · 改完必须由 docx 重新导出 作品提交表-职引.pdf（WPS 导出的 PDF 是字体子集，文本替换不了）")
    print("  C. 提交材料里其他带旧站点码的行（以下是当场扫到的实况）：")
    rows = []
    try:
        import check_assets
        rows, _ = check_assets.scan_markdown(code)
    except Exception as e:
        print("     ! 扫 Markdown 失败：%s" % e)
    flagged = [r for r in rows if r["code"] != code and "历史" not in os.path.basename(r["file"])]
    if flagged:
        for r in flagged:
            print("     · %s:%d  %s" % (r["file"], r["line"], r["code"]))
    else:
        print("     · （无）")
    print("  D. 过程截图 / 演示视频：如重录，注意结尾二维码也要是新的")
    print("  E. 手机 4G（别连校园网）扫码走一遍全流程 —— 02 清单硬要求")
    print("  F. 旧站收尾：确认新站 5 分支 + 黄金集都过之后再改名/关停；"
          "release.py 默认不碰旧应用，回退路径保留")
    if ctx.get("retired"):
        print("     本次已按 --retire-old 改名应用 %s" % ctx.get("retire_app"))
    print()
    print("  自检：python 技术档案/check_assets.py   # 五份副本是否已经对齐")


# ---------------------------------------------------------------- dry-run
def plan(args, patch):
    """dry-run：把要执行的步骤和要改的节点 id 全部摊开，不发任何写请求。"""
    old = read_site()
    print("=" * 72)
    print("职引 · 换站发布 · DRY-RUN（不产生任何写操作）")
    print("=" * 72)
    print("  源应用     %s" % args.src)
    print("  新应用名   %s" % args.name)
    print("  当前站点   %s（readysite.txt）" % (old or "（空）"))
    print("  补丁       %s" % (args.graph or "（未提供：源应用原样复制）"))
    print()
    print("计划（真实模式按此顺序执行，任一步失败即停）：")
    print("  [1/9] 取 token          from tok import token（CONSOLE_TOKEN → 技术档案/.token）")
    print("  [2/9] POST /console/api/apps/<src>/copy        → 新 app_id，随后 PUT 改名/描述/图标")
    print("  [3/9] GET 源草稿 → GET 新草稿 → 应用补丁 → POST 新草稿")
    if patch:
        errors, warns = validate_patch(patch)
        lines = describe_patch(patch)
        if lines:
            print("        补丁将改动：")
            for line in lines:
                print("          %s" % line)
        else:
            print("        补丁文件是空的：这一步等于不做任何修改")
        for e in errors:
            print("        ! 补丁结构错误：%s" % e)
        for w in warns:
            print("        ! %s" % w)
    else:
        print("        无补丁：草稿原样保存 —— 只能换地址，改不了任何行为；")
        print("        v13 通常要带 --graph（否则等于白换一次站）")
    print("  [4/9] POST /console/api/apps/<new>/workflows/publish  marked_comment=%r"
          % (args.comment or args.name))
    print("  [5/9] 轮询 GET /console/api/apps/<new> 与 /site，直到 workflow.id == 发布结果")
    print("        → 开站后再用 X-App-Code 调一次 /api/chat-messages 核对 live workflow_id")
    print("  [6/9] POST /console/api/apps/<new>/site-enable {enable_site:true}")
    print("        → 取站点码 → 覆写 技术档案/readysite.txt（旧值 %s 会先打印出来）" % (old or "空"))
    print("  [7/9] 重出二维码 参赛方案/素材/职引-二维码-公开站点.png（旧图备份 *.oldN.png.bak）")
    print("        → 用 cv2 解码复核（make-png.py 只管 LOGO/背景，不管二维码）")
    print("  [8/9] python 技术档案/run_all.py（SITE=<新码>）→ 打印 ---SCORE_SUMMARY--- 契约块")
    print("  [9/9] 打印人工待办（交接说明 / docx / PDF / 提交材料 Markdown / 手机扫码）")
    if args.retire_old:
        print("  [附加] PUT 旧应用 %s 改名为「（回退 · 上一版）」" % args.retire_old[:8])
    print()
    if args.check_src:
        if not token_available():
            print("  --check-src 需要 token，但本机没有：跳过源应用校验。")
            print("  （取法见 tok.py：CAS 登录后 copy(localStorage.getItem('console_token'))"
                  " 写进 技术档案/.token）")
        else:
            tok = load_token()
            status, app = api("/console/api/apps/%s" % args.src, "GET", None, tok)
            if status == 200:
                print("  源应用校验：HTTP %s  name=%s  workflow=%s  site=%s"
                      % (status, pick(app, "name", default="?"),
                         str(pick(app, "workflow.id", default="?"))[:8],
                         pick(app, "site.access_token", default="（无站点）")))
            else:
                print("  源应用校验失败：HTTP %s  %s" % (status, brief(app)))
    else:
        print("  dry-run 不联网：源应用存在性未校验（要校验加 --check-src 并准备 token）。")
    print("  dry-run 不需要联网，跳过鉴权；如要校验源应用请先准备 token"
          "（CONSOLE_TOKEN 或 技术档案/.token）。")
    print()
    print("回滚方式（真实模式）：")
    print("  · 停在 2~5 步：线上地址没变，旧站仍是当前站，丢掉新应用即可（未开站点，无人可访问）。")
    print("  · 停在 6 步后：把 readysite.txt 写回 %s，二维码用 *.oldN.png.bak 覆盖回去。"
          % (old or "<旧码>"))
    print("  · 旧应用不会被自动关停，回退地址一直有效。")
    return 0


# ---------------------------------------------------------------- 主流程
def build_parser():
    p = argparse.ArgumentParser(
        prog="release.py",
        description="职引换站发布流水线：复制 → 补丁 → 发布 → 轮询 → 开站 → 二维码 → 回归")
    p.add_argument("--from", dest="src", required=True, help="源应用 ID")
    p.add_argument("--name", required=True, help="新应用显示名")
    p.add_argument("--graph", help="补丁 JSON 路径（不给则原样复制）")
    p.add_argument("--dry-run", action="store_true", help="只打印计划，不发写请求")
    p.add_argument("--check-src", action="store_true", help="dry-run 时 GET 源应用校验存在性")
    p.add_argument("--icon", default=DEFAULT_ICON, help="新应用头像哈希")
    p.add_argument("--comment", default="", help="发布备注")
    p.add_argument("--retire-old", default="", help="旧应用 ID：收尾时改名标注回退")
    p.add_argument("--skip-qr", action="store_true", help="不重出二维码")
    p.add_argument("--skip-regression", action="store_true", help="不跑 run_all.py")
    p.add_argument("--refresh-brand", action="store_true", help="额外跑 make-png.py")
    p.add_argument("--wait-site", type=int, default=180, help="等 live workflow 生效的秒数")
    p.add_argument("--interval", type=int, default=10, help="轮询间隔秒数")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)

    patch = None
    if args.graph:
        if not os.path.exists(args.graph):
            print("补丁文件不存在：%s" % args.graph)
            return 2
        try:
            patch = load_patch(args.graph)
        except (OSError, ValueError) as e:
            print("补丁读取失败：%s" % e)
            return 2
        errors, _ = validate_patch(patch)
        if errors:
            print("补丁结构有错，先改好再来：")
            for e in errors:
                print("  - %s" % e)
            return 2

    if args.dry_run:
        return plan(args, patch)

    print("=" * 72)
    print("职引 · 换站发布（真实模式）")
    print("=" * 72)

    head(1, "取 token")
    if not token_available():
        print("  本机没有控制台 token（凭据不落盘）。取法：")
        print("  1) 大赛门户 http://aiac.cqut.edu.cn:3090/ai → 「体验智小理智能体平台」走 CAS")
        print("  2) aiagent.cqut.edu.cn:31134 标签页 console：copy(localStorage.getItem('console_token'))")
        print("  3) 粘进 %s（单行）或用环境变量 CONSOLE_TOKEN" % os.path.join(HERE, ".token"))
        print("  只想看计划就用 --dry-run。")
        return 2
    tok = load_token()
    if not tok:
        return 2
    print("  token 已取到（%d 字符）" % len(tok))

    ctx = {"old_site": read_site(), "new_app": "", "draft_saved": False,
           "published": False, "site": "", "site_written": False, "qr_done": False,
           "want_wf": "", "retired": False, "retire_app": args.retire_old}

    new_id = step_copy(tok, args.src, args.name, args.icon, ctx)
    if not new_id:
        return 1
    if not step_draft(tok, args.src, new_id, patch, ctx):
        return 1
    if not step_publish(tok, new_id, args.comment or args.name, ctx):
        return 1
    want_wf = step_poll_console(tok, new_id, ctx)
    code = step_site_enable(tok, new_id, ctx)
    if not code:
        return 1

    if not poll_live(code, want_wf, ctx.get("old_live", ""), args.wait_site, args.interval):
        print()
        print("! 站点已开，但 live workflow 还没切到刚发布的版本（平台有 5~10 分钟延迟）。")
        print("  不是致命错误：过几分钟再跑 python 技术档案/run_all.py 看 wf 是否换新，")
        print("  或直接打开 %s/chat/%s 抽查。readysite.txt 已写入，先别发材料。" % (BASE, code))

    if args.skip_qr:
        print()
        print("[7/9] 跳过二维码（--skip-qr）")
    else:
        ctx["qr_done"] = step_qr(code, args.refresh_brand)

    rc = 0
    if args.skip_regression:
        print()
        print("[8/9] 跳过回归（--skip-regression）")
    else:
        rc = step_regression(code)

    if args.retire_old:
        print()
        print("[附加] 旧应用改名")
        status, obj = api("/console/api/apps/%s" % args.retire_old, "PUT",
                          {"name": "%s（回退 · 上一版）" % args.name,
                           "description": "回退用：站点 %s" % ctx.get("old_site", "")},
                          tok)
        print("  PUT -> HTTP %s  %s" % (status, brief(obj)))
        ctx["retired"] = status == 200
        print("  注意：改名不等于关站，旧地址仍可访问（回退路径保留）。")

    step_checklist(code, ctx.get("old_site", ""), ctx)

    print()
    if rc != 0:
        print("!" * 72)
        print("回归没过（run_all.py 退出码 %s）：新码 %s 先别发出去。" % (rc, code))
        print("!" * 72)
        return 1
    print("完成：%s/chat/%s" % (BASE, code))
    return 0


if __name__ == "__main__":
    sys.exit(main())
