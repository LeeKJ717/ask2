# -*- coding: utf-8 -*-
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig10-2.svg', 480)
cx, cy = 330, 240
f.ellipse(cx, cy, 285, 175, LBLUE, BLUE, 3)
f.ellipse(cx, cy, 245, 135, LGOLD, GOLD, 3)
# 크리스타: 내막이 안쪽으로 접힌 주름
xs = [-170, -105, -40, 25, 90, 155]
for i, dx in enumerate(xs):
    t = math.sqrt(1 - (dx / 245) ** 2) * 135
    if i % 2 == 0:
        f.path(f'M {cx+dx} {cy-t} L {cx+dx} {cy+10}', GOLD, 4)
    else:
        f.path(f'M {cx+dx} {cy+t} L {cx+dx} {cy-10}', GOLD, 4)
f.circle(cx - 20, cy + 70, 13, 'none', WARM, 3)
f.callout(cx + 245 * math.cos(math.radians(70)), cy - 135 * math.sin(math.radians(70)), 640, 55, ['내막'], 24)
f.callout(cx + 285 * math.cos(math.radians(30)), cy - 175 * math.sin(math.radians(30)), 640, 125, ['외막'], 24)
f.callout(cx + 265 * math.cos(math.radians(12)), cy - 155 * math.sin(math.radians(12)), 640, 195, ['막간 공간'], 24)
f.callout(cx + 200, cy - 5, 640, 265, ['기질'], 24)
f.callout(cx + 155, cy + 60, 640, 345, ['크리스타', '(내막의 주름)'], 24)
f.callout(cx - 20, cy + 83, 640, 440, ['mtDNA'], 24)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig10-2.svg'), write_to=os.path.join(o, '그림10-2.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림10-2.png')).convert('L').save(os.path.join(o, '그림10-2-흑백.png'))
