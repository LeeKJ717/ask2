# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig19-1.svg', 540)
x0, x1, yb, yt = 90, 770, 430, 50
f.line(x0, yb, x1, yb, INK, 2.5); f.line(x0, yb, x0, yt, INK, 2.5)
for h in range(0, 4):
    x = x0 + (x1 - x0) * h / 3
    f.line(x, yb, x, yb + 10, INK, 2); f.text(x, yb + 38, str(h), 22, 'normal', 'middle')
f.text((x0 + x1) / 2, yb + 72, '포도당 투여 후 시간 (시간)', 22, 'normal', 'middle')
f.text(55, 240, '인슐린', 22, 'normal', 'middle'); f.text(55, 270, '분비', 22, 'normal', 'middle')
base = 380
# oral: large; IV: small (same plasma glucose)
oral = f'M {x0} {base} C 190 {base} 220 120 300 120 C 400 120 450 {base-40} 560 {base-20} C 640 {base-10} 700 {base} {x1} {base}'
iv = f'M {x0} {base} C 190 {base} 220 250 300 250 C 400 250 450 {base-30} 560 {base-12} C 640 {base-5} 700 {base} {x1} {base}'
f.path(oral, BLUE, 4); f.path(iv, WARM, 4)
f.line(500, 85, 560, 85, BLUE, 5); f.text(575, 94, '경구 포도당', 24, 'normal', 'start')
f.line(500, 140, 560, 140, WARM, 5); f.text(575, 149, '정맥 포도당', 24, 'normal', 'start')
f.text(575, 182, '(혈당 곡선 동일)', 22, 'normal', 'start', GRAY)
f.line(300, 125, 300, 245, GRAY, 2, '8 6')
f.text(312, 212, '인크레틴', 22, 'normal', 'start', GRAY)
f.text(312, 238, '효과', 22, 'normal', 'start', GRAY)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig19-1.svg'), write_to=os.path.join(o, '그림19-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림19-1.png')).convert('L').save(os.path.join(o, '그림19-1-흑백.png'))
