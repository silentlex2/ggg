# -*- coding: utf-8 -*-
"""政策实时源体检：① 本机能否直连 ncss.cn ② 线上政策分支是否还能吐出带日期的条目。

两道检查分开，是为了区分"是平台侧 HTTP 节点坏了"还是"本机网络出不去"。
"""
import json
import re
import ssl
import sys
import time
import urllib.error
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")
BASE = "https://aiagent.cqut.edu.cn:31134"
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE
SITE = open("readysite.txt", encoding="utf-8").read().strip()


def check_local_net():
    print("① 本机直连 www.ncss.cn")
    req = urllib.request.Request("https://www.ncss.cn/", headers={"User-Agent": "Mozilla/5.0"})
    try:
        t0 = time.time()
        with urllib.request.urlopen(req, context=CTX, timeout=15) as resp:
            body = resp.read(4000).decode("utf-8", "replace")
        print("   [%s] %.1fs  %d 字节" % (resp.status, time.time() - t0, len(body)))
        return True
    except Exception as exc:  # noqa: BLE001
        print("   [失败] %r" % (exc,))
        return False


def ask(q):
    req = urllib.request.Request(BASE + "/api/passport", headers={"X-App-Code": SITE})
    with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
        tok = json.loads(resp.read().decode())["access_token"]
    # /api 这条要用 streaming 模式（blocking 会 400，实测），答案从 SSE 里拼
    body = json.dumps({"response_mode": "streaming", "conversation_id": "", "query": q,
                       "inputs": {"user_input": q}, "parent_message_id": None}).encode()
    req = urllib.request.Request(BASE + "/api/chat-messages", data=body, method="POST",
                                 headers={"Content-Type": "application/json", "X-App-Code": SITE,
                                          "authorization": "Bearer " + tok,
                                          "auth-token": "Bearer " + tok})
    t0 = time.time()
    with urllib.request.urlopen(req, context=CTX, timeout=300) as resp:
        raw = resp.read().decode("utf-8", "replace")
    ans = ""
    for blk in raw.replace("\r\n", "\n").split("\n\n"):
        if not blk.startswith("data:"):
            continue
        try:
            j = json.loads(blk[5:].strip())
        except Exception:  # noqa: BLE001
            continue
        if j.get("event") == "message":
            ans += j.get("answer") or ""
    return ans, time.time() - t0


def main():
    net = check_local_net()
    print("")
    print("② 线上政策分支：问「最近有什么新的就业政策」")
    q = "最近有什么新的就业政策"
    ans, sec = ask(q)
    dates = re.findall(r"20\d{2}[-年]\d{1,2}[-月]\d{1,2}", ans)
    print("   回答 %d 字，%.1fs，带日期条目 %d 个" % (len(ans), sec, len(dates)))
    print("   提到 ncss / 国家大学生就业服务平台：%s" % ("是" if re.search(r"ncss|国家大学生就业服务平台", ans) else "否"))
    print("   ---- 开头 400 字 ----")
    print("   " + ans[:400].replace("\n", " "))
    print("")
    print("---NCSS_SUMMARY---")
    print("LOCAL_NET: %s" % ("ok" if net else "blocked"))
    print("ANSWER_CHARS: %d" % len(ans))
    print("DATED_ITEMS: %d" % len(dates))
    print("---END---")


if __name__ == "__main__":
    main()
