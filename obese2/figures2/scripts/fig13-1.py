# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig13-1.svg', 700)
f.tbox(40, 30, 330, 90, ['전자전달계', '(전자 누출)'], 24, LBLUE, BLUE, first_bold=True)
f.tbox(430, 30, 330, 90, ['산소 (O2)'], 24, LGRAY, GRAY, first_bold=True) if False else f.tbox(430, 30, 330, 90, ['산소 (O2)'], 24, '#F1F3F5', GRAY, first_bold=True)
f.tbox(235, 190, 330, 90, ['슈퍼옥사이드', '(O2-)'], 24, LWARM, WARM, first_bold=True)
f.tbox(235, 350, 330, 90, ['과산화수소', '(H2O2)'], 24, LWARM, WARM, first_bold=True)
f.tbox(40, 540, 330, 90, ['물 (H2O)'], 24, LGREEN, GREEN, first_bold=True)
f.tbox(430, 540, 330, 90, ['수산화 라디칼', '(OH)'], 24, LWARM, WARM, first_bold=True)
f.arrow(205, 120, 330, 190, GRAY, 2.8)
f.arrow(595, 120, 470, 190, GRAY, 2.8)
f.arrow(400, 280, 400, 350, GRAY, 2.8)
f.arrow(330, 440, 205, 540, GRAY, 2.8)
f.arrow(470, 440, 595, 540, GRAY, 2.8)
f.text(255, 318, 'SOD', 22, 'bold', 'end')
f.text(150, 495, '카탈레이스, GPx', 22, 'normal', 'middle')
f.text(655, 495, '철 이온 (Fenton)', 22, 'normal', 'middle')
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig13-1.svg'), write_to=os.path.join(o, '그림13-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림13-1.png')).convert('L').save(os.path.join(o, '그림13-1-흑백.png'))
