# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig22-1.svg', 610)
x0, x1, yb, yt = 90, 770, 400, 110
f.line(x0, yb, x1, yb, INK, 2.5); f.line(x0, yb, x0, yt, INK, 2.5)
bd = [x0, 210, 380, 560, x1]
for x in bd[1:-1]:
    f.line(x, yt - 10, x, yb, GRAY, 2, '8 6')
for x, t in zip(bd[:-1], ['흡수기', '흡수후기', '단식', '장기 단식']):
    pass
for i, t in enumerate(['흡수기', '흡수후기', '단식', '장기 단식']):
    f.text((bd[i] + bd[i + 1]) / 2, 85, t, 22, 'bold', 'middle')
for x, t in zip([x0, 210, 380, 560], ['0', '6시간', '24시간', '3일']):
    f.line(x, yb, x, yb + 10, INK, 2); f.text(x, yb + 38, t, 22, 'normal', 'middle')
f.text(x1, yb + 38, '수주', 22, 'normal', 'middle')
f.text((x0 + x1) / 2, yb + 72, '마지막 식사 뒤 시간 (비례 아님)', 22, 'normal', 'middle')
f.text(50, 255, '상대', 22, 'normal', 'middle'); f.text(50, 285, '수준', 22, 'normal', 'middle')
# 간 글리코겐: 높음에서 소진
f.path(f'M {x0} 150 C 170 150 200 170 260 230 C 320 290 360 380 400 392 L {x1} 392', GOLD, 4)
# 혈당: 거의 평탄, 약간 하강
f.path(f'M {x0} 215 C 130 195 170 205 210 240 C 250 272 500 262 {x1} 292', BLUE, 4)
# 유리지방산: 완만 상승
f.path(f'M {x0} 360 C 200 360 260 330 380 290 C 480 255 600 225 {x1} 215', WARM, 4)
# 케톤체: 늦게 급상승
f.path(f'M {x0} 395 L 330 395 C 420 392 480 350 560 270 C 640 200 700 170 {x1} 160', GREEN, 4)
ly = [520, 560]
f.line(100, ly[0], 160, ly[0], GOLD, 5); f.text(175, ly[0] + 9, '간 글리코겐', 24, 'normal', 'start')
f.line(430, ly[0], 490, ly[0], BLUE, 5); f.text(505, ly[0] + 9, '혈당', 24, 'normal', 'start')
f.line(100, ly[1], 160, ly[1], WARM, 5); f.text(175, ly[1] + 9, '유리지방산', 24, 'normal', 'start')
f.line(430, ly[1], 490, ly[1], GREEN, 5); f.text(505, ly[1] + 9, '케톤체', 24, 'normal', 'start')
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig22-1.svg'), write_to=os.path.join(o, '그림22-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림22-1.png')).convert('L').save(os.path.join(o, '그림22-1-흑백.png'))
