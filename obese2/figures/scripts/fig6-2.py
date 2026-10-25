# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig6-2.svg', 560)
rows = [(['균형', '작용제'], 5, 5), (['G단백질 편향', '작용제'], 7.5, 2), (['아레스틴 편향', '작용제'], 2, 7.5)]
for i, (name, a, b) in enumerate(rows):
    y = 10 + i * 180
    f.tbox(10, y + 20, 220, 90, name, 22, LGOLD, GOLD, first_bold=True)
    f.tbox(300, y + 20, 150, 90, ['수용체'], 24, LBLUE, BLUE, first_bold=True)
    f.arrow(230, y + 65, 300, y + 65, GOLD, 3)
    f.tbox(580, y, 210, 70, ['cAMP 신호'], 22, LGREEN, GREEN)
    f.tbox(580, y + 90, 210, 70, ['β-아레스틴 신호'], 22, LWARM, WARM)
    f.arrow(450, y + 50, 580, y + 35, GREEN, a)
    f.arrow(450, y + 80, 580, y + 125, WARM, b)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig6-2.svg'), write_to=os.path.join(o, '그림6-2.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림6-2.png')).convert('L').save(os.path.join(o, '그림6-2-흑백.png'))
