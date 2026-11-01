# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig40-1.svg', 400)
f.line(100,30,100,300,INK,3); f.line(100,300,770,300,INK,3)
f.line(100,40,770,40,GOLD,3,'10 8')
pts=[]
for k in range(0,81):
    S=k/10.0; pts.append((100+S/8*660, 300-260*S/(1+S)))
d='M '+' L '.join(f'{x:.1f} {y:.1f}' for x,y in pts)
f.path(d,BLUE,4)
f.line(100,170,182,170,GRAY,2,'6 6'); f.line(182,170,182,300,GRAY,2,'6 6')
f.text(770,24,'Vmax',22,'normal','end',GOLD)
f.text(108,160,'Vmax/2',22,'normal','start',GRAY)
f.text(182,330,'Km',22,'normal','middle',GRAY)
f.text(430,385,'기질 농도 [S]',22,'normal','middle',GRAY)
f.text(108,75,'속도 v',22,'normal','start',GRAY)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig40-1.svg'), write_to=os.path.join(o, '그림40-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림40-1.png')).convert('L').save(os.path.join(o, '그림40-1-흑백.png'))
