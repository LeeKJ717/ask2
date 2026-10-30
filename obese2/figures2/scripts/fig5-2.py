# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig5-2.svg', 470)
f.tbox(290, 10, 220, 80, ['피루브산'], 28, LBLUE, BLUE, first_bold=True)
items = [(10, ['젖산', 'LDH'], LWARM, WARM), (210, ['아세틸-CoA', 'PDH'], LGOLD, GOLD),
         (410, ['옥살로', '아세트산', 'PC'], LGREEN, GREEN), (610, ['알라닌', 'ALT'], LGRAY := '#F1F3F5', GRAY)]
for x, ls, fl, st in items:
    f.tbox(x, 270, 180, 130 if len(ls) == 3 else 110, ls, 22, fl, st, first_bold=True)
    f.arrow(400, 90, x + 90, 270, st, 2.8)
f.text(100, 440, '혐기·적혈구', 22, 400, 'middle', WARM)
f.text(300, 440, '호기·미토콘드리아', 22, 400, 'middle', GOLD)
f.text(520, 440, '보충·포도당 신생', 22, 400, 'middle', GREEN)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig5-2.svg'), write_to=os.path.join(o, '그림5-2.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림5-2.png')).convert('L').save(os.path.join(o, '그림5-2-흑백.png'))
