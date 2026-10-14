#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""异常兜底逐条验证（对应 04 手册第六节的 8 类异常）。

用法：python probe_exceptions.py <站点码>
"""
import json, os, ssl, sys, time, urllib.request

BASE = "https://aiagent.cqut.edu.cn:31134"
HERE = os.path.dirname(os.path.abspath(__file__))
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE


def site_code():
    if len(sys.argv) > 1:
        return sys.argv[1].strip()
    p = os.path.join(HERE, "readysite.txt")
    if os.path.exists(p):
        return open(p, encoding="utf-8").read().strip()
    sys.exit("缺少站点码")


def token(site):
    req = urllib.request.Request(BASE + "/api/passport", headers={"X-App-Code": site})
    with urllib.request.urlopen(req, context=CTX, timeout=30) as r:
        return json.loads(r.read().decode())["access_token"]


def upload(site, tok, path, fname):
    boundary = "----zhiyinexc7c31"
    with open(path, "rb") as f:
        data = f.read()
    parts = [("--" + boundary + "\r\n").encode(),
             ('Content-Disposition: form-data; name="file"; filename="%s"\r\n' % fname).encode(),
             b"Content-Type: text/markdown\r\n\r\n", data,
             ("\r\n--" + boundary + "--\r\n").encode()]
    req = urllib.request.Request(
        BASE + "/api/files/upload", data=b"".join(parts), method="POST",
        headers={"Content-Type": "multipart/form-data; boundary=" + boundary,
                 "X-App-Code": site, "Authorization": "Bearer " + tok, "auth-token": "Bearer " + tok})
    with urllib.request.urlopen(req, context=CTX, timeout=90) as r:
        return json.loads(r.read().decode())


def ask(site, tok, query, extra=None, conv=""):
    payload = {"response_mode": "streaming", "conversation_id": conv, "query": query,
               "inputs": dict({"user_input": query}, **(extra or {})), "parent_message_id": None}
    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        BASE + "/api/chat-messages", data=body, method="POST",
        headers={"Content-Type": "application/json", "X-App-Code": site,
                 "authorization": "Bearer " + tok, "auth-token": "Bearer " + tok})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=300) as r:
            raw = r.read().decode("utf-8", "replace")
    except Exception as e:
        return {"err": str(e)[:90], "answer": "", "chain": [], "cost": time.time() - t0, "failed": []}
    cost = time.time() - t0
    ans, chain, failed = "", [], []
    for blk in raw.replace("\r\n", "\n").split("\n\n"):
        if not blk.startswith("data:"):
            continue
        try:
            j = json.loads(blk[5:].strip())
        except Exception:
            continue
        ev = j.get("event")
        if ev == "message":
            ans += j.get("answer", "")
        elif ev == "node_finished":
            d = j.get("data", {})
            chain.append(d.get("title"))
            if d.get("status") == "failed":
                failed.append(d.get("title"))
    return {"answer": ans, "chain": chain, "cost": cost, "failed": failed}


def main():
    site = site_code()
    tok = token(site)
    print("站点:", site, " 凭证: OK")
    cases = []

    # 8 空输入
    cases.append(("8 空输入（全角空格）", "　", None))
    cases.append(("8b 空输入（纯标点）", "？？？", None))
    # 3 目标岗位缺失
    cases.append(("3 目标岗位缺失", "帮我匹配岗位", None))
    # 6 知识库召回为空（问库外政策）
    cases.append(("6 库外政策问题", "美国 OPT 实习签证怎么申请？", None))
    # 7 面试上下文（新会话直接说继续）
    cases.append(("7 新会话说继续", "继续", None))
    # 1 文档提取为空的近似：内容极少的文件
    tiny = os.path.join(HERE, "scratch", "tiny-resume.md")
    os.makedirs(os.path.dirname(tiny), exist_ok=True)
    with open(tiny, "w", encoding="utf-8") as f:
        f.write("简历")
    up = upload(site, tok, tiny, "tiny.md")
    cases.append(("1 极简文件触发诊断", "帮我诊断简历",
                  {"user_file": {"type": "document", "transfer_method": "local_file", "upload_file_id": up.get("id")}}))

    for name, q, extra in cases:
        r = ask(site, tok, q, extra)
        print("\n" + "=" * 72)
        print("【%s】query=%r" % (name, q))
        if r.get("err"):
            print("请求异常:", r["err"])
            continue
        print("耗时 %.1fs  失败节点=%s" % (r["cost"], r["failed"] or "无"))
        print("节点链: " + " -> ".join(r["chain"]))
        print("-" * 72)
        print(r["answer"][:400])


if __name__ == "__main__":
    main()
