# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig15-1.svg', 640)
f.tbox(235, 20, 330, 70, ['혈중 포도당·영양 상태'], 24, '#F1F3F5', GRAY, first_bold=True)
f.tbox(30, 190, 340, 120, ['식후 호르몬', '인슐린, 인크레틴', '(GLP-1, GIP)'], 24, LGREEN, GREEN, first_bold=True)
f.tbox(430, 190, 340, 150, ['공복·스트레스 호르몬', '글루카곤, 코르티솔,', '성장호르몬, 카테콜아민'], 24, LWARM, WARM, first_bold=True)
f.tbox(30, 480, 340, 100, ['저장', '(글리코겐, 지방, 단백질)'], 24, LGOLD, GOLD, first_bold=True)
f.tbox(430, 480, 340, 100, ['동원', '(포도당, 지방산, 케톤체)'], 24, LGOLD, GOLD, first_bold=True)
f.arrow(330, 90, 200, 190, GRAY, 2.8)
f.arrow(470, 90, 600, 190, GRAY, 2.8)
f.arrow(200, 310, 200, 480, GRAY, 2.8)
f.arrow(600, 340, 600, 480, GRAY, 2.8)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig15-1.svg'), write_to=os.path.join(o, '그림15-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림15-1.png')).convert('L').save(os.path.join(o, '그림15-1-흑백.png'))
