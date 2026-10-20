# -*- coding: utf-8 -*-
"""对比三种把文件喂进简历分支的方式，找出真正让文档提取拿到内容的那一种。

A. 只传 files[]（对应 sys.files，start 变量 user_file 仍为空）
B. 只传 inputs.user_file 为文件对象
C. 两者都传
"""
import json
import mimetypes
import os
import ssl
import sys
import urllib.request
import uuid

sys.stdout.reconfigure(encoding="utf-8")
BASE = "https://aiagent.cqut.edu.cn:31134"
KEY = "app-8PKbSyrPSFnPGjQ5AQX6u1Zl"
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE
PDF = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "参赛方案", "素材",
                   "张明-化工工艺工程师-重庆理工大学.pdf")
HDR = {"Authorization": "Bearer " + KEY}


def upload():
    boundary = "----zhiyin" + uuid.uuid4().hex
    with open(PDF, "rb") as fh:
        content = fh.read()
    ctype = mimetypes.guess_type(PDF)[0] or "application/pdf"
    parts = []
    parts.append(("--%s\r\nContent-Disposition: form-data; name=\"user\"\r\n\r\nuprobe\r\n"
                  % boundary).encode())
    parts.append(("--%s\r\nContent-Disposition: form-data; name=\"file\"; filename=\"%s\"\r\n"
                  "Content-Type: %s\r\n\r\n" % (boundary, os.path.basename(PDF), ctype)).encode())
    parts.append(content)
    parts.append(b"\r\n")
    parts.append(("--%s--\r\n" % boundary).encode())
    req = urllib.request.Request(BASE + "/v1/files/upload", data=b"".join(parts), method="POST",
                                 headers={"Authorization": "Bearer " + KEY,
                                          "Content-Type": "multipart/form-data; boundary=" + boundary})
    with urllib.request.urlopen(req, context=CTX, timeout=180) as r:
        return json.loads(r.read().decode()).get("id")


def chat(payload):
    req = urllib.request.Request(BASE + "/v1/chat-messages", data=json.dumps(payload).encode(),
                                 method="POST",
                                 headers=dict(HDR, **{"Content-Type": "application/json"}))
    with urllib.request.urlopen(req, context=CTX, timeout=300) as r:
        return json.loads(r.read().decode("utf-8", "replace"))


FID = upload()
print("file id = %s" % FID)
Q = "帮我诊断一下这份简历，我想投重庆的化工工艺工程师岗位"
FILE_OBJ = {"type": "document", "transfer_method": "local_file", "upload_file_id": FID}

CASES = [
    ("A 只传 files[]", {"inputs": {"user_input": Q, "ctx": ""},
                        "files": [FILE_OBJ]}),
    ("B 只传 inputs.user_file", {"inputs": {"user_input": Q, "ctx": "", "user_file": FILE_OBJ}}),
    ("C 两者都传", {"inputs": {"user_input": Q, "ctx": "", "user_file": FILE_OBJ},
                    "files": [FILE_OBJ]}),
]

for label, extra in CASES:
    payload = {"query": Q, "response_mode": "blocking", "conversation_id": "",
               "user": "uprobe", "inputs": extra["inputs"]}
    if "files" in extra:
        payload["files"] = extra["files"]
    try:
        j = chat(payload)
    except Exception as exc:  # noqa: BLE001
        print("")
        print("%s -> 请求失败 %r" % (label, exc))
        continue
    ans = j.get("answer") or ""
    print("")
    print("%s -> %d 字" % (label, len(ans)))
    print("   " + ans[:260].replace("\n", " "))
