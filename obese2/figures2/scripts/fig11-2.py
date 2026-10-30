# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig11-2.svg', 640)
f.text(400, 30, '막간 공간 (양성자 많음)', 24, 700, 'middle', BLUE)
f.arrow(400, 50, 400, 150, BLUE, 3); f.text(430, 105, 'H+', 24, 700, 'start', BLUE)
f.rect(0, 150, 800, 120, LGOLD, GOLD, 2, 0)
f.tbox(210, 160, 380, 100, ['F0: c-고리와 a 소단위', '양성자가 지나가며 고리가 회전'], 22, LBLUE, BLUE, first_bold=True)
f.arrow(400, 270, 400, 310, GRAY, 2.8)
f.tbox(210, 310, 380, 90, ['F1: α3β3 머리', 'γ 축이 회전하며 β소단위를 누름'], 22, LGREEN, GREEN, first_bold=True)
st = [(20, ['느슨 (L)', 'ADP + Pi 결합']), (290, ['긴밀 (T)', 'ATP 합성']), (560, ['개방 (O)', 'ATP 방출'])]
for x, ls in st:
    f.tbox(x, 470, 220, 90, ls, 22, LGOLD, GOLD, first_bold=True)
f.arrow(240, 515, 290, 515, GOLD, 2.8); f.arrow(510, 515, 560, 515, GOLD, 2.8)
f.line(660, 470, 660, 440, GOLD, 2.8); f.line(660, 440, 130, 440, GOLD, 2.8); f.arrow(130, 440, 130, 470, GOLD, 2.8)
f.arrow(400, 400, 400, 440, GRAY, 2.8)
f.text(400, 620, '기질 (양성자 적음)', 24, 700, 'middle', BLUE)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig11-2.svg'), write_to=os.path.join(o, '그림11-2.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림11-2.png')).convert('L').save(os.path.join(o, '그림11-2-흑백.png'))
