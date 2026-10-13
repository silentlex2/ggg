#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, ssl, sys, time, urllib.request
BASE="https://aiagent.cqut.edu.cn:31134"
CTX=ssl.create_default_context(); CTX.check_hostname=False; CTX.verify_mode=ssl.CERT_NONE
site=sys.argv[1]; want=sys.argv[2]; tries=int(sys.argv[3]) if len(sys.argv)>3 else 8
def tok():
    for a in range(3):
        try:
            req=urllib.request.Request(BASE+"/api/passport",headers={"X-App-Code":site})
            with urllib.request.urlopen(req,context=CTX,timeout=30) as r:
                return json.loads(r.read().decode())["access_token"]
        except Exception: time.sleep(3)
    return ""
def livewf(t):
    for a in range(4):
        body=json.dumps({"response_mode":"streaming","conversation_id":"","query":"你好",
            "inputs":{"user_input":"你好"},"parent_message_id":None}).encode()
        req=urllib.request.Request(BASE+"/api/chat-messages",data=body,method="POST",
            headers={"Content-Type":"application/json","authorization":"Bearer "+t,"auth-token":"Bearer "+t})
        try:
            with urllib.request.urlopen(req,context=CTX,timeout=240) as r: raw=r.read().decode("utf-8","replace")
        except Exception: time.sleep(4); continue
        raw=raw.replace("\r\n","\n")
        for blk in raw.split("\n\n"):
            if not blk.startswith("data:"): continue
            try: j=json.loads(blk[5:].strip())
            except Exception: continue
            if j.get("event")=="workflow_finished": return (j.get("data") or {}).get("workflow_id","")
        time.sleep(3)
    return ""
t=tok()
if not t: print("TOKEN_FAIL"); sys.exit(1)
for i in range(tries):
    w=livewf(t)
    ok = (w==want)
    print("poll%d live=%s want=%s %s" % (i+1,w,want,"MATCH" if ok else "mismatch"))
    if ok: sys.exit(0)
    time.sleep(10)
sys.exit(2)
