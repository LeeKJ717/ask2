# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig9-2.svg', 520)
f.tbox(250, 10, 300, 80, ['소포체 스트레스', '잘못 접힌 단백질 증가'], 22, LWARM, WARM, first_bold=True)
for x, t in [(20, 'PERK'), (285, 'IRE1'), (550, 'ATF6')]:
    f.tbox(x, 180, 230, 80, [t], 24, LBLUE, BLUE, first_bold=True)
    f.arrow(400, 90, x + 115, 180, GRAY, 2.8)
    f.arrow(x + 115, 260, 205, 370, GREEN, 2.8)
f.tbox(40, 370, 330, 110, ['초기: 적응 반응', '합성 감소·샤페론 증가'], 22, LGREEN, GREEN, first_bold=True)
f.tbox(450, 370, 330, 110, ['오래 지속되면', '세포 사멸 신호'], 22, LWARM, WARM, first_bold=True)
f.arrow(370, 425, 450, 425, WARM, 3)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig9-2.svg'), write_to=os.path.join(o, '그림9-2.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림9-2.png')).convert('L').save(os.path.join(o, '그림9-2-흑백.png'))
