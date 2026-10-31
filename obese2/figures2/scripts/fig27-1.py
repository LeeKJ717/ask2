# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig27-1.svg', 480)
cols = [(20, 230), (305, 230), (590, 190)]
rows = [30, 180, 330]
def box(r, c, lines, fill, stroke, h=96):
    x, w = cols[c]; f.tbox(x, rows[r], w, h, lines, 24, fill, stroke, True)
box(0, 0, ['지방조직', '감소'], LBLUE, BLUE)
box(0, 1, ['렙틴', '감소'], LBLUE, BLUE)
box(0, 2, ['시상하부', '식욕 증가', '소비 감소'], LBLUE, BLUE, 110)
box(1, 0, ['유리지방산', '증가'], LWARM, WARM)
box(1, 1, ['간 PPARα', '활성'], LGREEN, GREEN)
box(1, 2, ['FGF21', '증가'], LGREEN, GREEN)
box(2, 0, ['혈당, 인슐린', '감소'], LGOLD, GOLD)
box(2, 1, ['췌장', '글루카곤 증가'], LGOLD, GOLD)
box(2, 2, ['간', '포도당 신생', '케톤 생성'], LGREEN, GREEN, 110)
for r in range(3):
    y = rows[r] + 48
    f.arrow(250, y, 305, y, INK, 3); f.arrow(535, y, 590, y, INK, 3)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig27-1.svg'), write_to=os.path.join(o, '그림27-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림27-1.png')).convert('L').save(os.path.join(o, '그림27-1-흑백.png'))
