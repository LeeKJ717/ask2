# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD, LGRAY
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig7-1.svg', 700)
f.text(135, 34, '포도당 경로', 26, 700); f.text(665, 34, 'GLP-1 경로', 26, 700)
L = ['포도당 유입', '글루코키네이스·해당', 'ATP/ADP 비 증가', 'KATP 채널 닫힘', '탈분극, Ca 채널 열림', '세포 내 Ca2+ 증가']
y = 56
for i, t in enumerate(L):
    f.tbox(20, y, 230, 64, [t], 22, LBLUE if i < 5 else LGREEN, BLUE if i < 5 else GREEN)
    if i: f.arrow(135, y - 28, 135, y, BLUE, 2.8)
    y += 92
R = ['GLP-1 수용체(Gs)', 'cAMP 증가', 'PKA·EPAC2 활성화']
y = 56
for i, t in enumerate(R):
    f.tbox(550, y, 230, 64, [t], 22, LGOLD, GOLD)
    if i: f.arrow(665, y - 28, 665, y, GOLD, 2.8)
    y += 92
f.tbox(270, 586, 260, 80, ['인슐린 과립 분비'], 24, LGREEN, GREEN, first_bold=True)
f.arrow(250, 520, 330, 586, GREEN, 3)
f.arrow(665, 304, 530, 612, GOLD, 3)
f.text(655, 360, '증폭', 24, 700, 'start', GOLD)
f.tbox(290, 200, 240, 150, ['포도당이 낮으면', 'ATP·Ca2+가 부족해', '증폭 효과 약함'], 22, LGRAY, GRAY, dash='8 5')
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig7-1.svg'), write_to=os.path.join(o, '그림7-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림7-1.png')).convert('L').save(os.path.join(o, '그림7-1-흑백.png'))
