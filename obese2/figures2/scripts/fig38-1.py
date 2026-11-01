# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig38-1.svg', 400)
cols = [(20, 230, '메트포르민', LGREEN, GREEN, ['간', '포도당 생산 감소']),
        (305, 230, '인크레틴 계열', LWARM, WARM, ['췌장·뇌', '인슐린 증가, 식욕 감소']),
        (590, 190, 'SGLT2 억제제', LBLUE, BLUE, ['신장', '포도당 소변 배출'])]
for x, w, h, fill, st, body in cols:
    f.tbox(x, 20, w, 70, [h], 24, fill, st, True)
    f.tbox(x, 170, w, 90, [body[0]], 24, fill, st, True)
    f.tbox(x, 300, w, 90, body[1].split(' ', 1) if len(body[1].split(' ', 1)) > 1 else [body[1]], 22, 'white', st, False)
    f.arrow(x + w // 2, 90, x + w // 2, 170, INK, 3)
    f.arrow(x + w // 2, 260, x + w // 2, 300, INK, 3)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig38-1.svg'), write_to=os.path.join(o, '그림38-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림38-1.png')).convert('L').save(os.path.join(o, '그림38-1-흑백.png'))
