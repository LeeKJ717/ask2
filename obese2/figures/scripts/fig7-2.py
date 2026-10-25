# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
LGRAY = "#F1F3F5"
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig7-2.svg', 560)
rows = [('밀리초~초', ['채널 열림·닫힘', '막전위 변화'], LBLUE, BLUE),
        ('초~분', ['Ca2+ 진동', 'cAMP 변화'], LGREEN, GREEN),
        ('분', ['인슐린 과립 분비', '(제1기, 제2기)'], LGOLD, GOLD),
        ('시간', ['유전자 발현', '인슐린 합성'], LWARM, WARM),
        ('일~주', ['β세포 수·생존', '변화'], LGRAY, GRAY)]
for i, (t, ev, fl, st) in enumerate(rows):
    y = 10 + i * 108
    f.tbox(10, y, 190, 86, [t], 24, fl, st, first_bold=True)
    f.tbox(250, y, 540, 86, ev, 22, fl, st)
    f.arrow(200, y + 43, 250, y + 43, st, 2.8)
    if i: f.arrow(105, y - 22, 105, y, GRAY, 2.5)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig7-2.svg'), write_to=os.path.join(o, '그림7-2.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림7-2.png')).convert('L').save(os.path.join(o, '그림7-2-흑백.png'))
