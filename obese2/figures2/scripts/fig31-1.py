# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig31-1.svg', 460)
f.tbox(20, 90, 230, 120, ['식후 입력', '포도당, 아미노산', '(문맥, 장에서)'], 24, LBLUE, BLUE, True)
f.tbox(20, 250, 230, 120, ['공복 입력', '지방산, 젖산', '글리세롤, 아미노산'], 24, LWARM, WARM, True)
f.tbox(305, 40, 230, 376, ['간', '글리코겐 저장·분해', '지방 합성', '포도당 신생', 'β산화', '케톤 생성', '요소 회로'], 24, LGREEN, GREEN, True)
outs = [('포도당', '(혈당 공급)', LWARM, WARM), ('VLDL', '(지방 수출)', LGOLD, GOLD), ('케톤체', '(공복 연료)', LGREEN, GREEN), ('요소', '(질소 배설)', '#F1F3F5', GRAY)]
for i, (a, b, fl, st) in enumerate(outs):
    y = 40 + 100 * i
    f.tbox(590, y, 190, 76, [a, b], 24, fl, st, True)
    f.arrow(535, y + 38, 590, y + 38, INK, 3)
f.arrow(250, 150, 305, 150, INK, 3)
f.arrow(250, 310, 305, 310, INK, 3)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig31-1.svg'), write_to=os.path.join(o, '그림31-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림31-1.png')).convert('L').save(os.path.join(o, '그림31-1-흑백.png'))
