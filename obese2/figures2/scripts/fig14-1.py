# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig14-1.svg', 700)
f.tbox(30, 30, 340, 90, ['에너지 부족', '(AMP/ATP 비 상승)'], 24, LWARM, WARM, first_bold=True)
f.tbox(430, 30, 340, 90, ['영양 풍부', '(아미노산, 인슐린)'], 24, LGREEN, GREEN, first_bold=True)
f.tbox(30, 230, 340, 80, ['AMPK'], 24, LBLUE, BLUE, first_bold=True)
f.tbox(430, 230, 340, 80, ['mTORC1'], 24, LBLUE, BLUE, first_bold=True)
f.tbox(30, 450, 340, 100, ['이화 촉진', '(지방산 산화, 자가포식)'], 24, LGOLD, GOLD, first_bold=True)
f.tbox(430, 450, 340, 100, ['동화 촉진', '(단백질·지질 합성)'], 24, LGOLD, GOLD, first_bold=True)
f.arrow(200, 120, 200, 230, GRAY, 2.8)
f.arrow(600, 120, 600, 230, GRAY, 2.8)
f.inhibit(370, 270, 430, 270, WARM, 2.8)
f.arrow(200, 310, 200, 450, GRAY, 2.8)
f.arrow(600, 310, 600, 450, GRAY, 2.8)
f.inhibit(130, 310, 450, 450, WARM, 2.0) if False else None
f.text(400, 640, '막대 끝 선은 억제를 뜻한다', 22, 'normal', 'middle')
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig14-1.svg'), write_to=os.path.join(o, '그림14-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림14-1.png')).convert('L').save(os.path.join(o, '그림14-1-흑백.png'))
