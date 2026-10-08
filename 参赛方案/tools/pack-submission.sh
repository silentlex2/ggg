#!/usr/bin/env bash
# 「职引」提交材料打包脚本
#
# 用法：
#   ./tools/pack-submission.sh "张明" "13800000000"
#
# 产出：
#   提交包-<队长姓名><联系方式>.zip        ← 直接上传官网指定端口
#
# 官方要求（指南 5）：
#   - 所有材料打包压缩，命名为「队长姓名 + 联系方式」
#   - 不按要求提交或材料不全者，视为形式审查不通过
set -euo pipefail

NAME="${1:-}"
CONTACT="${2:-}"

if [[ -z "$NAME" || -z "$CONTACT" ]]; then
  echo "用法: $0 <队长姓名> <联系方式>" >&2
  echo "示例: $0 \"张明\" \"13800000000\"" >&2
  exit 2
fi

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

STAGE="$(mktemp -d)"
PKG_NAME="${NAME}${CONTACT}"
DEST="${STAGE}/${PKG_NAME}"
mkdir -p "$DEST"

say() { printf '  %s\n' "$1"; }
missing=0

# ---------------------------------------------------------------- 必需材料
echo "检查并收集必需材料（官方硬性要求）："

# 1) 作品提交表（PDF）
shopt -s nullglob
pdfs=("$ROOT"/提交材料/*提交表*.pdf)
if (( ${#pdfs[@]} > 0 )); then
  cp "${pdfs[@]}" "$DEST/"
  say "✅ 作品提交表 PDF：${#pdfs[@]} 份"
else
  say "❌ 缺少《作品提交表》PDF —— 用 02-提交材料清单.md 的三份正式稿填入官方模板后导出"
  missing=1
fi

# 2) 作品演示视频（≤3 分钟）
vids=("$ROOT"/提交材料/*演示视频*.* "$ROOT"/提交材料/*demo*.*)
if (( ${#vids[@]} > 0 )); then
  cp "${vids[@]}" "$DEST/"
  say "✅ 作品演示视频：${#vids[@]} 个（务必确认时长 < 3:00）"
else
  say "❌ 缺少作品演示视频（≤3 分钟）—— 脚本见 01-路演与答辩.md §四"
  missing=1
fi

# 3) 团队活动记录：图片 ≥3 张、视频 ≥30 秒
imgs=("$ROOT"/提交材料/团队活动*.jpg "$ROOT"/提交材料/团队活动*.jpeg \
      "$ROOT"/提交材料/团队活动*.png "$ROOT"/提交材料/团队活动*.heic)
recv=("$ROOT"/提交材料/团队活动*.mp4 "$ROOT"/提交材料/团队活动*.mov)
if (( ${#imgs[@]} >= 3 )); then
  cp "${imgs[@]}" "$DEST/"
  say "✅ 团队活动记录图片：${#imgs[@]} 张（要求 ≥3）"
else
  say "❌ 团队活动记录图片不足（当前 ${#imgs[@]} 张，要求 ≥3 张）"
  missing=1
fi
if (( ${#recv[@]} > 0 )); then
  cp "${recv[@]}" "$DEST/"
  say "✅ 团队活动记录视频：${#recv[@]} 个（务必确认时长 ≥30 秒）"
else
  say "⚠️  未发现团队活动记录视频（官方要求视频不少于 30 秒，建议补）"
fi

# ---------------------------------------------------------------- 可选加分材料
echo ""
echo "收集加分材料（有则带上）："
opt=("$ROOT"/提交材料/作品截图*.png "$ROOT"/提交材料/作品截图*.jpg)
if (( ${#opt[@]} > 0 )); then
  cp "${opt[@]}" "$DEST/"
  say "✅ 作品截图：${#opt[@]} 张"
else
  say "⚠️  未发现作品截图（建议 3–5 张，优先级见 02 §二）"
fi

# 工作流编排截图 / 监测数据截图（命名任意，放在 提交材料/ 下即可）
for f in "$ROOT"/提交材料/*.png "$ROOT"/提交材料/*.jpg; do
  [[ -f "$f" ]] || continue
  cp -n "$f" "$DEST/" 2>/dev/null || true
done

# ---------------------------------------------------------------- 打包
echo ""
ZIP="${ROOT}/提交包-${PKG_NAME}.zip"
rm -f "$ZIP"
( cd "$STAGE" && zip -r -q "$ZIP" "$PKG_NAME" )
rm -rf "$STAGE"

echo "已生成：$(basename "$ZIP")  ($(du -h "$ZIP" | cut -f1))"
echo "包内文件："
unzip -l "$ZIP" | sed -n '4,$p' | head -n -2 | sed 's/^/  /'

if (( missing == 1 )); then
  echo ""
  echo "⚠️  有必需材料缺失（见上面的 ❌），此时提交会被视为「形式审查不通过」。"
  exit 1
fi

echo ""
echo "✅ 必需材料齐全。提交前请再过一遍 02-提交材料清单.md §三 的检查表："
echo "   - [ ] 作品地址在别的设备（手机 4G）能打开"
echo "   - [ ] 演示视频时长 < 3:00，能正常播放"
echo "   - [ ] 报名信息与提交表完全一致（队名/姓名/学号/手机号）"
echo "   - [ ] 11/10 18:00 前通过官网指定端口提交，提交后截图留证"
