# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig3-1.svg', 640)
f.text(400, 30, '표준 환원 전위 E°′ (V)', 24, 700, 'middle', INK)
rows = [("NAD+ / NADH", "−0.32", LWARM, WARM), ("피루브산 / 젖산", "−0.19", LWARM, WARM),
        ("푸마르산 / 숙신산", "+0.03", LGOLD, GOLD), ("유비퀴논 / 유비퀴놀", "+0.05", LGOLD, GOLD),
        ("시토크롬 c (Fe3+ / Fe2+)", "+0.22", LGREEN, GREEN), ("O2 / H2O", "+0.82", LBLUE, BLUE)]
y = 55
for nm, v, fl, st in rows:
    f.tbox(30, y, 520, 80, [nm], 24, fl, st)
    f.tbox(580, y, 190, 80, [v], 26, fl, st, first_bold=True)
    y += 92
f.arrow(15, 70, 15, 590, GRAY, 2.5)
f.text(40, 625, '전자를 주려는 경향 큼', 22, 400, 'start', GRAY)
f.text(770, 625, '전자를 받으려는 경향 큼', 22, 400, 'end', GRAY)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig3-1.svg'), write_to=os.path.join(o, '그림3-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림3-1.png')).convert('L').save(os.path.join(o, '그림3-1-흑백.png'))
