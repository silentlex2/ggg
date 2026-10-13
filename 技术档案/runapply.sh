#!/bin/bash
# 用法: bash runapply.sh  → 依次执行 apply_iv.js 和 apply_cls.js
set -e
for f in apply_iv.js apply_cls.js; do
  echo "--- $f ---"
  B=$(base64 -w0 "$f")
  owb eval --tab 2030596171 --await-promise --expression \
    "eval(new TextDecoder('utf-8').decode(Uint8Array.from(atob('$B'),c=>c.charCodeAt(0))))" 2>&1 \
    | python -c "
import sys,json
try:
    print(json.load(sys.stdin).get('value',''))
except Exception:
    sys.stdin.seek(0); print('OWB_ERR')
"
done
