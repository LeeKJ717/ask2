# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig18-1.svg', 620)
f.tbox(250, 20, 300, 80, ['식후 영양소', '(인슐린 상승)'], 24, '#F1F3F5', GRAY, first_bold=True)
f.tbox(15, 250, 250, 170, ['간', '포도당 흡수', '글리코겐 합성', '새 지방 합성'], 22, LGREEN, GREEN, first_bold=True)
f.tbox(275, 250, 250, 170, ['근육', 'GLUT4 포도당 흡수', '글리코겐 합성', '아미노산 단백질 합성'], 22, LBLUE, BLUE, first_bold=True)
f.tbox(535, 250, 250, 170, ['지방조직', 'GLUT4 포도당 흡수', 'LPL로 지방산 흡수', '중성지방 저장'], 22, LGOLD, GOLD, first_bold=True)
f.arrow(330, 100, 140, 250, GRAY, 2.8)
f.arrow(400, 100, 400, 250, GRAY, 2.8)
f.arrow(470, 100, 660, 250, GRAY, 2.8)
f.tbox(15, 500, 250, 90, ['VLDL 분비', '(간에서 혈액으로)'], 22, LWARM, WARM, first_bold=True)
f.arrow(140, 420, 140, 500, GRAY, 2.8)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig18-1.svg'), write_to=os.path.join(o, '그림18-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림18-1.png')).convert('L').save(os.path.join(o, '그림18-1-흑백.png'))
