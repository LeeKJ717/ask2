#!/bin/bash
# SVG → PNG 미리보기 (눈 검수용, 흑백 변환본도 함께 만든다)
# 사용: tools/preview_figs.sh fig/fig13_1.svg [fig/...]   → preview/fig13_1.png, preview/fig13_1_gray.png
ROOT="$(pwd)"   # 책 프로젝트 루트에서 실행: preview/ 에 PNG 생성
mkdir -p "$ROOT/preview"
for f in "$@"; do
  b=$(basename "$f" .svg)
  rsvg-convert -w 1100 -b white "$f" -o "$ROOT/preview/$b.png" && echo "$ROOT/preview/$b.png"
  python3 - "$ROOT/preview/$b.png" "$ROOT/preview/${b}_gray.png" <<'EOF' 2>/dev/null
import sys
from PIL import Image
Image.open(sys.argv[1]).convert('L').save(sys.argv[2])
EOF
done
