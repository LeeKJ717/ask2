# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig7-2.svg', 650)
rows = [(['시트르산', '(미토콘드리아에서 세포질로)'], LGOLD, GOLD), (['아세틸-CoA'], LBLUE, BLUE),
        (['말로닐-CoA'], LWARM, WARM), (['팔미트산 (탄소 16개)'], LGREEN, GREEN), (['중성지방'], LGREEN, GREEN)]
ys = [30 + 125 * i for i in range(5)]
for (ls, fl, st), y in zip(rows, ys):
    f.tbox(60, y, 440, 80, ls, 22, fl, st, first_bold=True)
labs = ['ACLY', 'ACC: 인슐린 활성, AMPK 억제', 'FASN: NADPH 필요', '에스터화']
for i in range(4):
    f.arrow(280, ys[i] + 80, 280, ys[i + 1], GRAY, 2.8)
    f.text(295, ys[i] + 108, labs[i], 22, 400, 'start', GRAY)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig7-2.svg'), write_to=os.path.join(o, '그림7-2.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림7-2.png')).convert('L').save(os.path.join(o, '그림7-2-흑백.png'))
