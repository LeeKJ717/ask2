# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig34-1.svg', 440)
f.tbox(20, 40, 230, 76, ['포도당', '(GLUT2 유입)'], 24, LWARM, WARM, True)
f.tbox(305, 40, 230, 76, ['글루코키나아제', '(대사 시작)'], 24, LBLUE, BLUE, True)
f.tbox(590, 40, 190, 76, ['ATP/ADP', '증가'], 24, LBLUE, BLUE, True)
f.tbox(590, 190, 190, 76, ['KATP 채널', '닫힘'], 24, LGREEN, GREEN, True)
f.tbox(305, 190, 230, 76, ['탈분극', 'Ca2+ 유입'], 24, LGREEN, GREEN, True)
f.tbox(20, 190, 230, 76, ['인슐린', '분비'], 24, LWARM, WARM, True)
f.tbox(305, 340, 230, 76, ['GLP-1', 'cAMP 증폭'], 24, LGOLD, GOLD, True)
f.arrow(250, 78, 305, 78, INK, 3); f.arrow(535, 78, 590, 78, INK, 3)
f.arrow(685, 116, 685, 190, INK, 3)
f.arrow(590, 228, 535, 228, INK, 3); f.arrow(305, 228, 250, 228, INK, 3)
f.arrow(420, 340, 420, 266, GOLD, 3)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig34-1.svg'), write_to=os.path.join(o, '그림34-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림34-1.png')).convert('L').save(os.path.join(o, '그림34-1-흑백.png'))
