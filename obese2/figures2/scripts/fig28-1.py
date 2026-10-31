# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig28-1.svg', 420)
f.tbox(20, 100, 230, 76, ['AMP/ATP 비', '증가'], 24, LWARM, WARM, True)
f.tbox(305, 100, 230, 76, ['AMPK', '활성'], 24, LBLUE, BLUE, True)
f.tbox(20, 310, 230, 76, ['NAD+', '증가'], 24, LWARM, WARM, True)
f.tbox(305, 310, 230, 76, ['SIRT1', '활성'], 24, LBLUE, BLUE, True)
f.tbox(590, 30, 190, 76, ['오토파지', '(ULK1)'], 24, LGREEN, GREEN, True)
f.tbox(590, 170, 190, 76, ['mTORC1', '억제'], 24, LGOLD, GOLD, True)
f.tbox(590, 310, 190, 76, ['미토콘드리아', '생합성'], 24, LGREEN, GREEN, True)
f.arrow(250, 138, 305, 138, INK, 3)
f.arrow(250, 348, 305, 348, INK, 3)
f.arrow(535, 125, 590, 68, INK, 3)
f.inhibit(535, 150, 590, 208, GOLD, 3)
f.arrow(535, 348, 590, 348, INK, 3)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig28-1.svg'), write_to=os.path.join(o, '그림28-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림28-1.png')).convert('L').save(os.path.join(o, '그림28-1-흑백.png'))
