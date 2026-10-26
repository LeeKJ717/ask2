# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig10-2.svg', 470)
rows = [(['췌도 조직'], LWARM, WARM), (['세포를 하나씩 분리'], LBLUE, BLUE),
        (['세포마다 mRNA 종류와 양을 읽음'], LGREEN, GREEN),
        (['비슷한 세포끼리 묶어 지도로 표시'], LGOLD, GOLD)]
for i, (t, fl, st) in enumerate(rows):
    y = 10 + i * 116
    f.tbox(110, y, 580, 76, t, 24, fl, st)
    if i: f.arrow(400, y - 40, 400, y, GRAY, 2.8)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig10-2.svg'), write_to=os.path.join(o, '그림10-2.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림10-2.png')).convert('L').save(os.path.join(o, '그림10-2-흑백.png'))
