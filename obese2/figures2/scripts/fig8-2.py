# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig8-2.svg', 480)
f.tbox(20, 20, 330, 90, ['간', '케톤체 생성'], 22, LWARM, WARM, first_bold=True)
f.tbox(450, 20, 330, 90, ['혈액', 'β-하이드록시부티르산 등'], 22, '#F1F3F5', GRAY, first_bold=True)
f.arrow(350, 65, 450, 65, WARM, 2.8)
f.tbox(450, 190, 330, 100, ['뇌·근육·심장', '(말초 조직)'], 22, LBLUE, BLUE, first_bold=True)
f.arrow(615, 110, 615, 190, GRAY, 2.8)
f.tbox(20, 190, 330, 100, ['아세토아세틸-CoA', 'SCOT 반응'], 22, LGOLD, GOLD, first_bold=True)
f.arrow(450, 240, 350, 240, GOLD, 2.8)
f.tbox(20, 360, 330, 90, ['아세틸-CoA 2분자', '→ TCA 회로'], 22, LGREEN, GREEN, first_bold=True)
f.arrow(185, 290, 185, 360, GREEN, 2.8)
f.text(600, 360, '간에는 SCOT가 없어', 22, 400, 'middle', WARM)
f.text(600, 392, '자기가 만든 케톤을 쓰지 못한다', 22, 400, 'middle', WARM)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig8-2.svg'), write_to=os.path.join(o, '그림8-2.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림8-2.png')).convert('L').save(os.path.join(o, '그림8-2-흑백.png'))
