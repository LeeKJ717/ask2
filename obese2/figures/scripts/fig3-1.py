# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD, MGRAY, LGRAY
here = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(here, "..", "svg")
f = Fig('fig3-1.svg', 640)
# 혈중 신호(왼쪽 열)
f.text(100, 40, '혈액의 신호', 26, 700)
f.tbox(10, 62, 180, 84, ['렙틴', '(지방조직)'], 24, LGOLD, GOLD)
f.tbox(10, 168, 180, 84, ['인슐린', '(췌장 β세포)'], 24, LGOLD, GOLD)
f.tbox(10, 274, 180, 84, ['그렐린', '(위)'], 24, LWARM, WARM)
f.tbox(10, 380, 180, 84, ['GLP-1·PYY', '(소장·대장)'], 24, LBLUE, BLUE)
# 궁상핵
f.rect(250, 40, 270, 330, LGRAY, GRAY, 2, 14, dash='8 6')
f.text(385, 76, '궁상핵', 26, 700)
f.tbox(272, 100, 226, 96, ['POMC/CART', '뉴런 (포만)'], 24, LGREEN, GREEN, first_bold=True)
f.tbox(272, 250, 226, 96, ['AgRP/NPY', '뉴런 (배고픔)'], 24, LWARM, WARM, first_bold=True)
# 실방핵
f.tbox(590, 150, 200, 130, ['실방핵', 'MC4R 뉴런'], 26, LBLUE, BLUE, first_bold=True)
f.tbox(590, 330, 200, 84, ['식욕 감소', '에너지 소비 증가'], 22, LGREEN, GREEN)
# 뇌간
f.rect(250, 470, 270, 150, LBLUE, BLUE, 2, 14)
f.text(385, 508, '뇌간', 26, 700)
f.text(385, 548, '고립로핵 · 최후야', 24, 400)
f.text(385, 584, '(포만·구역 신호)', 24, 400, color=GRAY)
# 화살표: 렙틴 -> POMC(+), 렙틴 -| AgRP
f.arrow(190, 104, 272, 140, GREEN, 2.8)
f.inhibit(190, 112, 272, 276, WARM, 2.8)
f.arrow(190, 210, 272, 160, GREEN, 2.8)
f.inhibit(190, 218, 272, 290, WARM, 2.8)
f.arrow(190, 316, 272, 312, WARM, 2.8)
f.arrow(190, 422, 272, 180, GREEN, 2.8, dash='8 5')
f.arrow(190, 440, 250, 500, BLUE, 2.8)
# 궁상핵 -> 실방핵
f.arrow(498, 148, 590, 190, GREEN, 3)
f.inhibit(498, 298, 590, 245, WARM, 3)
f.inhibit(385, 250, 385, 200, WARM, 3)
f.arrow(590, 280, 590, 330, GREEN, 3) if False else f.arrow(690, 280, 690, 330, GREEN, 3)
f.arrow(520, 520, 660, 418, BLUE, 3)
f.text(395, 140, '', 22) if False else None
# 범례
f.arrow(560, 600, 610, 600, GREEN, 3); f.text(620, 608, '촉진', 22, 400, 'start')
f.inhibit(690, 600, 740, 600, WARM, 3); f.text(748, 608, '억제', 22, 400, 'start')
print(f.save(OUT)); F.report()

import cairosvg
from PIL import Image
o=os.path.join(here,'..','out')
cairosvg.svg2png(url=os.path.join(OUT,'fig3-1.svg'), write_to=os.path.join(o,'그림3-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o,'그림3-1.png')).convert('L').save(os.path.join(o,'그림3-1-흑백.png'))
