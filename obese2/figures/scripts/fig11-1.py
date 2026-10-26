# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig11-1.svg', 640)
rows = [(['유전 변이 발견'], ['MC4R, POMC', '변이 환자'], LWARM, WARM),
        (['기능 확인'], ['세포·생쥐에서', '기능 확인'], LBLUE, BLUE),
        (['효과 방향 추정'], ['전장 유전체', '연관 연구'], LBLUE, BLUE),
        (['약으로 같은 방향 조절'], ['MC4R 경로를', '켜는 약'], LGREEN, GREEN),
        (['임상시험으로 확인'], ['희귀 질환', '임상 결과'], LGOLD, GOLD)]
for i, (a, b, fl, st) in enumerate(rows):
    y = 10 + i * 124
    f.tbox(20, y, 400, 84, a, 24, fl, st, first_bold=True)
    f.tbox(480, y, 300, 84, b, 22, fl, st)
    f.arrow(420, y + 42, 480, y + 42, st, 2.8)
    if i: f.arrow(220, y - 40, 220, y, GRAY, 2.8)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig11-1.svg'), write_to=os.path.join(o, '그림11-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림11-1.png')).convert('L').save(os.path.join(o, '그림11-1-흑백.png'))
