# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig8-1.svg', 720)
rows = [(['아세틸-CoA 2분자'], LGOLD, GOLD), (['아세토아세틸-CoA'], LGOLD, GOLD), (['HMG-CoA'], LWARM, WARM), (['아세토아세트산'], LWARM, WARM)]
ys = [30 + 125 * i for i in range(4)]
for (ls, fl, st), y in zip(rows, ys):
    f.tbox(60, y, 400, 80, ls, 24, fl, st, first_bold=True)
labs = ['티올레이스', 'HMG-CoA 합성효소 (HMGCS2)', 'HMG-CoA 분해효소']
for i in range(3):
    f.arrow(260, ys[i] + 80, 260, ys[i + 1], GRAY, 2.8)
    f.text(275, ys[i] + 108, labs[i], 22, 400, 'start', GRAY)
f.tbox(60, 555, 400, 80, ['β-하이드록시부티르산'], 24, LWARM, WARM, first_bold=True)
f.arrow(200, ys[3] + 80, 200, 555, WARM, 2.8); f.text(215, 540, '+NADH', 22, 400, 'start', GRAY)
f.tbox(540, ys[3], 200, 80, ['아세톤'], 24, '#F1F3F5', GRAY, first_bold=True)
f.arrow(460, ys[3] + 40, 540, ys[3] + 40, GRAY, 2.5)
f.text(260, 690, '간 미토콘드리아 기질에서 일어난다', 22, 400, 'middle', GRAY)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig8-1.svg'), write_to=os.path.join(o, '그림8-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림8-1.png')).convert('L').save(os.path.join(o, '그림8-1-흑백.png'))
