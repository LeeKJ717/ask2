# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig2-2.svg', 600)
def flow(y0,title,steps,fl,st,endfl,endst):
    f.text(400,y0,title,24,700)
    y=y0+16; H=44; G=20
    for i,s in enumerate(steps):
        last = i==len(steps)-1
        f.tbox(150,y,500,H,[s],24,endfl if last else fl,endst if last else st,last)
        if not last: f.arrow(400,y+H,400,y+H+G,INK,2)
        y+=H+G
flow(28,'단일세포 자료 → 발현 위치',['자료 내려받기','품질 관리·정규화','군집·세포 유형 지정','표적 발현 확인'],LBLUE,BLUE,LGREEN,GREEN)
flow(340,'요약 통계 → 유전학 근거',['노출·결과 자료 조화','멘델 무작위화','공동 국소화','유전학 근거 칸'],LBLUE,BLUE,LGOLD,GOLD)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig2-2.svg'), write_to=os.path.join(o, '그림2-2.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림2-2.png')).convert('L').save(os.path.join(o, '그림2-2-흑백.png'))
