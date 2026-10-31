# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig16-1.svg', 620)
f.tbox(30, 30, 340, 90, ['포도당 산화', '(해당, PDH)'], 24, LBLUE, BLUE, first_bold=True)
f.tbox(430, 30, 340, 90, ['지방산 산화', '(CPT1, 베타 산화)'], 24, LGOLD, GOLD, first_bold=True)
f.tbox(30, 260, 340, 90, ['말로닐-CoA', '(포도당이 풍부할 때 증가)'], 24, '#F1F3F5', GRAY, first_bold=True)
f.tbox(430, 260, 340, 90, ['아세틸-CoA, 시트르산', '(지방산이 풍부할 때 증가)'], 24, '#F1F3F5', GRAY, first_bold=True)
f.arrow(200, 120, 200, 260, GRAY, 2.8)
f.arrow(600, 120, 600, 260, GRAY, 2.8)
f.inhibit(370, 305, 430, 305, WARM, 2.8) if False else None
f.inhibit(200, 350, 480, 450, WARM, 2.8)
f.inhibit(600, 350, 320, 450, WARM, 2.8)
f.tbox(30, 480, 340, 90, ['CPT1 억제', '→ 지방산 산화 감소'], 24, LWARM, WARM, first_bold=True)
f.tbox(430, 480, 340, 90, ['PDH·PFK 억제', '→ 포도당 산화 감소'], 24, LWARM, WARM, first_bold=True)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig16-1.svg'), write_to=os.path.join(o, '그림16-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림16-1.png')).convert('L').save(os.path.join(o, '그림16-1-흑백.png'))
