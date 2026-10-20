# -*- coding: utf-8 -*-
r"""提交材料 加密归档 / 还原（AES-256-GCM + PBKDF2-HMAC-SHA256）

为什么用这个而不是 zip 口令：Windows 自带 Compress-Archive 不支持加密，
本机也没有 7z / WinRAR；Python 标准库 zipfile 不能写加密包。
这里用 cryptography 的标准算法自组一个带认证的容器，格式简单、可校验。

用法（在仓库根目录执行）：
    python 参赛方案/tools/submission-archive.py pack   --password-file F:\path\口令.txt
    python 参赛方案/tools/submission-archive.py unpack --archive F:\path\xxx.tar.gz.enc --password-file F:\path\口令.txt --dest D:\restore

容器格式：
    magic  b"ZYSUB1\n"
    salt   16 字节随机（PBKDF2 盐）
    nonce  12 字节随机（GCM nonce）
    tag    16 字节（GCM 认证标签）
    body   AES-256-GCM 密文（明文 = tar.gz 字节流）

口令丢失 = 数据不可恢复（没有后门、没有 escrow）。口令文件放仓库外。
"""
import argparse
import io
import os
import sys
import tarfile

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

MAGIC = b"ZYSUB1\n"
SALT_LEN, NONCE_LEN, TAG_LEN = 16, 12, 16
ITER = 600_000

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
SRC = os.path.join(REPO, "参赛方案", "提交材料")


def key_from(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=ITER)
    return kdf.derive(password.encode("utf-8"))


def read_password(path: str) -> str:
    with io.open(path, encoding="utf-8") as f:
        pw = f.read().strip()
    if len(pw) < 16:
        raise SystemExit("口令少于 16 字符，换一个更长的")
    return pw


def pack(src: str, out: str, password: str) -> None:
    if not os.path.isdir(src):
        raise SystemExit("找不到目录：%s" % src)
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        for name in sorted(os.listdir(src)):
            p = os.path.join(src, name)
            tar.add(p, arcname=os.path.join("提交材料", name))
    plain = buf.getvalue()

    salt, nonce = os.urandom(SALT_LEN), os.urandom(NONCE_LEN)
    ct = AESGCM(key_from(password, salt)).encrypt(nonce, plain, MAGIC)
    body, tag = ct[:-TAG_LEN], ct[-TAG_LEN:]
    with open(out, "wb") as f:
        f.write(MAGIC + salt + nonce + tag + body)
    print("已加密归档：%s" % out)
    print("  明文 tar.gz %d 字节 -> 容器 %d 字节" % (len(plain), os.path.getsize(out)))
    print("  算法 AES-256-GCM / PBKDF2-SHA256 %d 轮" % ITER)


def unpack(archive: str, dest: str, password: str) -> None:
    with open(archive, "rb") as f:
        blob = f.read()
    if not blob.startswith(MAGIC):
        raise SystemExit("不是本工具的容器（magic 不匹配）")
    off = len(MAGIC)
    salt = blob[off:off + SALT_LEN]; off += SALT_LEN
    nonce = blob[off:off + NONCE_LEN]; off += NONCE_LEN
    tag = blob[off:off + TAG_LEN]; off += TAG_LEN
    body = blob[off:]
    try:
        plain = AESGCM(key_from(password, salt)).decrypt(nonce, body + tag, MAGIC)
    except Exception:
        raise SystemExit("解密失败：口令不对，或容器被改动过")
    os.makedirs(dest, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(plain), mode="r:gz") as tar:
        tar.extractall(dest)
    n = sum(len(files) for _, _, files in os.walk(dest))
    print("已还原到：%s（%d 个文件）" % (dest, n))


def main() -> int:
    ap = argparse.ArgumentParser(description="提交材料加密归档工具")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("pack"); p.add_argument("--out", default=os.path.join(os.path.dirname(REPO), "职引-提交材料-%s.tar.gz.enc" % "20261020")); p.add_argument("--password-file", required=True); p.add_argument("--src", default=SRC)
    u = sub.add_parser("unpack"); u.add_argument("--archive", required=True); u.add_argument("--password-file", required=True); u.add_argument("--dest", required=True)
    a = ap.parse_args()
    pw = read_password(a.password_file)
    if a.cmd == "pack":
        pack(a.src, a.out, pw)
    else:
        unpack(a.archive, a.dest, pw)
    return 0


if __name__ == "__main__":
    sys.exit(main())
