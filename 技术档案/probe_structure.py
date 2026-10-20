#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""结构核实：站点开场白 + 岗位匹配 / 简历诊断的实际输出结构。

用法：python probe_structure.py
"""
import json, os, re, ssl, sys, time, urllib.request, urllib.error
from tok import token  # 控制台 token 统一入口（见 tok.py）
sys.stdout.reconfigure(encoding="utf-8")

BASE = "https://aiagent.cqut.edu.cn:31134"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SITE = open(os.path.join(HERE, "readysite.txt"), encoding="utf-8").read().strip()
APP = "69fa1c02-27bf-41fc-a7d2-0c068480c034"
PDF = os.path.join(ROOT, "参赛方案", "素材", "张明-化工工艺工程师-重庆理工大学.pdf")
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE


def http(url, headers=None, timeout=60):
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, context=CTX, timeout=timeout) as r:
        return r.status, r.read().decode("utf-8", "replace")


def get(url, headers=None, timeout=60):
    return json.loads(http(url, headers, timeout)[1])


def token(site):
    return get(BASE + "/api/passport", {"X-App-Code": site})["access_token"]


def hdrs(tok):
    return {"Content-Type": "application/json", "X-App-Code": SITE,
            "authorization": "Bearer " + tok, "auth-token": "Bearer " + tok}


def upload(tok, path):
    boundary = "----zhiyinprobe8f21"
    data = open(path, "rb").read()
    parts = [("--" + boundary + "\r\n").encode(),
             ('Content-Disposition: form-data; name="file"; filename="resume.pdf"\r\n').encode(),
             b"Content-Type: application/pdf\r\n\r\n", data,
             ("\r\n--" + boundary + "--\r\n").encode()]
    req = urllib.request.Request(BASE + "/api/files/upload", data=b"".join(parts), method="POST",
        headers={"Content-Type": "multipart/form-data; boundary=" + boundary, "X-App-Code": SITE,
                 "Authorization": "Bearer " + tok, "auth-token": "Bearer " + tok})
    with urllib.request.urlopen(req, context=CTX, timeout=180) as r:
        return json.loads(r.read().decode())


def ask(tok, query, extra=None):
    payload = {"response_mode": "streaming", "conversation_id": "", "query": query,
               "inputs": dict({"user_input": query}, **(extra or {})), "parent_message_id": None}
    req = urllib.request.Request(BASE + "/api/chat-messages", data=json.dumps(payload).encode(),
                                 method="POST", headers=hdrs(tok))
    t0 = time.time()
    with urllib.request.urlopen(req, context=CTX, timeout=300) as r:
        raw = r.read().decode("utf-8", "replace")
    ans, chain = "", []
    for blk in raw.replace("\r\n", "\n").split("\n\n"):
        if not blk.startswith("data:"):
            continue
        try:
            j = json.loads(blk[5:].strip())
        except Exception:
            continue
        if j.get("event") == "message":
            ans += j.get("answer", "")
        elif j.get("event") == "node_finished":
            chain.append(j.get("data", {}).get("title"))
    return time.time() - t0, ans, chain


def section(t):
    print("\n" + "=" * 78 + "\n" + t + "\n" + "=" * 78)


def probe_site_cfg():
    section("1. 站点开场白 · 端点探测")
    ct = ""
    tf = os.path.join(HERE, "scratch", ".token")
    if os.path.exists(tf):
        ct = open(tf, encoding="utf-8").read().strip()
    auth = {"Authorization": "Bearer " + ct, "OperToken": ct, "Accept": "application/json"}
    for path in ["/console/api/apps/" + APP,
                 "/console/api/apps/" + APP + "/site",
                 "/console/api/apps/" + APP + "/site/app",
                 "/console/api/apps/" + APP + "/sites"]:
        try:
            st, body = http(BASE + path, auth, 40)
            print("[%s] %s -> %d  %s" % ("console", path, st, body[:160]))
        except urllib.error.HTTPError as e:
            print("[%s] %s -> HTTP %d %s" % ("console", path, e.code, e.read().decode("utf-8", "replace")[:120]))
        except Exception as e:
            print("[%s] %s -> ERR %r" % ("console", path, e))

    for path in ["/api/site", "/api/web/site", "/api/app-params"]:
        try:
            st, body = http(BASE + path, {"X-App-Code": SITE}, 30)
            print("[%s] %s -> %d  %s" % ("public", path, st, body[:120]))
        except urllib.error.HTTPError as e:
            print("[%s] %s -> HTTP %d" % ("public", path, e.code))
        except Exception as e:
            print("[%s] %s -> ERR %r" % ("public", path, e))

    # 直接抓站点 HTML，找内嵌配置
    try:
        st, html = http(BASE + "/chat/" + SITE, {"User-Agent": "Mozilla/5.0"}, 60)
        print("\n[html] /chat/%s -> %d, %d 字节" % (SITE, st, len(html)))
        for key in ["opening_statement", "suggested_questions", "opening_questions"]:
            i = html.find(key)
            print("  含 %-22s : %s" % (key, "是" if i >= 0 else "否"))
            if i >= 0:
                print("    片段:", html[i:i + 400].replace("\\n", " "))
    except Exception as e:
        print("[html] ERR %r" % e)


def main():
    probe_site_cfg()
    tok = token(SITE)

    section("2. 岗位匹配 · 实际输出")
    c, a, ch = ask(tok, "我是化学工程与工艺专业大四，会 Aspen Plus，想找重庆的化工类校招岗位")
    print("耗时 %.1fs  节点链: %s" % (c, " -> ".join(ch)))
    print("-" * 78)
    print(a)

    section("3. 简历诊断（上传 PDF）· 实际输出")
    up = upload(tok, PDF)
    fid = up.get("id")
    print("上传: id=%s name=%s size=%s" % (str(fid)[:12], up.get("name"), up.get("size")))
    c, a, ch = ask(tok, "帮我诊断一下简历，目标岗位是化工工艺工程师",
                   {"user_file": {"type": "document", "transfer_method": "local_file", "upload_file_id": fid}})
    print("耗时 %.1fs  节点链: %s" % (c, " -> ".join(ch)))
    print("-" * 78)
    print(a)


if __name__ == "__main__":
    main()
