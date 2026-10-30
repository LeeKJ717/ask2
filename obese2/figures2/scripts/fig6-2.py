# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig6-2.svg', 480)
f.text(135, 28, '보충 반응', 24, 700, 'middle', GREEN); f.text(665, 28, '빠져나가는 분기', 24, 700, 'middle', WARM)
f.tbox(20, 100, 230, 100, ['피루브산', '→ 옥살로아세트산'], 22, LGREEN, GREEN, first_bold=True)
f.tbox(20, 270, 230, 100, ['아미노산', '→ α-케토글루타르산'], 22, LGREEN, GREEN, first_bold=True)
f.tbox(300, 165, 200, 120, ['TCA 회로'], 28, LGOLD, GOLD, first_bold=True)
f.arrow(250, 150, 300, 200, GREEN, 2.8); f.arrow(250, 320, 300, 250, GREEN, 2.8)
rb = [['시트르산', '→ 지방산 합성'], ['α-케토글루타르산', '→ 글루탐산'], ['숙시닐-CoA', '→ 헴 합성'], ['옥살로아세트산', '→ 포도당 신생']]
for i, ls in enumerate(rb):
    y = 45 + 105 * i
    f.tbox(550, y, 230, 90, ls, 22, LWARM, WARM, first_bold=True)
    f.arrow(500, 225, 550, y + 45, WARM, 2.8)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig6-2.svg'), write_to=os.path.join(o, '그림6-2.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림6-2.png')).convert('L').save(os.path.join(o, '그림6-2-흑백.png'))
