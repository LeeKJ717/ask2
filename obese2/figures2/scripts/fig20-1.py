# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig20-1.svg', 560)
f.tbox(250, 20, 300, 80, ['섭취한 에너지'], 24, '#F1F3F5', GRAY, first_bold=True)
f.tbox(15, 230, 250, 110, ['저장', '(글리코겐, 지방)'], 22, LGOLD, GOLD, first_bold=True)
f.tbox(275, 230, 250, 110, ['식이유발열', '(소화·흡수·대사 비용)'], 22, LWARM, WARM, first_bold=True)
f.tbox(535, 230, 250, 110, ['기타 소비', '(기초대사, 활동)'], 22, LBLUE, BLUE, first_bold=True)
f.arrow(330, 100, 140, 230, GRAY, 2.8)
f.arrow(400, 100, 400, 230, GRAY, 2.8)
f.arrow(470, 100, 660, 230, GRAY, 2.8)
f.tbox(235, 430, 330, 90, ['열로 방출', '(체온 유지에 기여)'], 22, LWARM, WARM, first_bold=True)
f.arrow(400, 340, 400, 430, GRAY, 2.8)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig20-1.svg'), write_to=os.path.join(o, '그림20-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림20-1.png')).convert('L').save(os.path.join(o, '그림20-1-흑백.png'))
