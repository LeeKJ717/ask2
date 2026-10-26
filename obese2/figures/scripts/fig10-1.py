# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig10-1.svg', 700)
rows = [('개체', ['사람 한 명'], LWARM, WARM),
        ('조직', ['췌장 속 췌도(섬 모양 세포 집단)'], LWARM, WARM),
        ('세포', ['인슐린을 만드는 β세포'], LBLUE, BLUE),
        ('핵', ['DNA가 들어 있는 곳'], LBLUE, BLUE),
        ('염색체', ['DNA가 감긴 구조, 사람은 23쌍'], LGREEN, GREEN),
        ('유전자', ['INS(인슐린 유전자), 11번 염색체'], LGREEN, GREEN),
        ('mRNA', ['핵 안에서 복사된 설계도'], LGOLD, GOLD),
        ('단백질', ['리보솜이 읽어 만든 인슐린'], LGOLD, GOLD)]
for i, (a, b, fl, st) in enumerate(rows):
    y = 10 + i * 84
    f.tbox(20, y, 190, 62, [a], 24, fl, st, first_bold=True)
    f.tbox(260, y, 520, 62, b, 22, fl, st)
    f.arrow(210, y + 31, 260, y + 31, st, 2.8)
    if i: f.arrow(115, y - 22, 115, y, GRAY, 2.5)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig10-1.svg'), write_to=os.path.join(o, '그림10-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림10-1.png')).convert('L').save(os.path.join(o, '그림10-1-흑백.png'))
