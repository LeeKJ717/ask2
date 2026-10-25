# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig8-2.svg', 500)
f.tbox(20, 10, 340, 80, ['AgRP/NPY 뉴런', '배고픔 쪽'], 22, LWARM, WARM)
f.tbox(440, 10, 340, 80, ['POMC/CART 뉴런', '포만 쪽'], 22, LBLUE, BLUE)
f.tbox(20, 180, 340, 70, ['AgRP(길항 펩타이드)'], 22, LWARM, WARM)
f.tbox(440, 180, 340, 70, ['α-MSH(작동 펩타이드)'], 22, LBLUE, BLUE)
f.arrow(190, 90, 190, 180, WARM, 2.8)
f.arrow(610, 90, 610, 180, BLUE, 2.8)
f.tbox(220, 380, 360, 100, ['MC4R 뉴런', 'Gs·cAMP 신호'], 22, LGREEN, GREEN, first_bold=True)
f.arrow(190, 250, 300, 380, WARM, 2.8)
f.arrow(610, 250, 500, 380, BLUE, 2.8)
f.text(170, 330, '차단', 24, 700, 'end', WARM)
f.text(630, 330, '활성', 24, 700, 'start', BLUE)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig8-2.svg'), write_to=os.path.join(o, '그림8-2.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림8-2.png')).convert('L').save(os.path.join(o, '그림8-2-흑백.png'))
