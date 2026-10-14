#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全链路节点追踪：抓每次 node_finished 的 inputs/outputs，定位检索失败环节。

用法：python probe_trace.py [场景]
场景：job（默认）/ policy / interview / resume
"""
import json, os, ssl, sys, time, urllib.request
sys.stdout.reconfigure(encoding="utf-8")

BASE = "https://aiagent.cqut.edu.cn:31134"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SITE = open(os.path.join(HERE, "readysite.txt"), encoding="utf-8").read().strip()
PDF = os.path.join(ROOT, "参赛方案", "素材", "张明-化工工艺工程师-重庆理工大学.pdf")
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE

SCENES = {
    "job": ("我是化学工程与工艺专业大四，会 Aspen Plus，想找重庆的化工类校招岗位", None),
    "job2": ("我想找化工工艺工程师的岗位，重庆的", None),
    "policy": ("重庆高校毕业生就业补贴怎么申请", None),
    "interview": ("我想面试化工工艺工程师", None),
    "resume": ("帮我诊断一下简历，目标岗位是化工工艺工程师", "pdf"),
}

INTEREST = ("retrieval_query", "major", "city", "degree", "job_type", "target_job", "keyword",
            "topic", "qtype", "body", "result", "text", "answer")


def tok():
    req = urllib.request.Request(BASE + "/api/passport", headers={"X-App-Code": SITE})
    with urllib.request.urlopen(req, context=CTX, timeout=30) as r:
        return json.loads(r.read().decode())["access_token"]


def upload(t, path):
    boundary = "----zhiyinprobe8f21"
    data = open(path, "rb").read()
    parts = [("--" + boundary + "\r\n").encode(),
             ('Content-Disposition: form-data; name="file"; filename="resume.pdf"\r\n').encode(),
             b"Content-Type: application/pdf\r\n\r\n", data,
             ("\r\n--" + boundary + "--\r\n").encode()]
    req = urllib.request.Request(BASE + "/api/files/upload", data=b"".join(parts), method="POST",
        headers={"Content-Type": "multipart/form-data; boundary=" + boundary, "X-App-Code": SITE,
                 "Authorization": "Bearer " + t, "auth-token": "Bearer " + t})
    with urllib.request.urlopen(req, context=CTX, timeout=180) as r:
        return json.loads(r.read().decode())


def preview(v, n=260):
    if v is None:
        return "None"
    if isinstance(v, str):
        return v[:n].replace("\n", " | ")
    try:
        return json.dumps(v, ensure_ascii=False)[:n]
    except Exception:
        return str(v)[:n]


def main():
    scene = sys.argv[1] if len(sys.argv) > 1 else "job"
    q, kind = SCENES[scene]
    t = tok()
    inputs = {"user_input": q}
    if kind == "pdf":
        up = upload(t, PDF)
        inputs["user_file"] = {"type": "document", "transfer_method": "local_file", "upload_file_id": up.get("id")}
        print("已上传 resume.pdf id=" + str(up.get("id"))[:12])
    payload = {"response_mode": "streaming", "conversation_id": "", "query": q,
               "inputs": inputs, "parent_message_id": None}
    req = urllib.request.Request(BASE + "/api/chat-messages", data=json.dumps(payload).encode(),
                                 method="POST",
                                 headers={"Content-Type": "application/json", "X-App-Code": SITE,
                                          "authorization": "Bearer " + t, "auth-token": "Bearer " + t})
    t0 = time.time()
    with urllib.request.urlopen(req, context=CTX, timeout=300) as r:
        raw = r.read().decode("utf-8", "replace")
    print("场景=%s  耗时 %.1fs  输入=%s" % (scene, time.time() - t0, q))
    print("=" * 78)
    ans = ""
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
            title = d.get("title")
            o = d.get("outputs") or {}
            keep = {k: v for k, v in o.items() if k in INTEREST}
            print("\n▶ %s  [%s]" % (title, d.get("status")))
            if isinstance(keep.get("result"), list):
                res = keep["result"]
                print("   result: %d 条" % len(res))
                for i, item in enumerate(res[:3]):
                    if isinstance(item, dict):
                        print("     [%d] score=%s  %s" % (i, item.get("score"), preview(item.get("content", item), 200)))
                    else:
                        print("     [%d] %s" % (i, preview(item, 200)))
                keep.pop("result")
            for k, v in keep.items():
                print("   %s = %s" % (k, preview(v)))
    print("\n" + "=" * 78 + "\n最终回答（前 700 字）\n" + "=" * 78)
    print(ans[:700])


if __name__ == "__main__":
    main()
