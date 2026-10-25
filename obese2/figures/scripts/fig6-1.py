# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD, LGRAY
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig6-1.svg', 660)
f.tbox(290, 10, 220, 70, ['펩타이드 작용제', '(세포 밖)'], 22, LGOLD, GOLD, first_bold=True)
f.rect(10, 150, 780, 54, LGRAY, GRAY, 2, 10)
f.text(120, 186, '세포막', 24, 700, color=GRAY)
f.tbox(290, 130, 220, 94, ['B군 수용체', '(GLP1R 등)'], 24, LBLUE, BLUE, first_bold=True)
f.arrow(400, 80, 400, 130, GOLD, 3)
f.text(130, 262, '① G단백질 경로', 24, 700); f.text(670, 262, '② 아레스틴 경로', 24, 700)
# 왼쪽 사슬
L = [('Gs 단백질', LBLUE, BLUE), ('아데닐릴 고리화효소', LBLUE, BLUE), ('cAMP 증가', LGREEN, GREEN), ('PKA·EPAC2', LGREEN, GREEN)]
y = 280
for i, (t, fl, st) in enumerate(L):
    f.tbox(20, y, 220, 64, [t], 22, fl, st)
    if i: f.arrow(130, y - 22, 130, y, st, 2.8)
    y += 86
f.arrow(340, 224, 200, 280, BLUE, 2.8)
# 오른쪽 사슬
R = [('GRK 인산화', LWARM, WARM), ('β-아레스틴 결합', LWARM, WARM), ('내재화(엔도솜)', LGOLD, GOLD), ('재순환 또는 분해', LGOLD, GOLD)]
y = 280
for i, (t, fl, st) in enumerate(R):
    f.tbox(560, y, 220, 64, [t], 22, fl, st)
    if i: f.arrow(670, y - 22, 670, y, st, 2.8)
    y += 86
f.arrow(460, 224, 600, 280, WARM, 2.8)
f.tbox(290, 440, 220, 100, ['엔도솜에서도', 'cAMP 신호 가능'], 22, LGRAY, GRAY, dash='8 5')
f.arrow(560, 450, 510, 480, GRAY, 2.5, dash='8 5')
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig6-1.svg'), write_to=os.path.join(o, '그림6-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림6-1.png')).convert('L').save(os.path.join(o, '그림6-1-흑백.png'))
