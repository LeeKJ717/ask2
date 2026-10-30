# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig7-1.svg', 790)
rows = [(['지방산', '(세포질)'], LBLUE, BLUE), (['아실-CoA', '(세포질)'], LBLUE, BLUE),
        (['아실카르니틴', '(막간 공간)'], LGOLD, GOLD), (['아실카르니틴', '(기질로 이동)'], LGOLD, GOLD),
        (['아실-CoA', '(미토콘드리아 기질)'], LGREEN, GREEN), (['아세틸-CoA + NADH + FADH2'], LGREEN, GREEN)]
ys = [30 + 125 * i for i in range(6)]
for (ls, fl, st), y in zip(rows, ys):
    f.tbox(240, y, 330, 90, ls, 22, fl, st, first_bold=True)
labs = ['ACSL', 'CPT1', 'CACT', 'CPT2', 'β산화']
for i in range(5):
    f.arrow(405, ys[i] + 90, 405, ys[i + 1], GRAY, 2.8)
    f.text(390, ys[i] + 118, labs[i], 22, 400, 'end', GRAY)
f.tbox(620, ys[1] + 75, 170, 80, ['말로닐-CoA'], 22, LWARM, WARM, first_bold=True)
f.inhibit(620, ys[1] + 115, 420, ys[1] + 115, WARM, 2.8)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig7-1.svg'), write_to=os.path.join(o, '그림7-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림7-1.png')).convert('L').save(os.path.join(o, '그림7-1-흑백.png'))
