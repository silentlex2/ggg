# -*- coding: utf-8 -*-
"""控制台 token 取用（唯一入口）。

为什么要单独一个模块：token 是 535 字符的会话凭据，**不落仓库、不写死在脚本里**。
2026-10-20 已把原先散落在 `scratch/.token` 的明文副本删掉，改由本模块按需读取。

取用顺序：
    1. 环境变量 `CONSOLE_TOKEN`
    2. `技术档案/.token`（单行纯文本，已被 .gitignore 排除）
    3. 旧位置 `技术档案/scratch/.token`（兼容老用法）

都没有时抛 SystemExit 并打印取 token 的方法：

    浏览器里走完 CAS 登录（门户 http://aiac.cqut.edu.cn:3090/ai → 点「体验智小理智能体平台」），
    在 aiagent.cqut.edu.cn:31134 标签页的 console 里执行：
        copy(localStorage.getItem('console_token'))
    然后把剪贴板粘进 技术档案/.token（单行，不要换行、不要引号）。

注意：站点只读回归（run_all.py / eval_golden.py / finaltest_ready.py）**不需要** token，
走的是 /api/passport + X-App-Code，无需登录。只有控制台/草稿/克隆类脚本才要。
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def token():
    env = os.environ.get("CONSOLE_TOKEN", "").strip()
    if env:
        return env
    for rel in (".token", os.path.join("scratch", ".token")):
        path = os.path.join(HERE, rel)
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                value = f.read().strip().strip('"').strip("'")
            if value:
                return value
    raise SystemExit(
        "缺少控制台 token。\n"
        "  1) 走 CAS 登录进平台：http://aiac.cqut.edu.cn:3090/ai → 「体验智小理智能体平台」\n"
        "  2) 在 aiagent.cqut.edu.cn:31134 标签页 console 执行： copy(localStorage.getItem('console_token'))\n"
        "  3) 粘进 %s（单行；该文件已被 .gitignore 排除）\n"
        "  或用环境变量 CONSOLE_TOKEN 临时传入。\n"
        "  只读回归不需要 token。"
        % os.path.join(HERE, ".token"))
