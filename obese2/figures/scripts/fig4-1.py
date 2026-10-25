# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD, MGOLD
import shapes as S
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg")
f = Fig('fig4-1.svg', 620)
f.ellipse(430, 55, 100, 40, LBLUE, BLUE, 2.5); f.text(430, 65, '뇌', 28, 700)
f.ellipse(315, 230, 70, 48, LWARM, WARM, 2.8, rot=-20)
f.ellipse(480, 265, 75, 20, LGOLD, GOLD, 2.5, rot=8)
pts = [(400,310),(505,328),(390,362),(505,396),(390,430),(505,464),(410,495)]
for w, c in ((30, BLUE), (24, LBLUE)):
    f.path(S.smooth_open(pts), c, w, 'none')
for c, w in ((BLUE, 30), (LGREEN, 24)):
    f.path('M 600 340 L 600 565 L 300 565 L 300 525', c, w, 'none')
    f.path('M 410 495 Q 340 505 300 525', BLUE if w == 30 else LBLUE, w, 'none')
f.ellipse(730, 440, 55, 45, LGOLD, GOLD, 2.5)
f.path('M 445 312 C 380 260 385 150 405 92', GRAY, 3, 'none', dash='9 6')
def dot(x, y, c): f.circle(x, y, 9, c, INK, 1.4)
dot(315, 230, WARM); dot(400, 316, GREEN); dot(398, 366, BLUE)
dot(505, 466, GOLD); dot(600, 450, GOLD); dot(480, 265, MGOLD); dot(730, 440, GOLD)
R = 215
f.callout(315, 230, R, 185, ['위: X/A형 세포'], 24, 'end', weight=700, sub='→ 그렐린')
f.callout(400, 316, R, 295, ['십이지장·공장'], 24, 'end', weight=700, sub='I세포→CCK')
f.callout(398, 366, R, 395, ['K세포'], 24, 'end', weight=700, sub='→ GIP')
f.callout(505, 466, R, 470, ['회장: L세포'], 24, 'end', weight=700, sub='→ GLP-1·PYY·OXM')
f.callout(480, 265, 570, 190, ['췌장 β세포'], 24, 'start', weight=700, sub='→ 인슐린·아밀린')
f.callout(730, 440, 724, 350, ['지방세포'], 24, 'end', weight=700, sub='→ 렙틴')
f.callout(600, 450, 625, 555, ['대장: L세포'], 24, 'start', weight=700, sub='→ GLP-1·PYY')
f.text(330, 160, '미주신경', 22, 400, 'end', GRAY)
print(f.save(OUT)); F.report()
import cairosvg
from PIL import Image
o = os.path.join(here, '..', 'out')
cairosvg.svg2png(url=os.path.join(OUT, 'fig4-1.svg'), write_to=os.path.join(o, '그림4-1.png'), output_width=2079, background_color='white')
Image.open(os.path.join(o, '그림4-1.png')).convert('L').save(os.path.join(o, '그림4-1-흑백.png'))
