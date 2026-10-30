# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig17-2.svg', 600)
f.tbox(20, 10, 230, 100, ['약물 노출', '용량, 흡수, 순응도'], 22, LGOLD, GOLD, first_bold=True)
f.tbox(285, 10, 230, 100, ['수용체와 유전', 'GLP1R 변이 등'], 22, LBLUE, BLUE, first_bold=True)
f.tbox(550, 10, 230, 100, ['몸의 상태', '당뇨병, 간, 신장'], 22, LGREEN, GREEN, first_bold=True)
f.arrow(135, 110, 330, 260, GOLD, 2.8); f.arrow(400, 110, 400, 260, BLUE, 2.8); f.arrow(665, 110, 470, 260, GREEN, 2.8)
f.tbox(250, 260, 300, 110, ['개인별 반응', '체중, 부작용'], 22, LWARM, WARM, first_bold=True)
f.tbox(20, 480, 340, 100, ['행동과 식이', '식사량, 활동량'], 22, "#F1F3F5", GRAY, first_bold=True)
f.arrow(190, 480, 330, 370, GRAY, 2.8)
f.tbox(440, 480, 340, 100, ['치료 기간', '중단 후 재증가'], 22, "#F1F3F5", GRAY, first_bold=True)
f.arrow(610, 480, 470, 370, GRAY, 2.8)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig17-2.svg'), write_to=os.path.join(o, '그림17-2.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림17-2.png')).convert('L').save(os.path.join(o, '그림17-2-흑백.png'))
