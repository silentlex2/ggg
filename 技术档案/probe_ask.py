# -*- coding: utf-8 -*-
"""通用问句探针：给站点码 + 若干问句，逐条打印回答长度与全文。

用法：
    python probe_ask.py <站点码> q1 "q2" ...        # 直接给问句
    python probe_ask.py <站点码> --file qs.txt      # 每行一个问句
    python probe_ask.py <站点码> --repeat 3 --file qs.txt   # 每条重复 N 次
"""
import json, ssl, sys, time, urllib.request, urllib.error

BASE = "https://aiagent.cqut.edu.cn:31134"
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

A = list(sys.argv[1:])
SITE = A.pop(0)
REPEAT = 1
if "--repeat" in A:
    i = A.index("--repeat")
    REPEAT = int(A[i + 1])
    del A[i:i + 2]
QS = []
if "--file" in A:
    i = A.index("--file")
    with open(A[i + 1], encoding="utf-8") as f:
        QS = [l.rstrip("\n") for l in f if l.strip()]
    del A[i:i + 2]
QS += A


def tok():
    r = urllib.request.Request(BASE + "/api/passport", headers={"X-App-Code": SITE})
    with urllib.request.urlopen(r, context=CTX, timeout=30) as resp:
        return json.loads(resp.read().decode())["access_token"]


def ask(q, t):
    body = json.dumps({"response_mode": "streaming", "conversation_id": "", "query": q,
                       "inputs": {"user_input": q}, "parent_message_id": None}).encode()
    r = urllib.request.Request(BASE + "/api/chat-messages", data=body, method="POST",
        headers={"Content-Type": "application/json", "X-App-Code": SITE,
                 "authorization": "Bearer " + t, "auth-token": "Bearer " + t})
    try:
        with urllib.request.urlopen(r, context=CTX, timeout=400) as resp:
            raw = resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return "[HTTP %d] %s" % (e.code, e.read().decode("utf-8", "replace")[:300])
    ans = ""
    for blk in raw.replace("\r\n", "\n").split("\n\n"):
        if not blk.startswith("data:"):
            continue
        try:
            j = json.loads(blk[5:].strip())
        except Exception:
            continue
        if j.get("event") == "message":
            ans += j.get("answer", "")
    return ans


def main():
    t = tok()
    print("站点 %s   问句 %d 条   每条重复 %d 次" % (SITE, len(QS), REPEAT))
    for q in QS:
        for k in range(REPEAT):
            t0 = time.time()
            a = ask(q, t)
            print("\n" + "=" * 78)
            print("Q[%d/%d] %s" % (k + 1, REPEAT, q))
            print("长度 %d   耗时 %.1fs" % (len(a), time.time() - t0))
            print("-" * 78)
            print(a)
    return 0


if __name__ == "__main__":
    sys.exit(main())
