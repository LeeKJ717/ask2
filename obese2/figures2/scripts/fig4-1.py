# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig4-1.svg', 760)
# 가운데 기둥: 포도당 → 피루브산 → 아세틸-CoA → TCA 회로
f.tbox(300, 10, 200, 70, ['포도당'], 26, LBLUE, BLUE, first_bold=True)
f.arrow(400, 80, 400, 130, GRAY, 2.8); f.text(520, 112, '해당', 22, 400, 'start', GRAY)
f.tbox(300, 130, 200, 70, ['피루브산'], 26, LBLUE, BLUE, first_bold=True)
f.arrow(400, 200, 400, 250, GRAY, 2.8); f.text(520, 232, 'PDH', 22, 400, 'start', GRAY)
f.tbox(300, 250, 200, 70, ['아세틸-CoA'], 26, LGOLD, GOLD, first_bold=True)
f.arrow(400, 320, 400, 380, GRAY, 2.8)
f.tbox(270, 380, 260, 100, ['TCA 회로'], 28, LGOLD, GOLD, first_bold=True)
f.arrow(400, 480, 400, 540, GRAY, 2.8)
f.tbox(220, 540, 360, 90, ['전자전달계, ATP'], 26, LGREEN, GREEN, first_bold=True)
# 왼쪽: 글리코겐 (저장)
f.tbox(20, 10, 220, 70, ['글리코겐'], 24, LGRAY if False else '#F1F3F5', GRAY, first_bold=True)
f.arrow(240, 45, 300, 45, GRAY, 2.5)
# 오른쪽: 지방산
f.tbox(560, 250, 220, 70, ['지방산'], 26, LWARM, WARM, first_bold=True)
f.arrow(560, 285, 500, 285, WARM, 2.8)
f.text(670, 232, 'β산화', 22, 400, 'middle', WARM)
f.tbox(560, 380, 220, 90, ['케톤체'], 26, LWARM, WARM, first_bold=True)
f.arrow(500, 300, 590, 380, WARM, 2.5); f.text(670, 510, '간에서 생성', 22, 400, 'middle', WARM)
# 왼쪽: 아미노산
f.tbox(20, 130, 220, 70, ['아미노산'], 26, LGREEN, GREEN, first_bold=True)
f.arrow(240, 165, 300, 165, GREEN, 2.5)
f.tbox(20, 380, 220, 100, ['아미노산', '요소회로'], 24, LGREEN, GREEN)
f.arrow(270, 430, 240, 430, GREEN, 2.5)
f.text(400, 700, '화살표는 주된 흐름 방향이며, 비가역 단계는 표 4-1', 22, 400, 'middle', GRAY)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig4-1.svg'), write_to=os.path.join(o, '그림4-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림4-1.png')).convert('L').save(os.path.join(o, '그림4-1-흑백.png'))
