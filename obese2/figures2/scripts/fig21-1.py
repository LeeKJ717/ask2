# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig21-1.svg', 760)
bx = [(['만성적 과영양'], '#F1F3F5', GRAY),
      (['피하지방 저장 한계'], LGOLD, GOLD),
      (['이소성 지방 축적', '(간, 근육, 췌장)'], LWARM, WARM),
      (['인슐린 신호 약화', '(DAG, 세라마이드 등)'], LWARM, WARM),
      (['식후 고혈당, 고지혈증'], LBLUE, BLUE)]
ys = [20, 170, 320, 470, 620]
for (ls, fl, st), y in zip(bx, ys):
    f.tbox(200, y, 400, 90 if len(ls) > 1 else 80, ls, 24, fl, st, first_bold=True)
for i in range(4):
    f.arrow(400, ys[i] + (90 if len(bx[i][0]) > 1 else 80), 400, ys[i + 1], GRAY, 2.8)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig21-1.svg'), write_to=os.path.join(o, '그림21-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림21-1.png')).convert('L').save(os.path.join(o, '그림21-1-흑백.png'))
