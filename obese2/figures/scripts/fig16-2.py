# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig16-2.svg', 520)
f.tbox(20, 10, 340, 100, ['체중 감소', '지방과 제지방이 함께 줄어듦'], 22, LWARM, WARM, first_bold=True)
f.tbox(440, 10, 340, 100, ['근육 보존 접근', '액티빈 수용체 차단 등'], 22, LGREEN, GREEN, first_bold=True)
f.arrow(190, 110, 190, 210, WARM, 2.8); f.arrow(610, 110, 610, 210, GREEN, 2.8)
f.tbox(20, 210, 340, 130, ['제지방 감소', '근력, 기초대사량', '저하 우려'], 22, LWARM, WARM, first_bold=True)
f.tbox(440, 210, 340, 130, ['제지방 유지 또는', '증가를 목표', '(임상 근거 축적 중)'], 22, LGREEN, GREEN, first_bold=True)
f.arrow(190, 340, 190, 410, WARM, 2.8); f.arrow(610, 340, 610, 410, GREEN, 2.8)
f.tbox(20, 410, 340, 100, ['체중 재증가 위험', '(논쟁 중)'], 22, "#F1F3F5", GRAY, first_bold=True)
f.tbox(440, 410, 340, 100, ['체성분 개선', '(기대)'], 22, "#F1F3F5", GRAY, first_bold=True)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig16-2.svg'), write_to=os.path.join(o, '그림16-2.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림16-2.png')).convert('L').save(os.path.join(o, '그림16-2-흑백.png'))
