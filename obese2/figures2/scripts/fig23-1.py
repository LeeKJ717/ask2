# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig23-1.svg', 520)
f.tbox(30, 40, 230, 76, ['젖산', '(근육, 적혈구)'], 24, LBLUE, BLUE, True)
f.tbox(30, 150, 230, 76, ['아미노산(알라닌)', '(근육 단백질)'], 24, LBLUE, BLUE, True)
f.tbox(30, 260, 230, 76, ['글리세롤', '(지방조직)'], 24, LBLUE, BLUE, True)
f.tbox(330, 150, 200, 100, ['간 포도당', '신생'], 24, LGREEN, GREEN, True)
f.tbox(330, 330, 200, 76, ['포도당 6-인산'], 24, '#F1F3F5', GRAY, False)
f.tbox(30, 420, 230, 76, ['간 글리코겐', '(분해)'], 24, LGOLD, GOLD, True)
f.tbox(590, 330, 180, 76, ['혈중 포도당'], 24, LWARM, WARM, True)
f.tbox(590, 150, 180, 76, ['글루카곤', '(자극)'], 24, LGOLD, GOLD, True)
f.tbox(590, 40, 180, 76, ['인슐린', '(억제)'], 24, LWARM, WARM, True)
for y in (78, 188, 298): f.arrow(260, y, 330, 200, INK, 3)
f.arrow(430, 250, 430, 330, INK, 3)
f.arrow(260, 458, 330, 380, INK, 3)
f.arrow(530, 368, 590, 368, INK, 3)
f.arrow(590, 188, 530, 200, GOLD, 3)
f.inhibit(590, 90, 531, 178, WARM, 3)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig23-1.svg'), write_to=os.path.join(o, '그림23-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림23-1.png')).convert('L').save(os.path.join(o, '그림23-1-흑백.png'))
