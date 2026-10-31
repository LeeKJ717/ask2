# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig35-1.svg', 570)
def node(x, y, t, fill, stroke): f.tbox(x, y, 170, 64, [t], 24, fill, stroke, True)
node(315, 30, '뇌', LBLUE, BLUE)
node(30, 150, '장', LGOLD, GOLD)
node(600, 150, '지방조직', LGOLD, GOLD)
node(30, 330, '췌장', LWARM, WARM)
node(600, 330, '근육', LBLUE, BLUE)
node(315, 450, '간', LGREEN, GREEN)
f.arrow(115, 214, 115, 330, INK, 3); f.text(130, 280, '인크레틴', 22, 'normal', 'start')
f.arrow(200, 375, 315, 470, INK, 3); f.text(40, 430, '인슐린·글루카곤', 22, 'normal', 'start')
f.arrow(685, 150, 485, 70, INK, 3); f.text(500, 135, '렙틴', 22, 'normal', 'start')
f.arrow(400, 450, 400, 94, INK, 3); f.text(415, 280, '케톤체, FGF21', 22, 'normal', 'start')
f.arrow(650, 214, 470, 455, INK, 3); f.text(630, 285, '지방산', 22, 'normal', 'start')
f.arrow(685, 394, 485, 480, INK, 3); f.text(625, 490, '아미노산, 젖산', 22, 'normal', 'start')
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig35-1.svg'), write_to=os.path.join(o, '그림35-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림35-1.png')).convert('L').save(os.path.join(o, '그림35-1-흑백.png'))
