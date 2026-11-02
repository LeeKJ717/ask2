# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
AX=['① 유전학 근거','② 발현 위치','③ 구조 가용성','④ 안전성 신호','⑤ 경쟁 현황']
H=46; G=16; top=14
f = Fig('fig2-1.svg', top+5*H+4*G+20)
y=top; cy=[]
for a in AX:
    f.tbox(20,y,350,H,[a],24,LBLUE,BLUE,False)
    cy.append(y+H/2); y+=H+G
mid=top+(5*H+4*G)/2
f.tbox(450,mid-70,330,56,['종합 우선순위'],24,LGREEN,GREEN,True)
f.tbox(450,mid+20,330,56,['3장 검증 설계'],24,LGOLD,GOLD,True)
for c in cy:
    f.line(370,c,410,c,INK,2)
f.line(410,cy[0],410,cy[4],INK,2)
f.arrow(410,mid-42,450,mid-42,INK,2.5)
f.arrow(615,mid-14,615,mid+20,INK,2.5)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig2-1.svg'), write_to=os.path.join(o, '그림2-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림2-1.png')).convert('L').save(os.path.join(o, '그림2-1-흑백.png'))
