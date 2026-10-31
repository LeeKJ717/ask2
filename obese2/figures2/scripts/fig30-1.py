# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig30-1.svg', 405)
X0, X1 = 20, 780
def row(y, label, segs):
    f.text(X0, y - 14, label, 24, 'bold', 'start')
    x = X0
    for w, t, fill, stroke in segs:
        f.tbox(x, y, w, 64, [t], 24, fill, stroke, False); x += w
row(60, '일반 식사 (자주 먹음)', [(560, '식후 상태', LBLUE, BLUE), (200, '공복', LWARM, WARM)])
row(190, '시간제한 식사', [(260, '식후 상태', LBLUE, BLUE), (500, '공복', LWARM, WARM)])
row(320, '장기 단식', [(120, '식후', LBLUE, BLUE), (220, '공복', LWARM, WARM), (420, '케톤 상태', LGREEN, GREEN)])
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig30-1.svg'), write_to=os.path.join(o, '그림30-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림30-1.png')).convert('L').save(os.path.join(o, '그림30-1-흑백.png'))
