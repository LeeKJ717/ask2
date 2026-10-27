# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig15-1.svg', 560)
f.tbox(20, 10, 340, 90, ['펩타이드 작용제', '큰 분자, 넓은 결합면'], 22, LGOLD, GOLD, first_bold=True)
f.tbox(440, 10, 340, 90, ['소분자 작용제', '작은 분자, 안쪽 포켓'], 22, LGREEN, GREEN, first_bold=True)
f.arrow(190, 100, 190, 200, GOLD, 2.8); f.arrow(610, 100, 610, 200, GREEN, 2.8)
f.tbox(20, 200, 340, 130, ['위장관에서 분해', '주사 또는 흡수 촉진제', '필요'], 22, LWARM, WARM, first_bold=True)
f.tbox(440, 200, 340, 130, ['알약으로 복용', '음식 제한 적음', '(약물에 따라 다름)'], 22, LGREEN, GREEN, first_bold=True)
f.arrow(190, 330, 190, 430, GOLD, 2.8); f.arrow(610, 330, 610, 430, GREEN, 2.8)
f.tbox(20, 430, 340, 110, ['제조 단가가 높고', '냉장 보관이 필요'], 22, LGOLD, GOLD, first_bold=True)
f.tbox(440, 430, 340, 110, ['대량 합성이 쉽고', '간 안전성 확인 필요'], 22, LGREEN, GREEN, first_bold=True)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig15-1.svg'), write_to=os.path.join(o, '그림15-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림15-1.png')).convert('L').save(os.path.join(o, '그림15-1-흑백.png'))
