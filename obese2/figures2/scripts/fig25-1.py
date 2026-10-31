# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig25-1.svg', 540)
f.tbox(590, 20, 190, 76, ['인슐린 낮음', '글루카곤 높음'], 24, LGOLD, GOLD, True)
f.tbox(20, 140, 230, 76, ['유리지방산', '(간세포)'], 24, LWARM, WARM, True)
f.tbox(305, 140, 230, 76, ['아세틸-CoA', '(β산화)'], 24, LGREEN, GREEN, True)
f.tbox(590, 140, 190, 76, ['HMG-CoA', '(HMGCS2)'], 24, LGREEN, GREEN, True)
f.tbox(590, 290, 190, 140, ['케톤체', '아세토아세트산', 'β-하이드록시', '부티르산'], 24, LGREEN, GREEN, True)
f.tbox(305, 300, 230, 76, ['혈액뇌장벽', 'MCT1 수송'], 24, '#F1F3F5', GRAY, True)
f.tbox(20, 300, 230, 76, ['뇌 신경세포', '(OXCT1)'], 24, LBLUE, BLUE, True)
f.tbox(20, 440, 230, 76, ['TCA 회로', 'ATP 생산'], 24, LBLUE, BLUE, True)
f.arrow(685, 96, 685, 140, GOLD, 3)
f.arrow(250, 178, 305, 178, INK, 3)
f.arrow(535, 178, 590, 178, INK, 3)
f.arrow(685, 216, 685, 290, INK, 3)
f.arrow(590, 338, 535, 338, INK, 3)
f.arrow(305, 338, 250, 338, INK, 3)
f.arrow(135, 376, 135, 440, INK, 3)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig25-1.svg'), write_to=os.path.join(o, '그림25-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림25-1.png')).convert('L').save(os.path.join(o, '그림25-1-흑백.png'))
