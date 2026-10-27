# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig15-2.svg', 700)
steps = [(['1. 수용체 활성', 'TMD 포켓에 결합해', 'Gs 신호를 켠다'], LBLUE, BLUE),
         (['2. 흡수', '위장관을 통과해', '혈액에 도달한다'], LGOLD, GOLD),
         (['3. 대사와 안전성', '간에서의 처리와', '간 독성 여부를 본다'], LWARM, WARM),
         (['4. 임상 효과', '체중 감소와', '내약성을 확인한다'], LGREEN, GREEN)]
y = 10
for i, (lines, fl, st) in enumerate(steps):
    f.tbox(150, y, 500, 140, lines, 22, fl, st, first_bold=True)
    if i < 3: f.arrow(400, y + 140, 400, y + 170, GRAY, 2.8)
    y += 170
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig15-2.svg'), write_to=os.path.join(o, '그림15-2.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림15-2.png')).convert('L').save(os.path.join(o, '그림15-2-흑백.png'))
