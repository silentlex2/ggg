#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""简历诊断（带文件上传）端到端回归。

用法：python probe_resume.py <站点码> [简历文件路径]
"""
import json, os, ssl, sys, time, urllib.request

BASE = "https://aiagent.cqut.edu.cn:31134"
HERE = os.path.dirname(os.path.abspath(__file__))
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE
DEFAULT_RESUME = os.path.join(os.path.dirname(HERE), "参赛方案", "素材", "演示简历样本-化工工艺工程师.md")


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


def upload(site, tok, path):
    boundary = "----zhiyinprobe8f21"
    with open(path, "rb") as f:
        data = f.read()
    fname = "resume_probe.md"
    parts = []
    parts.append(("--" + boundary + "\r\n").encode())
    parts.append(('Content-Disposition: form-data; name="file"; filename="%s"\r\n' % fname).encode())
    parts.append(b"Content-Type: text/markdown\r\n\r\n")
    parts.append(data)
    parts.append(("\r\n--" + boundary + "--\r\n").encode())
    body = b"".join(parts)
    req = urllib.request.Request(
        BASE + "/api/files/upload", data=body, method="POST",
        headers={"Content-Type": "multipart/form-data; boundary=" + boundary,
                 "X-App-Code": site, "Authorization": "Bearer " + tok, "auth-token": "Bearer " + tok})
    with urllib.request.urlopen(req, context=CTX, timeout=90) as r:
        return json.loads(r.read().decode())


def ask(site, tok, query, extra=None, conv=""):
    payload = {
        "response_mode": "streaming", "conversation_id": conv, "query": query,
        "inputs": dict({"user_input": query}, **(extra or {})), "parent_message_id": None,
    }
    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        BASE + "/api/chat-messages", data=body, method="POST",
        headers={"Content-Type": "application/json", "X-App-Code": site,
                 "authorization": "Bearer " + tok, "auth-token": "Bearer " + tok})
    t0 = time.time()
    with urllib.request.urlopen(req, context=CTX, timeout=300) as r:
        raw = r.read().decode("utf-8", "replace")
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
    return {"cost": cost, "answer": ans, "chain": chain, "failed": failed}


def main():
    site = site_code()
    path = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_RESUME
    tok = token(site)
    print("站点:", site, " 简历:", os.path.basename(path))
    up = upload(site, tok, path)
    fid = up.get("id")
    print("上传结果: id=%s name=%s size=%s" % (str(fid)[:12], up.get("name"), up.get("size")))
    r = ask(site, tok, "帮我诊断一下简历，目标岗位是化工工艺工程师",
            {"user_file": {"type": "document", "transfer_method": "local_file", "upload_file_id": fid}})
    print("\n耗时 %.1fs  失败节点=%s" % (r["cost"], r["failed"] or "无"))
    print("节点链: " + " -> ".join(r["chain"]))
    print("-" * 72)
    print(r["answer"])


if __name__ == "__main__":
    main()
