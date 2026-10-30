# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig6-1.svg', 600)
ys = [60 + 130 * i for i in range(4)]
Lb = ['시트르산', '이소시트르산', 'α-케토글루타르산', '숙시닐-CoA']
Rb = ['옥살로아세트산', '말산', '푸마르산', '숙신산']
for n, y in zip(Lb, ys): f.tbox(20, y, 300, 80, [n], 24, LGOLD, GOLD)
for n, y in zip(Rb, ys): f.tbox(480, y, 300, 80, [n], 24, LGREEN, GREEN)
ll = ['', 'CO2 · NADH', 'CO2 · NADH']
for i in range(3):
    f.arrow(170, ys[i] + 80, 170, ys[i + 1], GOLD, 2.8)
    if ll[i]: f.text(185, ys[i] + 112, ll[i], 22, 400, 'start', WARM)
rl = ['NADH', '', 'FADH2']
for i in range(3):
    f.arrow(630, ys[i + 1], 630, ys[i] + 80, GREEN, 2.8)
    if rl[i]: f.text(645, ys[i] + 112, rl[i], 22, 400, 'start', WARM)
f.arrow(320, ys[3] + 40, 480, ys[3] + 40, GRAY, 2.8); f.text(400, ys[3] + 25, 'GTP', 22, 400, 'middle', WARM)
f.arrow(480, ys[0] + 40, 320, ys[0] + 40, GRAY, 2.8); f.text(400, 45, '+ 아세틸-CoA', 22, 700, 'middle', GOLD)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig6-1.svg'), write_to=os.path.join(o, '그림6-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림6-1.png')).convert('L').save(os.path.join(o, '그림6-1-흑백.png'))
