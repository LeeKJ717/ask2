# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig12-1.svg', 560)
f.tbox(20, 10, 760, 80, ['GLP-1 펩타이드 사슬', 'N 말단(수용체 안으로 들어가는 쪽) ~ C 말단'], 22, LBLUE, BLUE, first_bold=True)
cols = [(20, ['8번 자리', '알라닌을 Aib로 치환'], ['DPP-4 효소가', '자르지 못함'], LWARM, WARM),
        (285, ['26번 라이신', '지방산 측쇄를 붙임'], ['알부민에 붙어', '오래 순환'], LGOLD, GOLD),
        (550, ['34번 자리', '라이신→아르기닌'], ['지방산이 붙는', '자리를 하나로 정함'], LGREEN, GREEN)]
for x, a, b, fl, st in cols:
    f.arrow(x + 115, 90, x + 115, 190, st, 2.8)
    f.tbox(x, 190, 230, 110, a, 22, fl, st, first_bold=True)
    f.arrow(x + 115, 300, x + 115, 400, st, 2.8)
    f.tbox(x, 400, 230, 110, b, 22, fl, st)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig12-1.svg'), write_to=os.path.join(o, '그림12-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림12-1.png')).convert('L').save(os.path.join(o, '그림12-1-흑백.png'))
