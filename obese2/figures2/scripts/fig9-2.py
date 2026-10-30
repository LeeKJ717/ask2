# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig9-2.svg', 720)
f.text(160, 28, '들어가는 곳', 22, 700, 'middle', INK); f.text(560, 28, '대표 아미노산', 22, 700, 'middle', INK)
rows = [('피루브산', ['알라닌, 세린, 시스테인', '글리신, 트레오닌'], LGREEN, GREEN),
        ('α-케토글루타르산', ['글루탐산, 글루타민, 프롤린', '아르기닌, 히스티딘'], LGREEN, GREEN),
        ('숙시닐-CoA', ['발린, 이소류신, 메티오닌', '트레오닌'], LGREEN, GREEN),
        ('푸마르산', ['페닐알라닌, 티로신'], LGREEN, GREEN),
        ('옥살로아세트산', ['아스파르트산, 아스파라긴'], LGREEN, GREEN),
        ('아세틸-CoA / 아세토아세틸-CoA', ['류신, 라이신', '(이소류신·페닐알라닌 등 일부)'], LWARM, WARM)]
y = 50
for nm, ls, fl, st in rows:
    h = 100
    f.tbox(20, y, 280, h, [nm] if len(nm) < 14 else ['아세틸-CoA /', '아세토아세틸-CoA'], 22, fl, st, first_bold=True)
    f.tbox(330, y, 450, h, ls, 22, fl, st)
    y += 110
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig9-2.svg'), write_to=os.path.join(o, '그림9-2.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림9-2.png')).convert('L').save(os.path.join(o, '그림9-2-흑백.png'))
