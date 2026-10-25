# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig5-1.svg', 640)
f.tbox(290, 250, 220, 120, ['인크레틴 계열', '약물'], 26, LBLUE, BLUE, first_bold=True)
# 위: 췌장, 지방, 간 / 아래: 근육, 신장, 심장
items = [
 (10, 20, ['췌장', '인슐린 분비 증가', '글루카곤 감소'], LGOLD, GOLD, (290, 290)),
 (290, 20, ['지방조직', '지방량', '감소(간접)'], LGOLD, GOLD, (400, 250)),
 (570, 20, ['간', '간 지방', '감소(간접)'], LGREEN, GREEN, (510, 290)),
 (10, 510, ['근육', '제지방', '감소 우려'], LWARM, WARM, (290, 330)),
 (290, 510, ['신장', '알부민뇨', '감소 보고'], LGREEN, GREEN, (400, 370)),
 (570, 510, ['심장·혈관', '심혈관 사건', '감소 보고'], LGREEN, GREEN, (510, 330)),
]
for x, y, t, fl, st, (ax, ay) in items:
    f.tbox(x, y, 220, 120, t, 22, fl, st, first_bold=True)
    cx = x + 110; cy = y + 120 if y < 200 else y
    f.arrow(ax, ay, cx, cy, st, 2.8) if y < 200 else f.arrow(ax, ay, cx, cy, st, 2.8)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig5-1.svg'), write_to=os.path.join(o, '그림5-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림5-1.png')).convert('L').save(os.path.join(o, '그림5-1-흑백.png'))
