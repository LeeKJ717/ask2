# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
LGRAY2 = '#F1F3F5'
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig12-1.svg', 660)
f.text(400, 40, '미토콘드리아 내막', 24, 'bold', 'middle')
f.tbox(230, 70, 340, 90, ['전자전달계', '(복합체 I, III, IV)'], 24, LBLUE, BLUE, first_bold=True)
f.tbox(230, 230, 340, 70, ['양성자 구배'], 24, LGRAY2, GRAY, first_bold=True)
f.tbox(40, 370, 330, 90, ['UCP1', '(탈공역 단백질 1)'], 24, LWARM, WARM, first_bold=True)
f.tbox(430, 370, 330, 90, ['ATP 합성효소'], 24, LGREEN, GREEN, first_bold=True)
f.tbox(40, 560, 330, 70, ['열 방출'], 24, LGOLD, GOLD, first_bold=True)
f.tbox(430, 560, 330, 70, ['ATP 생산'], 24, LGOLD, GOLD, first_bold=True)
f.arrow(400, 160, 400, 230, GRAY, 2.8)
f.arrow(330, 300, 205, 370, GRAY, 2.8)
f.arrow(470, 300, 595, 370, GRAY, 2.8)
f.arrow(205, 460, 205, 560, GRAY, 2.8)
f.arrow(595, 460, 595, 560, GRAY, 2.8)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig12-1.svg'), write_to=os.path.join(o, '그림12-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림12-1.png')).convert('L').save(os.path.join(o, '그림12-1-흑백.png'))
