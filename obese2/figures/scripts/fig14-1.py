# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig14-1.svg', 560)
f.tbox(250, 10, 300, 90, ['티르제파타이드', '주 1회 주사'], 22, LWARM, WARM, first_bold=True)
f.tbox(20, 200, 330, 100, ['GIP 수용체', '지방조직, 췌장, 뇌'], 22, LGOLD, GOLD, first_bold=True)
f.tbox(450, 200, 330, 100, ['GLP-1 수용체', '췌장, 뇌, 위장관'], 22, LBLUE, BLUE, first_bold=True)
f.arrow(330, 100, 185, 200, GOLD, 2.8); f.arrow(470, 100, 615, 200, BLUE, 2.8)
f.arrow(185, 300, 185, 400, GOLD, 2.8); f.arrow(615, 300, 615, 400, BLUE, 2.8)
f.tbox(20, 400, 330, 130, ['인슐린 분비 보강', '지방 대사 조절', '(기전은 논쟁 중)'], 22, LGOLD, GOLD, first_bold=True)
f.tbox(450, 400, 330, 130, ['식욕 감소', '포도당 의존 인슐린 분비', '위 배출 지연'], 22, LBLUE, BLUE, first_bold=True)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig14-1.svg'), write_to=os.path.join(o, '그림14-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림14-1.png')).convert('L').save(os.path.join(o, '그림14-1-흑백.png'))
