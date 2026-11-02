# -*- coding: utf-8 -*-
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
import cairosvg
from PIL import Image
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg"); O = os.path.join(here, '..', 'out'); DD=os.path.join(here,'..','data')
def fin(f, num):
    print(f.save(OUT)); F.report()
    cairosvg.svg2png(url=os.path.join(OUT, f'fig{num}.svg'), write_to=os.path.join(O, f'그림{num}.png'), output_width=2079, background_color='white')
    Image.open(os.path.join(O, f'그림{num}.png')).convert('L').save(os.path.join(O, f'그림{num}-흑백.png'))
# 10-1 경로 모델 개략: 리간드 → 수용체 → Gs → cAMP → PKA, 아래 분기 β-아레스틴
f=Fig('fig10-1.svg',290)
xs=[20,175,330,485,640]; labs=[['리간드'],['GLP1R'],['Gs'],['cAMP'],['PKA']]
for i,(x,l) in enumerate(zip(xs,labs)):
    f.tbox(x,40,140,56,l,24,LBLUE if i<2 else LGREEN,BLUE if i<2 else GREEN,True)
    if i<4: f.arrow(x+140,68,xs[i+1],68,INK,2.5)
f.tbox(175,200,140,56,['β-아레스틴'],22,LGOLD,GOLD,True)
f.arrow(245,96,245,200,INK,2.5)
f.text(260,160,'결합 수용체',22,400,'start',GRAY)
fin(f,'10-1')
# 10-2 용량-반응 적합 곡선: 위 cAMP, 아래 β-아레스틴
R=json.load(open(os.path.join(DD,'fig10-2-fit.json')))['fits']
import math
f=Fig('fig10-2.svg',700)
X0,X1=130,770
def panel(y0,y1,path,title):
    f.line(X0,y1,X1,y1,INK,2.5); f.line(X0,y0,X0,y1,INK,2.5)
    f.text(X0+10,y0+4,title,24,700,'start',INK)
    for lig,col,dash in (('ref',BLUE,None),('test',WARM,'10 6')):
        em,le=R[f'{lig}-{path}']
        pts=[]
        for i in range(61):
            x=-12+6*i/60; y=em/(1+10**(le-x))
            pts.append((X0+20+(X1-X0-40)*i/60, y1-(y1-y0-40)*y))
        f.poly(pts,'none',col,4)
    f.text(X0-12,y1+8,'0',22,400,'end',GRAY); f.text(X0-12,y0+60,'1',22,400,'end',GRAY)
panel(30,300,'cAMP','cAMP 반응')
panel(370,640,'arr','β-아레스틴 반응')
f.text(450,688,'리간드 농도 (로그 눈금)',24,400,'middle',INK)
f.line(560,225,610,225,BLUE,4); f.text(620,233,'기준',22,400,'start',INK)
f.line(560,261,610,261,WARM,4); f.text(620,269,'시험',22,400,'start',INK)
fin(f,'10-2')
