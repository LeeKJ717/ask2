# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig33-1.svg', 415)
f.tbox(290, 30, 220, 76, ['지방세포'], 24, LGOLD, GOLD, True)
f.tbox(20, 180, 360, 210, ['저장고 기능', '식후: 지방 저장', '(LPL)', '공복: 지방 방출', '(ATGL, HSL)'], 24, LBLUE, BLUE, True)
f.tbox(420, 180, 360, 210, ['내분비 기능', '렙틴, 아디포넥틴', '염증 신호', '(TNF-α, IL-6)'], 24, LGREEN, GREEN, True)
f.arrow(350, 106, 200, 180, INK, 3)
f.arrow(450, 106, 600, 180, INK, 3)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig33-1.svg'), write_to=os.path.join(o, '그림33-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림33-1.png')).convert('L').save(os.path.join(o, '그림33-1-흑백.png'))
