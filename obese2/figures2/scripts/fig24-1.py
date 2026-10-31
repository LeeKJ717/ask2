# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig24-1.svg', 650)
cx, w = 400, 260
x = cx - w / 2
f.tbox(x, 30, w, 76, ['중성지방', '(지방방울)'], 24, LGOLD, GOLD, True)
f.tbox(x, 160, w, 76, ['디아실글리세롤'], 24, LGOLD, GOLD, False)
f.tbox(x, 290, w, 76, ['모노아실글리세롤'], 24, LGOLD, GOLD, False)
f.tbox(x, 420, w, 76, ['유리지방산', '+ 글리세롤'], 24, LWARM, WARM, True)
for y0, t in ((106, 'ATGL'), (236, 'HSL'), (366, 'MGL')):
    f.arrow(cx, y0, cx, y0 + 54, INK, 3)
    f.text(cx + 18, y0 + 36, t, 24, 'bold', 'start')
f.tbox(20, 550, 250, 76, ['유리지방산', '근육·간 β산화'], 24, LBLUE, BLUE, True)
f.tbox(530, 550, 250, 76, ['글리세롤', '간 포도당 신생'], 24, LGREEN, GREEN, True)
f.arrow(cx - 60, 496, 150, 550, INK, 3)
f.arrow(cx + 60, 496, 650, 550, INK, 3)
f.tbox(620, 30, 160, 76, ['인슐린', '(억제)'], 24, LWARM, WARM, True)
f.tbox(620, 150, 160, 110, ['카테콜아민', '글루카곤', '(자극)'], 24, LGOLD, GOLD, True)
f.inhibit(620, 68, 531, 68, WARM, 3)
f.arrow(620, 198, 531, 198, GOLD, 3)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig24-1.svg'), write_to=os.path.join(o, '그림24-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림24-1.png')).convert('L').save(os.path.join(o, '그림24-1-흑백.png'))
