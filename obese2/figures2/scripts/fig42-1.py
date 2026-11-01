# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig42-1.svg', 400)
f.line(100,30,100,300,INK,3); f.line(100,300,770,300,INK,3)
pts=[]
for k in range(0,101):
    r=k/100*4.0; pts.append((100+k/100*660, 60+ (300-60-60)*( (r**4)/(1+r**4) )*1.0))
d='M '+' L '.join(f'{x:.1f} {y:.1f}' for x,y in pts)
f.path(d,BLUE,4)
f.text(120,40,'포도당 방출',22,'normal','start',GRAY)
f.text(765,278,'포도당 흡수',22,'normal','end',GRAY)
f.text(220,330,'공복',22,'normal','middle')
f.text(650,330,'식후',22,'normal','middle')
f.text(430,385,'인슐린/글루카곤 비',22,'normal','middle',GRAY)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig42-1.svg'), write_to=os.path.join(o, '그림42-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림42-1.png')).convert('L').save(os.path.join(o, '그림42-1-흑백.png'))
