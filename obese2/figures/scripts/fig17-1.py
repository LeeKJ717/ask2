# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig17-1.svg', 560)
f.tbox(20, 10, 340, 100, ['뇌간 후구역과', '고립로핵의 GLP-1R'], 22, LBLUE, BLUE, first_bold=True)
f.tbox(440, 10, 340, 100, ['위장관: 위 배출 지연', '미주신경 신호'], 22, LGOLD, GOLD, first_bold=True)
f.arrow(190, 110, 330, 220, BLUE, 2.8); f.arrow(610, 110, 470, 220, GOLD, 2.8)
f.tbox(250, 220, 300, 110, ['오심, 구토', '포만 과다'], 22, LWARM, WARM, first_bold=True)
f.arrow(400, 330, 400, 410, GRAY, 2.8)
f.tbox(150, 410, 500, 120, ['완화 전략', '천천히 올리는 용량, 식사량 조절'], 22, LGREEN, GREEN, first_bold=True)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig17-1.svg'), write_to=os.path.join(o, '그림17-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림17-1.png')).convert('L').save(os.path.join(o, '그림17-1-흑백.png'))
