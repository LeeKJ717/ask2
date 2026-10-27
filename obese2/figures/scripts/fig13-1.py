# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig13-1.svg', 520)
f.tbox(20, 20, 230, 110, ['천연 GLP-1', '반감기 1~2분'], 22, LBLUE, BLUE, first_bold=True)
f.tbox(285, 20, 230, 110, ['리라글루타이드', '1일 1회 주사'], 22, LGOLD, GOLD, first_bold=True)
f.tbox(550, 20, 230, 110, ['세마글루타이드', '주 1회 주사'], 22, LWARM, WARM, first_bold=True)
f.arrow(250, 75, 285, 75, GRAY, 2.8); f.arrow(515, 75, 550, 75, GRAY, 2.8)
f.arrow(665, 130, 665, 230, WARM, 2.8)
f.tbox(285, 230, 495, 110, ['경구 세마글루타이드', 'SNAC 정제, 공복 복용'], 22, LGREEN, GREEN, first_bold=True)
f.tbox(20, 400, 760, 100, ['공통 문법: Aib 치환 + 지방산 측쇄 + 알부민 결합', '길이와 연결자를 바꾸어 체류 시간을 조절'], 22, "#F1F3F5", GRAY, first_bold=True)
f.arrow(530, 340, 530, 400, GRAY, 2.8)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig13-1.svg'), write_to=os.path.join(o, '그림13-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림13-1.png')).convert('L').save(os.path.join(o, '그림13-1-흑백.png'))
