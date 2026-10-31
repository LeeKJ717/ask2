# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig26-1.svg', 510)
f.tbox(20, 40, 230, 76, ['근육 단백질', '(분해)'], 24, LBLUE, BLUE, True)
f.tbox(305, 40, 230, 76, ['알라닌', '글루타민'], 24, LBLUE, BLUE, True)
f.tbox(590, 40, 190, 110, ['간', '포도당 신생', '요소 회로'], 24, LGREEN, GREEN, True)
f.tbox(305, 250, 230, 76, ['요소', '(소변 배설)'], 24, '#F1F3F5', GRAY, True)
f.tbox(590, 250, 190, 76, ['혈중 포도당'], 24, LWARM, WARM, True)
f.tbox(20, 400, 230, 76, ['케톤체', '(단백질 절약)'], 24, LGREEN, GREEN, True)
f.arrow(250, 78, 305, 78, INK, 3)
f.arrow(535, 78, 590, 78, INK, 3)
f.arrow(685, 150, 685, 250, INK, 3)
f.arrow(610, 150, 535, 275, INK, 3)
f.inhibit(135, 400, 135, 117, GREEN, 3)
f.text(155, 270, '분해 억제', 24, 'normal', 'start', GREEN)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig26-1.svg'), write_to=os.path.join(o, '그림26-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림26-1.png')).convert('L').save(os.path.join(o, '그림26-1-흑백.png'))
