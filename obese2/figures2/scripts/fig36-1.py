# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig36-1.svg', 470)
f.tbox(20, 20, 230, 90, ['지방조직', '인슐린 저항'], 24, LGOLD, GOLD, True)
f.tbox(305, 20, 230, 90, ['지방산', '간으로 유입 증가'], 24, LGOLD, GOLD, True)
f.tbox(590, 20, 190, 90, ['고인슐린', '혈증'], 24, LWARM, WARM, True)
f.tbox(305, 190, 230, 90, ['간: 지방 합성', '계속 작동'], 24, LGREEN, GREEN, True)
f.tbox(590, 190, 190, 90, ['간: 포도당', '신생 억제 실패'], 24, LGREEN, GREEN, True)
f.tbox(305, 360, 230, 90, ['간에 지방 축적', '(지방간)'], 24, LBLUE, BLUE, True)
f.arrow(250, 65, 305, 65, INK, 3)
f.arrow(420, 110, 420, 190, INK, 3)
f.arrow(620, 110, 520, 190, INK, 3)
f.arrow(685, 110, 685, 190, INK, 3)
f.arrow(420, 280, 420, 360, INK, 3)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig36-1.svg'), write_to=os.path.join(o, '그림36-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림36-1.png')).convert('L').save(os.path.join(o, '그림36-1-흑백.png'))
