# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig16-1.svg', 620)
f.tbox(240, 10, 320, 90, ['식욕과 에너지 균형', '뇌(시상하부, 뇌간)'], 22, LBLUE, BLUE, first_bold=True)
f.tbox(20, 250, 230, 110, ['아밀린', '췌장 β세포에서 분비'], 22, LGOLD, GOLD, first_bold=True)
f.tbox(285, 250, 230, 110, ['PYY', '장 L세포에서 분비'], 22, LGREEN, GREEN, first_bold=True)
f.tbox(550, 250, 230, 110, ['GDF15', '스트레스 때 분비'], 22, LWARM, WARM, first_bold=True)
f.arrow(135, 250, 300, 100, GOLD, 2.8); f.arrow(400, 250, 400, 100, GREEN, 2.8); f.arrow(665, 250, 500, 100, WARM, 2.8)
f.tbox(20, 500, 760, 100, ['근육: 체중이 줄 때 제지방이 함께 줄어드는 문제', '(근육 보존 접근이 별도 표적)'], 22, "#F1F3F5", GRAY, first_bold=True)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig16-1.svg'), write_to=os.path.join(o, '그림16-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림16-1.png')).convert('L').save(os.path.join(o, '그림16-1-흑백.png'))
