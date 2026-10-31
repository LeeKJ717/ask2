# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig17-1.svg', 560)
x0, x1, yb, yt = 90, 770, 440, 50
f.line(x0, yb, x1, yb, INK, 2.5)
f.line(x0, yb, x0, yt, INK, 2.5)
for h in range(0, 7):
    x = x0 + (x1 - x0) * h / 6
    f.line(x, yb, x, yb + 10, INK, 2)
    f.text(x, yb + 38, str(h), 22, 'normal', 'middle')
f.text((x0 + x1) / 2, yb + 74, '식사 후 시간 (시간)', 22, 'normal', 'middle')
f.text(60, 245, '상대', 22, 'normal', 'middle')
f.text(60, 275, '수준', 22, 'normal', 'middle')
# curves (schematic, baseline y=330 for glucose/insulin/aa/tg)
base = 330
f.path(f'M {x0} {base} C 170 {base} 190 190 260 190 C 340 190 380 {base-5} 450 {base} L {x1} {base}', BLUE, 4)
f.path(f'M {x0} {base+40} C 160 {base+40} 180 110 250 110 C 340 110 400 {base+30} 480 {base+40} L {x1} {base+40}', WARM, 4)
f.path(f'M {x0} {base+10} C 200 {base+10} 280 230 380 230 C 480 230 560 {base+5} {x1} {base+10}', GREEN, 4)
f.path(f'M {x0} {base+20} C 300 {base+20} 380 270 520 270 C 620 270 680 {base+15} {x1} {base+20}', GOLD, 4)
f.text(200, 160, '인슐린', 24, 'bold', 'middle', WARM) if False else None
f.callout(250, 110, 330, 75, ['인슐린'], 24, 'start')
f.callout(260, 190, 340, 150, ['혈중 포도당'], 24, 'start')
f.callout(380, 230, 470, 205, ['아미노산'], 24, 'start')
f.callout(520, 270, 560, 235, ['중성지방'], 24, 'start')
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig17-1.svg'), write_to=os.path.join(o, '그림17-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림17-1.png')).convert('L').save(os.path.join(o, '그림17-1-흑백.png'))
