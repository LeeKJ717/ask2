# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig1-1.svg', 700)
# 왼쪽: 네 수준(개체→효소), 오른쪽: 각 수준의 에너지 거래
rows = [("개체", ["음식 에너지 섭취", "→ 체온·움직임·저장"], LBLUE, BLUE),
        ("조직·세포", ["영양소 산화", "→ ATP 생산"], LGREEN, GREEN),
        ("미토콘드리아", ["전자 전달", "→ 양성자 구배"], LGOLD, GOLD),
        ("효소", ["ATP 가수분해", "→ 일(구조 변화)"], LWARM, WARM)]
y = 20
for i, (nm, ls, fl, st) in enumerate(rows):
    f.tbox(20, y, 250, 110, [nm], 26, fl, st, first_bold=True)
    f.tbox(330, y, 450, 110, ls, 24, fl, st)
    f.arrow(270, y + 55, 330, y + 55, st, 2.8)
    if i < 3: f.arrow(145, y + 110, 145, y + 150, GRAY, 2.8)
    y += 150
f.text(400, 650, '매 수준에서 일부 에너지는 열로 나가고, 엔트로피는 바깥으로 내보낸다', 22, 400, 'middle', GRAY)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig1-1.svg'), write_to=os.path.join(o, '그림1-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림1-1.png')).convert('L').save(os.path.join(o, '그림1-1-흑백.png'))
