# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig39-1.svg', 190)
TXT=[['반응 목록','네트워크'],['화학량론','행렬 S'],['제약과','목적함수'],['흐름 분포','S·v = 0']]
xs=[10,215,420,625]
fills=[(LBLUE,BLUE),(LGREEN,GREEN),(LGOLD,GOLD),(LWARM,WARM)]
for i,(x,t) in enumerate(zip(xs,TXT)):
    f.tbox(x,40,165,110,t,22,fills[i][0],fills[i][1],True)
    if i<3: f.arrow(x+165,95,xs[i+1],95,INK,3)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig39-1.svg'), write_to=os.path.join(o, '그림39-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림39-1.png')).convert('L').save(os.path.join(o, '그림39-1-흑백.png'))
