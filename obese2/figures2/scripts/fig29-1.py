# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig29-1.svg', 610)
x0, x1, yb, yt = 90, 770, 400, 90
f.line(x0, yb, x1, yb, INK, 2.5); f.line(x0, yb, x0, yt, INK, 2.5)
xa, xb = 250, 610
for x, t in ((xa, '공복'), (xb, '식후')):
    f.line(x, yb, x, yb + 10, INK, 2); f.text(x, yb + 38, t, 22, 'normal', 'middle')
f.text(55, 215, '포도당', 22, 'normal', 'middle'); f.text(55, 245, '산화', 22, 'normal', 'middle'); f.text(55, 275, '비중', 22, 'normal', 'middle')
f.line(xa, 340, xb, 130, BLUE, 5)
f.line(xa, 270, xb, 215, WARM, 5)
f.line(xa, yb, xa, 100, GRAY, 2, '8 6'); f.line(xb, yb, xb, 100, GRAY, 2, '8 6')
ly = [490, 540]
f.line(100, ly[0], 160, ly[0], BLUE, 5); f.text(175, ly[0] + 9, '대사 유연성이 있는 경우', 24, 'normal', 'start')
f.line(100, ly[1], 160, ly[1], WARM, 5); f.text(175, ly[1] + 9, '유연성이 줄어든 경우 (인슐린 저항)', 24, 'normal', 'start')
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig29-1.svg'), write_to=os.path.join(o, '그림29-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림29-1.png')).convert('L').save(os.path.join(o, '그림29-1-흑백.png'))
