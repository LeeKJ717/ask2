# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig9-1.svg', 800)
f.text(170, 28, '미토콘드리아 기질', 22, 700, 'middle', GOLD)
f.text(630, 292, '세포질', 22, 700, 'middle', BLUE)
L = [(['NH4+ + CO2 + ATP'], LGOLD, GOLD), (['카르바모일 인산'], LGOLD, GOLD), (['시트룰린'], LGOLD, GOLD)]
Ly = [50 + 125 * i for i in range(3)]
for (ls, fl, st), y in zip(L, Ly): f.tbox(20, y, 300, 80, ls, 22, fl, st, first_bold=True)
f.arrow(170, Ly[0] + 80, 170, Ly[1], GRAY, 2.8); f.text(185, Ly[0] + 108, 'CPS1', 22, 400, 'start', GRAY)
f.arrow(170, Ly[1] + 80, 170, Ly[2], GRAY, 2.8); f.text(185, Ly[1] + 108, 'OTC (+오르니틴)', 22, 400, 'start', GRAY)
R = [(['시트룰린'], LBLUE, BLUE), (['아르기니노숙신산'], LBLUE, BLUE), (['아르기닌'], LBLUE, BLUE), (['요소 + 오르니틴'], LWARM, WARM)]
Ry = [310 + 125 * i for i in range(4)]
for (ls, fl, st), y in zip(R, Ry): f.tbox(480, y, 300, 80, ls, 22, fl, st, first_bold=True)
labs = ['ASS (+아스파르트산)', 'ASL (푸마르산 방출)', 'ARG1']
for i in range(3):
    f.arrow(630, Ry[i] + 80, 630, Ry[i + 1], GRAY, 2.8); f.text(615, Ry[i] + 108, labs[i], 22, 400, 'end', GRAY)
f.arrow(320, Ly[2] + 25, 480, Ry[0] + 25, GOLD, 2.8)
f.line(480, Ry[3] + 55, 400, Ry[3] + 55, GRAY, 2.5); f.line(400, Ry[3] + 55, 400, Ly[2] + 62, GRAY, 2.5); f.arrow(400, Ly[2] + 62, 320, Ly[2] + 62, GRAY, 2.5)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig9-1.svg'), write_to=os.path.join(o, '그림9-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림9-1.png')).convert('L').save(os.path.join(o, '그림9-1-흑백.png'))
