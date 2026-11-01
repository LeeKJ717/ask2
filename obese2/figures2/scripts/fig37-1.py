# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig37-1.svg', 400)
f.line(90, 30, 90, 300, INK, 3); f.line(90, 300, 770, 300, INK, 3)
f.text(60, 175, '체중', 22, 'normal', 'end')
f.line(90, 90, 770, 90, GOLD, 3, '10 8')
f.text(770, 62, '설정점(개념)', 22, 'normal', 'end', GOLD)
f.path('M 90 90 L 230 90 C 280 90 300 250 370 250 L 450 250 C 520 250 560 100 690 90 L 770 90', BLUE, 4)
f.text(300, 328, '감량기', 22, 'normal', 'middle')
f.text(480, 328, '유지기', 22, 'normal', 'middle')
f.text(660, 328, '재증가', 22, 'normal', 'middle')
f.text(430, 380, '시간', 22, 'normal', 'middle', GRAY)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig37-1.svg'), write_to=os.path.join(o, '그림37-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림37-1.png')).convert('L').save(os.path.join(o, '그림37-1-흑백.png'))
