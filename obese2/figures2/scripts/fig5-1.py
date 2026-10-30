# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig5-1.svg', 760)
f.text(190, 28, '준비 단계 (ATP 2개 투입)', 22, 700, 'middle', BLUE)
f.text(610, 28, '보상 단계 (ATP 4개·NADH 2개)', 22, 700, 'middle', GREEN)
L = [('포도당', 0), ('포도당 6-인산', 1), ('프럭토스 6-인산', 0), ('프럭토스 1,6-이인산', 1), ('글리세르알데하이드 3-인산', 0)]
R = [('1,3-비스포스포글리세르산', 0), ('3-포스포글리세르산', 0), ('2-포스포글리세르산', 0), ('포스포엔올피루브산', 0), ('피루브산', 1)]
Le = ['HK', 'GPI', 'PFK-1', '알돌레이스+TPI']
Re = ['PGK', 'PGM', '에놀레이스', 'PK']
ys = [50 + 130 * i for i in range(5)]
for (nm, ir), y in zip(L, ys):
    f.tbox(20, y, 340, 80, [nm], 22, LWARM if ir else LBLUE, WARM if ir else BLUE)
for (nm, ir), y in zip(R, ys):
    f.tbox(440, y, 340, 80, [nm], 22, LWARM if ir else LGREEN, WARM if ir else GREEN)
for i in range(4):
    f.arrow(190, ys[i] + 80, 190, ys[i + 1], BLUE, 2.8)
    f.text(205, ys[i] + 112, Le[i], 22, 400, 'start', GRAY)
    f.arrow(610, ys[i] + 80, 610, ys[i + 1], GREEN, 2.8)
    f.text(625, ys[i] + 112, Re[i], 22, 400, 'start', GRAY)
m5 = ys[4] + 40; m1 = ys[0] + 40
f.line(360, m5, 400, m5, GRAY, 2.8); f.line(400, m5, 400, m1, GRAY, 2.8); f.arrow(400, m1, 440, m1, GRAY, 2.8)
f.text(400, 735, '붉은 상자 = 비가역 단계에서 만들어지는 물질', 22, 400, 'middle', WARM)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig5-1.svg'), write_to=os.path.join(o, '그림5-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림5-1.png')).convert('L').save(os.path.join(o, '그림5-1-흑백.png'))
