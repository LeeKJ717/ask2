# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, LGREEN, GOLD, LGOLD
import cairosvg
from PIL import Image
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, "..", "svg"); O = os.path.join(here, '..', 'out')
def fin(f, num):
    print(f.save(OUT)); F.report()
    cairosvg.svg2png(url=os.path.join(OUT, f'fig{num}.svg'), write_to=os.path.join(O, f'그림{num}.png'), output_width=2079, background_color='white')
    Image.open(os.path.join(O, f'그림{num}.png')).convert('L').save(os.path.join(O, f'그림{num}-흑백.png'))
def vflow(num, steps, fills, w=520, H=46, G=26, note=None):
    f = Fig(f'fig{num}.svg', 14+len(steps)*H+(len(steps)-1)*G+20)
    y=14; x=(800-w)/2
    for i,s in enumerate(steps):
        fl,st = fills[i]
        f.tbox(x,y,w,H,[s],24,fl,st,i==len(steps)-1)
        if i<len(steps)-1: f.arrow(400,y+H,400,y+H+G,INK,2.5)
        y+=H+G
    fin(f, num)
B=(LBLUE,BLUE); G_=(LGREEN,GREEN); Y=(LGOLD,GOLD); R=(LWARM,WARM)
# 4-1 장비 연결
f=Fig('fig4-1.svg',350)
devs=[['holymind','RTX 5060 Ti 16GB'],['z840','RTX 3060 12GB × 2'],['soul3 · win14','RTX 3060 12GB'],['z441','GPU 확인 필요']]
y=14
for d in devs:
    f.tbox(20,y,300,70,d,24,LBLUE,BLUE,False); f.line(320,y+35,360,y+35,INK,2); y+=84
f.line(360,49,360,301,INK,2); f.arrow(360,165,400,165,INK,2.5)
f.tbox(400,130,170,70,['작업','대기열'],24,LGREEN,GREEN,True)
f.arrow(570,165,610,165,INK,2.5)
f.tbox(610,115,170,100,['결과 · 로그','저장소','(z440)'],24,LGOLD,GOLD,True)
fin(f,'4-1')
vflow('5-1',['원본 (읽기 전용)','정리본 (형식 통일)','로컬 데이터베이스','분석 입력'],[B,B,G_,Y])
vflow('6-1',['구조 확보 · 예측','수용체 준비','도킹','재점수화','분자동역학','후보 판정'],[B,B,G_,G_,Y,R])
# 7-1 깔때기
STG=['후보 생성 · 열거','성질 · ADMET 필터','도킹 · 점수화','분자동역학 · 자유에너지','합성 · 시험 후보']
FL=[B,B,G_,Y,R]
f=Fig('fig7-1.svg',14+5*44+4*26+20); y=14
for i,s in enumerate(STG):
    w=700-i*100; f.tbox(400-w/2,y,w,44,[s],24,FL[i][0],FL[i][1],True)
    if i<4: f.arrow(400,y+44,400,y+70,INK,2.5)
    y+=70
fin(f,'7-1')
vflow('8-1',['질문','색인 검색','근거 문장 추출','답 생성','DOI 대조','근거 표시 답'],[B,B,B,G_,Y,R])
vflow('9-1',['설정 · 시드 · 환경 고정','입력 자료 + 해시','작업 흐름 실행','결과 + 실행 이력','저장소 기록 (git)'],[B,B,G_,Y,R])
