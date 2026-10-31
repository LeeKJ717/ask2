# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig32-1.svg', 450)
f.tbox(20, 40, 230, 76, ['인슐린'], 24, LWARM, WARM, True)
f.tbox(20, 200, 230, 76, ['근육 수축', '(운동)'], 24, LGOLD, GOLD, True)
f.tbox(305, 40, 230, 76, ['IRS, PI3K', 'AKT'], 24, LBLUE, BLUE, True)
f.tbox(305, 200, 230, 76, ['AMPK', '칼슘 신호'], 24, LBLUE, BLUE, True)
f.tbox(590, 90, 190, 150, ['GLUT4', '세포막 이동', '포도당 흡수'], 24, LGREEN, GREEN, True)
f.tbox(590, 330, 190, 96, ['글리코겐', '저장, 산화'], 24, LWARM, WARM, True)
f.arrow(250, 78, 305, 78, INK, 3); f.arrow(250, 238, 305, 238, INK, 3)
f.arrow(535, 78, 590, 140, INK, 3); f.arrow(535, 238, 590, 190, INK, 3)
f.arrow(685, 240, 685, 330, INK, 3)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig32-1.svg'), write_to=os.path.join(o, '그림32-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림32-1.png')).convert('L').save(os.path.join(o, '그림32-1-흑백.png'))
