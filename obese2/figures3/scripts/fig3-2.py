# -*- coding: utf-8 -*-
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
D=json.load(open(os.path.join(here,'..','data','fig3-2-power.json')))
f = Fig('fig3-2.svg', 495)
X0,X1,Y0,Y1=140,760,400,30
f.line(X0,Y0,X1,Y0,INK,2.5); f.line(X0,Y0,X0,Y1,INK,2.5)
def px(n): return X0+(X1-X0-10)*(n-2)/38
def py(p): return Y0-(Y0-Y1)*p
for p in (0,0.5,1.0):
    f.text(X0-12,py(p)+8,('%g'%p),24,400,'end',GRAY)
for n in (10,20,30,40):
    f.text(px(n),Y0+32,str(n),24,400,'middle',GRAY)
f.line(X0,py(0.8),X1,py(0.8),GRAY,2,'8 6'); f.text(X0+12,py(0.8)-8,'0.8',24,700,'start',GRAY)
cols={'0.5':GOLD,'0.8':GREEN,'1.0':BLUE,'1.5':WARM}
for d,c in cols.items():
    f.poly([(px(n),py(p)) for n,p in zip(D['n'],D['curves'][d])],'none',c,4)
# 범례(오른쪽 아래)
lx=545; ly=285
for i,(d,c) in enumerate(cols.items()):
    f.line(lx,ly+i*34,lx+50,ly+i*34,c,4); f.text(lx+62,ly+i*34+8,'d = '+d,24,400,'start',INK)
f.text(430,Y0+66,'집단당 표본 수 n',24,400,'middle',INK)
f.text(52,215,'검정력',24,400,'middle',INK)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig3-2.svg'), write_to=os.path.join(o, '그림3-2.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림3-2.png')).convert('L').save(os.path.join(o, '그림3-2-흑백.png'))
