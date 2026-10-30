# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig2-1.svg', 420)
f.tbox(20, 120, 190, 150, ['아데닌', '(염기)'], 24, LGREEN, GREEN, first_bold=True)
f.tbox(240, 120, 150, 150, ['리보스', '(당)'], 24, LGOLD, GOLD, first_bold=True)
f.tbox(420, 120, 110, 150, ['Pα'], 26, LBLUE, BLUE, first_bold=True)
f.tbox(550, 120, 110, 150, ['Pβ'], 26, LBLUE, BLUE, first_bold=True)
f.tbox(680, 120, 100, 150, ['Pγ'], 26, LWARM, WARM, first_bold=True)
for x1, x2 in ((210, 240), (390, 420), (530, 550), (660, 680)):
    f.line(x1, 195, x2, 195, GRAY, 3)
f.text(205, 60, '아데노신', 26, 700, 'middle', INK)
f.line(20, 90, 390, 90, GRAY, 2)
f.text(600, 60, '3개의 인산기', 26, 700, 'middle', INK)
f.line(420, 90, 780, 90, GRAY, 2)
f.arrow(715, 275, 715, 345, WARM, 2.8)
f.text(715, 395, '말단 인산 가수분해 → ADP + 무기인산', 22, 400, 'end', WARM)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig2-1.svg'), write_to=os.path.join(o, '그림2-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림2-1.png')).convert('L').save(os.path.join(o, '그림2-1-흑백.png'))
