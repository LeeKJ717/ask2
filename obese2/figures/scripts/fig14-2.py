# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig14-2.svg', 500)
rows = [('티르제파타이드 5 mg', 15.0, GOLD, LGOLD), ('티르제파타이드 10 mg', 19.5, WARM, LWARM),
        ('티르제파타이드 15 mg', 20.9, WARM, LWARM), ('위약', 3.1, GRAY, "#F1F3F5")]
y = 20; s = 28
for name, v, st, fl in rows:
    f.text(20, y + 22, name, 22, 'bold', 'start', INK)
    f.tbox(20, y + 40, v * s, 50, [''], 22, fl, st)
    f.text(20 + v * s + 15, y + 78, f"{v}%", 22, 'bold', 'start', INK)
    y += 110
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig14-2.svg'), write_to=os.path.join(o, '그림14-2.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림14-2.png')).convert('L').save(os.path.join(o, '그림14-2-흑백.png'))
