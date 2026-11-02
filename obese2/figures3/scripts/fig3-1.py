# -*- coding: utf-8 -*-
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig3-1.svg', 495)
X0,X1,Y0,Y1=140,770,400,30   # 축 영역(Y0 = 바닥)
f.line(X0,Y0,X1,Y0,INK,2.5); f.line(X0,Y0,X0,Y1,INK,2.5)
def curve(emax,ec,h=1.0):
    pts=[]
    for i in range(0,101):
        lx=-3+6*i/100            # log10 농도 -3..3 (상대 단위)
        r=emax/(1+10**((math.log10(ec)-lx)*h))
        pts.append((X0+20+(X1-X0-40)*i/100, Y0-(Y0-Y1-20)*r))
    return pts
f.poly(curve(1.0,1.0),'none',BLUE,4)
f.poly(curve(0.55,3.0),'none',WARM,4)
# 완전 작용제 EC50 표시
ex=X0+20+(X1-X0-40)*0.5
f.line(ex,Y0,ex,Y0-(Y0-Y1-20)*0.5,GRAY,2,'6 6'); f.line(X0,Y0-(Y0-Y1-20)*0.5,ex,Y0-(Y0-Y1-20)*0.5,GRAY,2,'6 6')
f.text(ex,Y0+34,'EC50',24,700,'middle',BLUE)
f.text(X0-12,Y0-(Y0-Y1-20)*0.5+8,'절반',24,400,'end',GRAY)
f.text(X0-12,Y1+36,'최대',24,400,'end',GRAY)
f.text(X0-12,Y0+6,'0',24,400,'end',GRAY)
f.text(450,Y0+66,'약물 농도 (로그 눈금)',24,400,'middle',INK)
f.text(300,70,'완전 작용제',24,700,'middle',BLUE)
f.text(690,150+130,'부분 작용제',24,700,'middle',WARM)
f.text(52,215,'반응',24,400,'middle',INK)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig3-1.svg'), write_to=os.path.join(o, '그림3-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림3-1.png')).convert('L').save(os.path.join(o, '그림3-1-흑백.png'))
