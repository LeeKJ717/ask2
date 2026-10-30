# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig10-1.svg', 790)
rows = [(['개체'], LBLUE, BLUE), (['조직·기관', '(근육, 간, 지방조직)'], LBLUE, BLUE), (['세포'], LGREEN, GREEN),
        (['미토콘드리아'], LGOLD, GOLD), (['내막의 크리스타'], LGOLD, GOLD), (['전자전달계 복합체 I~IV', 'ATP 합성효소'], LWARM, WARM)]
ys = [20 + 125 * i for i in range(6)]
for (ls, fl, st), y in zip(rows, ys):
    f.tbox(150, y, 500, 90, ls, 24, fl, st, first_bold=True)
for i in range(5):
    f.arrow(400, ys[i] + 90, 400, ys[i + 1], GRAY, 2.8)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig10-1.svg'), write_to=os.path.join(o, '그림10-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림10-1.png')).convert('L').save(os.path.join(o, '그림10-1-흑백.png'))
