# -*- coding: utf-8 -*-
"""biofig_kit 사용 예 — 세 가지 대표 그림을 만든다.
실행(책 프로젝트 루트에서):  python3 <kit>/example_figs.py   → fig/ex_cell.svg, fig/ex_forest.svg, fig/ex_membrane.svg
그다음:  python3 <kit>/check_figs.py fig/ex_*.svg   →  <kit>/preview_figs.sh fig/ex_*.svg   → preview/*.png 눈 검수
"""
import os, sys, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F
from figlib import Fig, INK, BLUE, LBLUE, GRAY, WARM, LWARM, GREEN, GOLD, WHITE
import shapes as S

OUT = os.path.join(os.getcwd(), 'fig')


# ── 예 1. 세포 단면: 곡선 윤곽 + 소기관 + 바깥 라벨(리더선) + 포함 검사 ──────────────
def ex_cell():
    f = Fig('ex_cell.svg', 520)
    CX, CY, RX, RY = 400, 262, 190, 200
    WOB = (0.02, 0.03, 0.0, -0.02, -0.03, 0.01, 0.03, 0.01, -0.02, -0.03, 0.0, 0.02)
    f.path(S.smooth(S.blob_pts(CX, CY, RX, RY, WOB, 12)), BLUE, 3.2, '#f2f7f9')          # 세포막(바깥선)
    f.path(S.smooth(S.blob_pts(CX, CY, RX, RY, WOB, 12, scale=0.972)), '#86a8bb', 1.3)   # 막 두께(안쪽선)
    inner = S.outline(CX, CY, RX, RY, WOB, 12, scale=0.965)                              # 포함 검사 윤곽
    # 핵(이중막)
    f.path(S.smooth(S.blob_pts(380, 262, 80, 70, (0.02, 0, -0.02, 0.01, 0.02, 0, -0.01, 0.01), 8)), BLUE, 2.2, '#a9c3d2')
    f.path(S.smooth(S.blob_pts(380, 262, 80, 70, (0.02, 0, -0.02, 0.01, 0.02, 0, -0.01, 0.01), 8, scale=0.93)), BLUE, 1.4, '#dce8ef')
    f.circle(395, 250, 18, '#56809a', '#24495e', 1.6)                                    # 핵소체
    # 미토콘드리아 2개 — mito()가 실제 윤곽점을 돌려주므로 그대로 포함 검사
    m1 = S.mito(f, 300, 140, -25, L=86, W=40)
    m2 = S.mito(f, 470, 400, -15, L=84, W=38)
    F.contain(f.name, '미토콘드리아', inner, m1 + m2)
    # 라벨: 왼쪽 열(오른쪽 정렬)·오른쪽 열(왼쪽 정렬)로 세로 정렬, 리더선은 교차하지 않게 위→아래 순서 유지
    mp = S.on_blob(CX, CY, RX, RY, WOB, 12, 215)
    f.callout(mp[0], mp[1], 170, 90, ['세포막'], 24, 'end', weight=700, sub='cell membrane')
    f.callout(272, 152, 170, 210, ['미토콘드리아'], 24, 'end', weight=700, sub='mitochondria')
    f.callout(395, 250, 640, 150, ['핵소체'], 24, 'start', weight=700, sub='nucleolus')
    f.callout(430, 300, 640, 290, ['핵'], 24, 'start', weight=700, sub='nucleus')
    return f.save(OUT)


# ── 예 2. 숲그림(메타분석·코호트 결과): 로그축 + 신뢰구간 + 유의/비유의 표지 ────────
def ex_forest():
    rows = [('연구 A (메타분석)', 'dia', 0.84, 0.76, 0.92, True),
            ('연구 B (코호트)', 'sq', 0.83, 0.46, 1.51, False),
            ('연구 C (코호트)', 'sq', 2.15, 1.08, 4.25, True)]
    top, rh = 40, 70
    f = Fig('ex_forest.svg', top + rh * len(rows) + 110)
    lo, hi, x0, w = 0.25, 8, 400, 360
    yb = top + rh * len(rows)
    for i, (lab, kind, e, a, b, sig) in enumerate(rows):
        y = top + rh * i + rh / 2
        f.text(20, y - 4, lab, 24, 700, 'start')
        f.text(20, y + 24, f'{e:.2f} ({a:.2f}–{b:.2f})', 22, 400, 'start', GRAY)
        S.ci_row(f, y, e, a, b, lo, hi, x0, w, kind, sig, BLUE)
    S.log_axis(f, lo, hi, x0, w, yb, (0.25, 0.5, 1, 2, 4, 8), ytop=top - 10)
    f.text(S.logx(1, lo, hi, x0, w) - 12, yb + 72, '← 위험 낮음', 22, 400, 'end', GRAY)
    f.text(S.logx(1, lo, hi, x0, w) + 12, yb + 72, '위험 높음 →', 22, 400, 'start', GRAY)
    return f.save(OUT)


# ── 예 3. 세포막 모식도: 인지질 이중층 + 수용체 + 약·성분 표지 + 순서 번호 ────────
def ex_membrane():
    f = Fig('ex_membrane.svg', 400)
    S.bilayer_h(f, 40, 760, 200)                                  # 세포막(가로)
    f.text(40, 170, '세포 밖', 22, 400, 'start', GRAY)
    f.text(40, 262, '세포 안', 22, 400, 'start', GRAY)
    S.receptor(f, 400, 190, 1.4)                                  # 막에 박힌 수용체
    S.drug(f, 250, 110, 11)
    S.ginsenoside_icon(f, 560, 110, 9)
    f.arrow(262, 122, 380, 170, INK, 2.2)                         # 화살표는 글자 상자 밖에서 시작·끝
    f.badge(320, 122, '1')
    F.contain(f.name, '수용체', [(360, 150), (440, 150), (440, 240), (360, 240)], [(400, 190), (400, 215)])
    f.callout(400, 225, 560, 330, ['수용체', '(자물쇠)'], 22, 'start')
    f.callout(250, 110, 120, 60, ['약 분자'], 22, 'end')
    f.callout(575, 100, 690, 60, ['성분'], 22, 'start')
    return f.save(OUT)


if __name__ == '__main__':
    for fn in (ex_cell, ex_forest, ex_membrane):
        name, minpt = fn()
        print(f'{name}: 최소 글자 {minpt:.1f}pt')
    F.report()
