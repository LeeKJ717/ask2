# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig11-1.svg', 600)
f.text(400, 30, '막간 공간 (양성자 많음)', 24, 700, 'middle', BLUE)
f.rect(0, 190, 800, 260, LGOLD, GOLD, 2, 0)
f.text(400, 585, '기질 (양성자 적음)', 24, 700, 'middle', BLUE)
f.tbox(10, 205, 135, 80, ['복합체 I'], 22, LBLUE, BLUE, first_bold=True)
f.tbox(225, 205, 135, 80, ['복합체 III'], 22, LBLUE, BLUE, first_bold=True)
f.tbox(435, 205, 135, 80, ['복합체 IV'], 22, LBLUE, BLUE, first_bold=True)
f.tbox(125, 340, 140, 80, ['복합체 II'], 22, LGREEN, GREEN, first_bold=True)
f.circle(185, 245, 26, LWARM, WARM, 2); f.text(185, 253, 'Q', 24, 700, 'middle', WARM)
f.circle(395, 245, 24, LWARM, WARM, 2); f.text(395, 253, 'c', 24, 700, 'middle', WARM)
f.tbox(620, 205, 160, 215, ['ATP', '합성효소'], 24, LGREEN, GREEN, first_bold=True)
f.arrow(145, 245, 157, 245, WARM, 2.5); f.arrow(213, 245, 225, 245, WARM, 2.5)
f.arrow(360, 245, 369, 245, WARM, 2.5); f.arrow(419, 245, 435, 245, WARM, 2.5)
f.arrow(195, 340, 190, 272, GREEN, 2.5)
for x, t in ((78, '4 H+'), (292, '4 H+'), (502, '2 H+')):
    f.arrow(x, 205, x, 110, BLUE, 3); f.text(x, 95, t, 24, 700, 'middle', BLUE)
f.arrow(700, 110, 700, 205, GREEN, 3); f.text(700, 95, 'H+', 24, 700, 'middle', GREEN)
f.arrow(80, 505, 80, 285, GRAY, 2.5); f.text(80, 535, 'NADH', 22, 700, 'middle', GRAY)
f.arrow(195, 505, 195, 420, GRAY, 2.5); f.text(195, 535, '숙신산', 22, 700, 'middle', GRAY)
f.arrow(500, 505, 500, 285, GRAY, 2.5); f.text(500, 535, 'O2 → H2O', 22, 700, 'middle', GRAY)
f.arrow(700, 420, 700, 505, GREEN, 2.5); f.text(700, 535, 'ADP → ATP', 22, 700, 'middle', GREEN)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig11-1.svg'), write_to=os.path.join(o, '그림11-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림11-1.png')).convert('L').save(os.path.join(o, '그림11-1-흑백.png'))
