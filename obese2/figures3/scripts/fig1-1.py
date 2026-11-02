# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
STG=['표적 확인·검증','히트 발견','리드 최적화','전임상 시험','임상 1상 · 안전성','임상 2상 · 용량·신호','임상 3상 · 확증']
FL=[(LBLUE,BLUE),(LBLUE,BLUE),(LGREEN,GREEN),(LGREEN,GREEN),(LGOLD,GOLD),(LGOLD,GOLD),(LWARM,WARM)]
H=44; G=32; top=14
f = Fig('fig1-1.svg', top+7*H+6*G+20)
y=top
for i,s in enumerate(STG):
    w=700-i*60; x=400-w/2
    f.tbox(x,y,w,H,[s],24,FL[i][0],FL[i][1],True)
    if i<6:
        f.arrow(400,y+H,400,y+H+G,INK,2.5)
        f.text(415,y+H+G-6,'계속·중단 판정',22,'normal','start',GRAY)
    y+=H+G
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig1-1.svg'), write_to=os.path.join(o, '그림1-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림1-1.png')).convert('L').save(os.path.join(o, '그림1-1-흑백.png'))
