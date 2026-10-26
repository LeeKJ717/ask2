# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig9-1.svg', 580)
f.tbox(20, 10, 230, 120, ['미토콘드리아', 'ATP를 만드는 곳'], 22, LWARM, WARM, first_bold=True)
f.tbox(285, 10, 230, 120, ['소포체', '단백질 접힘·칼슘'], 22, LBLUE, BLUE, first_bold=True)
f.tbox(550, 10, 230, 120, ['리소좀·오토파지', '분해와 재활용'], 22, LGREEN, GREEN, first_bold=True)
f.arrow(135, 130, 330, 250, WARM, 2.8)
f.arrow(400, 130, 400, 250, BLUE, 2.8)
f.arrow(665, 130, 470, 250, GREEN, 2.8)
f.tbox(220, 250, 360, 100, ['에너지·영양 센서', 'AMPK와 mTOR'], 22, LGOLD, GOLD, first_bold=True)
f.arrow(400, 350, 400, 440, GOLD, 3)
f.tbox(150, 440, 500, 110, ['세포 상태가 바뀜', '분비·생존·대사 속도'], 22, LGRAY if False else "#F1F3F5", GRAY)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig9-1.svg'), write_to=os.path.join(o, '그림9-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림9-1.png')).convert('L').save(os.path.join(o, '그림9-1-흑백.png'))
