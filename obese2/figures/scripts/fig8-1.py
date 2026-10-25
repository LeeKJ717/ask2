# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
LGRAY = "#F1F3F5"
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig8-1.svg', 600)
L = ['렙틴(지방세포 호르몬)', '렙틴 수용체(LepRb)', 'JAK2 인산화효소 활성화', 'STAT3 인산화·핵 이동', '유전자 발현 변화(POMC 증가 등)']
cols = [(LGOLD, GOLD), (LBLUE, BLUE), (LBLUE, BLUE), (LBLUE, BLUE), (LGREEN, GREEN)]
for i, t in enumerate(L):
    y = 10 + i * 112
    f.tbox(20, y, 360, 70, [t], 22, cols[i][0], cols[i][1])
    if i: f.arrow(200, y - 42, 200, y, GRAY, 2.8)
f.tbox(450, 330, 330, 120, ['SOCS3 단백질 증가', '신호를 줄이는 되먹임'], 22, LGRAY, GRAY, dash='8 5')
f.arrow(380, 381, 450, 381, GRAY, 2.8)
f.arrow(560, 330, 380, 269, GRAY, 2.8)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig8-1.svg'), write_to=os.path.join(o, '그림8-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림8-1.png')).convert('L').save(os.path.join(o, '그림8-1-흑백.png'))
