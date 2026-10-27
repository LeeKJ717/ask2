# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig12-2.svg', 600)
f.tbox(40, 10, 300, 90, ['세포 밖 도메인', '(ECD)'], 22, LBLUE, BLUE, first_bold=True)
f.tbox(440, 10, 340, 100, ['펩타이드 작용제', 'C 쪽은 ECD, N 쪽은 TMD로'], 22, LGOLD, GOLD, first_bold=True)
f.arrow(440, 55, 340, 55, GOLD, 2.8)
f.arrow(190, 100, 190, 240, BLUE, 2.8)
f.arrow(560, 110, 450, 240, GOLD, 2.8)
f.tbox(100, 240, 600, 130, ['막횡단 도메인(TMD)', '세포막을 가로지르는 7개 나선과 안쪽 포켓'], 22, LGREEN, GREEN, first_bold=True)
f.tbox(40, 480, 340, 100, ['소분자 작용제', 'TMD 안쪽 포켓에 결합'], 22, LWARM, WARM, first_bold=True)
f.arrow(210, 480, 280, 370, WARM, 2.8)
f.tbox(440, 480, 340, 100, ['세포 안쪽', 'Gs 단백질이 붙음'], 22, "#F1F3F5", GRAY, first_bold=True)
f.arrow(560, 370, 610, 480, GRAY, 2.8)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig12-2.svg'), write_to=os.path.join(o, '그림12-2.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림12-2.png')).convert('L').save(os.path.join(o, '그림12-2-흑백.png'))
