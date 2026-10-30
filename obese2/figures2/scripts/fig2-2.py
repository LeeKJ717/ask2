# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig2-2.svg', 520)
f.tbox(40, 190, 220, 120, ['ATP'], 30, LWARM, WARM, first_bold=True)
f.tbox(540, 190, 220, 120, ['ADP + 인산'], 26, LBLUE, BLUE, first_bold=True)
f.arrow(260, 225, 540, 225, WARM, 3)
f.arrow(540, 275, 260, 275, GREEN, 3)
f.text(400, 190, '일 (수축·수송·합성)', 22, 400, 'middle', WARM)
f.text(400, 335, '산화적 인산화·해당', 22, 400, 'middle', GREEN)
f.tbox(40, 20, 220, 90, ['소비 경로'], 24, '#F1F3F5', GRAY)
f.tbox(540, 20, 220, 90, ['생산 경로'], 24, '#F1F3F5', GRAY)
f.arrow(150, 110, 150, 190, GRAY, 2.5); f.arrow(650, 190, 650, 110, GRAY, 2.5)
f.tbox(200, 410, 400, 90, ['AMP는 아데닐산 키네이스로', '2 ADP ⇌ ATP + AMP'], 22, LGOLD, GOLD)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig2-2.svg'), write_to=os.path.join(o, '그림2-2.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림2-2.png')).convert('L').save(os.path.join(o, '그림2-2-흑백.png'))
