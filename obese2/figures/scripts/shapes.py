# -*- coding: utf-8 -*-
"""biofig_kit/shapes.py — 생물·의학 그림용 도형 부품 모음
「인삼과 암치유」(2026-09)의 그림 스크립트 8종(figs_w1~w8.py)에서 다시 쓸 만한 부품을 모았다.
모든 부품은 figlib.Fig 객체 f 에 그린다. 글자는 넣지 않는다(라벨은 f.callout()으로 도형 밖에).

  곡선      smooth, smooth_open, sample_open, blob_pts, on_blob, blob, capsule, polar, sector
  배치      g_open/g_close(이동·회전 묶음), arc_arrow
  세포      mito(미토콘드리아), cancer_cell(암세포), immune_cell(면역세포), rbc(적혈구),
            endo_wall(혈관 내피 한 줄), lipid·bilayer_h·bilayer_v(인지질 이중층), bacterium(세균)
  분자      hexv, dammarane(스테로이드·트리테르펜 4고리), draw_rings, sugar·chain(당 사슬),
            ginsenoside_icon(작은 진세노사이드 표지), drug(약 분자), receptor(수용체 컵)
  식물      leaflet, compound_leaf(손바닥 겹잎)
  기관      tube(관 모양: 혈관·장·카테터)
  통계      logx, log_axis, marker, ci_row(숲그림), person(사람 아이콘)
"""
import math, random
from figlib import (INK, BLUE, LBLUE, FILL, GRAY, LGRAY, MGRAY, WARM, LWARM, MWARM,
                    GREEN, LGREEN, MGREEN, GOLD, LGOLD, MGOLD, WHITE)

# 보조 명도 단계(같은 색상의 명도 3~4단계로 입체감; 흑백에서도 20% 이상 차이)
MBLUE, DBLUE = '#9dbccd', '#1f4459'
DWARM = '#6e3620'
DGOLD = '#b08a3e'
DRUG = '#2b3a42'


def P(x, y):
    return f'{x:.1f},{y:.1f}'


# ── 곡선 ──────────────────────────────────────────────────────
def smooth(pts, closed=True, k=1.0):
    """점들을 지나는 매끈한 곡선(Catmull-Rom → 3차 베지어) path d. 세포 윤곽·핵·주머니 모양의 기본."""
    n = len(pts)
    if n < 3:
        return 'M' + ' L'.join(P(x, y) for x, y in pts)
    d = [f'M{P(*pts[0])}']
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[i]
        p1, p2 = pts[i], pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else pts[(i + 1) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6 * k, p1[1] + (p2[1] - p0[1]) / 6 * k)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6 * k, p2[1] - (p3[1] - p1[1]) / 6 * k)
        d.append(f'C{P(*c1)} {P(*c2)} {P(*p2)}')
    if closed:
        d.append('Z')
    return ' '.join(d)


def smooth_open(pts):
    return smooth(pts, closed=False)


def sample_open(pts, step=4.0):
    """Catmull-Rom 곡선 위 점들(일정 간격) — 주름·세균·리보솜을 곡선을 따라 배치할 때"""
    Q = [pts[0]] + list(pts) + [pts[-1]]
    out = []
    for i in range(1, len(Q) - 2):
        p0, p1, p2, p3 = Q[i - 1], Q[i], Q[i + 1], Q[i + 2]
        n = max(2, int(math.dist(p1, p2) / step))
        for k in range(n):
            t = k / n; t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2
                                    + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in (0, 1)))
    out.append(pts[-1])
    return out


def blob_pts(cx, cy, rx, ry, wob=(), n=16, rot=0.0, scale=1.0):
    """타원 둘레 n점에 반지름 흔들림(wob: 비율 목록, 길이 n 권장)을 준 점들.
       ⚠ wob 길이와 n을 다르게 주면 흔들림이 반복되어 모양이 달라진다. 윤곽을 촘촘히 뽑으려면 on_blob()을 쓸 것."""
    pts = []
    r = math.radians(rot)
    for i in range(n):
        a = 2 * math.pi * i / n
        w = 1 + (wob[i % len(wob)] if wob else 0)
        x, y = rx * scale * w * math.cos(a), ry * scale * w * math.sin(a)
        pts.append((cx + x * math.cos(r) - y * math.sin(r), cy + x * math.sin(r) + y * math.cos(r)))
    return pts


def blob_r(wob, n, a):
    t = (a % (2 * math.pi)) / (2 * math.pi) * n
    i = int(t) % n; fr = t - int(t)
    w0 = wob[i % len(wob)] if wob else 0; w1 = wob[(i + 1) % len(wob)] if wob else 0
    g = (1 - math.cos(fr * math.pi)) / 2
    return 1 + w0 * (1 - g) + w1 * g


def on_blob(cx, cy, rx, ry, wob, n, deg, scale=1.0):
    """blob_pts(n점) 윤곽 위, 각도 deg의 점(흔들림 보간). 리더선 끝점·포함 검사 윤곽에 쓴다."""
    a = math.radians(deg); w = blob_r(wob, n, a) * scale
    return (cx + rx * w * math.cos(a), cy + ry * w * math.sin(a))


def outline(cx, cy, rx, ry, wob, n, scale=1.0, step=2):
    """포함 검사용 윤곽 다각형(2도 간격) — figlib.contain()에 넘긴다"""
    return [on_blob(cx, cy, rx, ry, wob, n, d, scale) for d in range(0, 360, step)]


def blob(cx, cy, r, seed=0, n=8, jit=0.13, sx=1.0, sy=1.0):
    """무작위 흔들림 덩어리 path(작은 세포·면역세포 핵 등). seed로 모양 고정"""
    rnd = random.Random(seed)
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n + rnd.uniform(-0.15, 0.15)
        rr = r * (1 + rnd.uniform(-jit, jit))
        pts.append((cx + rr * math.cos(a) * sx, cy + rr * math.sin(a) * sy))
    return smooth(pts)


def capsule(L, W):
    """길이 L, 폭 W 캡슐(원점 중심, 가로) path — 미토콘드리아·세균·알약"""
    r = W / 2; h = L / 2 - r
    return (f'M{-h:.1f},{-r:.1f} L{h:.1f},{-r:.1f} A{r:.1f},{r:.1f} 0 0 1 {h:.1f},{r:.1f} '
            f'L{-h:.1f},{r:.1f} A{r:.1f},{r:.1f} 0 0 1 {-h:.1f},{-r:.1f} Z')


def capsule_outline(x, y, rot, L, W):
    """캡슐 실제 윤곽점(둥근 끝 포함) — 포함 검사용. 바운딩 사각형 모서리를 쓰면 과잉 경고가 난다."""
    a = math.radians(rot); r = W / 2; h = L / 2 - r
    loc = [(sx * h + r * math.cos(math.radians(d)) * (1 if sx > 0 else -1), r * math.sin(math.radians(d)))
           for sx in (-1, 1) for d in range(-90, 91, 20)]
    loc += [(t * h, s * r) for t in (-0.5, 0, 0.5) for s in (-1, 1)]
    return [(x + u * math.cos(a) - v * math.sin(a), y + u * math.sin(a) + v * math.cos(a)) for u, v in loc]


def polar(cx, cy, r, deg):
    a = math.radians(deg)
    return (cx + r * math.cos(a), cy + r * math.sin(a))


def sector(cx, cy, ro, ri, a0, a1):
    """도넛 부채꼴 path(각도: 도, 시계 방향) — 세포주기·원그래프"""
    large = 1 if (a1 - a0) > 180 else 0
    p1, p2 = polar(cx, cy, ro, a0), polar(cx, cy, ro, a1)
    p3, p4 = polar(cx, cy, ri, a1), polar(cx, cy, ri, a0)
    return (f'M{P(*p1)} A{ro},{ro} 0 {large} 1 {P(*p2)} L{P(*p3)} A{ri},{ri} 0 {large} 0 {P(*p4)} Z')


def g_open(f, x, y, rot=0, s=1.0):
    """원점 기준으로 그린 부품을 (x,y)로 옮기고 rot도 회전·s배 확대 — 반드시 g_close와 짝"""
    f.raw(f'<g transform="translate({x:.1f},{y:.1f}) rotate({rot}) scale({s})">')


def g_close(f):
    f.raw('</g>')


def arc_arrow(f, cx, cy, r, a0, a1, color=GRAY, sw=2.2, head=9):
    """시계 방향 원호 화살표(순환 과정)"""
    large = 1 if (a1 - a0) > 180 else 0
    p1, pe = polar(cx, cy, r, a0), polar(cx, cy, r, a1 - 2.5)
    f.raw(f'<path d="M{P(*p1)} A{r},{r} 0 {large} 1 {P(*pe)}" fill="none" stroke="{color}" stroke-width="{sw}"/>')
    tip = polar(cx, cy, r, a1); a = math.radians(a1)
    tx, ty = -math.sin(a), math.cos(a); nx, ny = math.cos(a), math.sin(a)
    b = (tip[0] - tx * head * 1.6, tip[1] - ty * head * 1.6)
    pts = [tip, (b[0] + nx * head * 0.7, b[1] + ny * head * 0.7), (b[0] - nx * head * 0.7, b[1] - ny * head * 0.7)]
    f.raw('<polygon points="' + ' '.join(P(*p) for p in pts) + f'" fill="{color}"/>')


# ── 세포 ──────────────────────────────────────────────────────
def mito(f, x, y, rot, L=96, W=44, n_cr=5, outer='#e6eaec', matrix='#aebbc2', line='#44545d'):
    """미토콘드리아: 바깥막·안쪽막(이중막) + 안쪽막이 접힌 크리스타 주름(위아래 번갈아)"""
    g_open(f, x, y, rot)
    f.raw(f'<path d="{capsule(L, W)}" fill="{outer}" stroke="{line}" stroke-width="2"/>')
    f.raw(f'<path d="{capsule(L - 9, W - 9)}" fill="{matrix}" stroke="{line}" stroke-width="1.3"/>')
    ih = (W - 9) / 2; span = L - 9 - (W - 9)
    for i in range(n_cr):
        cx = -span / 2 + span * (i + 0.5) / n_cr
        top = (i % 2 == 0); y0 = -ih if top else ih
        y1 = y0 + ih * 1.35 if top else y0 - ih * 1.35; w = 3.2
        d = (f'M{cx - w:.1f},{y0:.1f} C{cx - w:.1f},{(y0 + y1) / 2:.1f} {cx - w - 2:.1f},{y1:.1f} {cx:.1f},{y1:.1f} '
             f'C{cx + w + 2:.1f},{y1:.1f} {cx + w:.1f},{(y0 + y1) / 2:.1f} {cx + w:.1f},{y0:.1f}')
        f.raw(f'<path d="{d}" fill="{outer}" stroke="{line}" stroke-width="1.2"/>')
    g_close(f)
    return capsule_outline(x, y, rot, L, W)


def cancer_cell(f, cx, cy, rx, ry, seed=1, n=22, rough=0.09, nuc=0.5, rot=0, line=WARM, fill=LWARM,
                nfill=MWARM, sw=2.4, nucleoli=3):
    """암세포: 울퉁불퉁한 윤곽(느린 굴곡 + 잔돌기), 크고 불규칙한 핵, 여러 개의 핵소체. 반환: 핵 중심"""
    rnd = random.Random(seed); m = n * 2
    ph1, ph2 = rnd.uniform(0, 6.3), rnd.uniform(0, 6.3)
    wob = [rough * (0.55 * math.sin(6 * math.pi * i / m + ph1) + 0.3 * math.sin(10 * math.pi * i / m + ph2)
                    + 0.35 * rnd.uniform(-1, 1) + (0.35 if i % 4 == 0 else 0)) for i in range(m)]
    f.path(smooth(blob_pts(cx, cy, rx, ry, wob, m, rot)), stroke=line, sw=sw, fill=fill)
    nw = [0.12 * math.sin(4 * math.pi * i / 14 + ph2) + rnd.uniform(-0.08, 0.08) for i in range(14)]
    ncx, ncy = cx + rx * rnd.uniform(-0.08, 0.08), cy + ry * rnd.uniform(-0.08, 0.08)
    f.path(smooth(blob_pts(ncx, ncy, rx * nuc, ry * nuc * 0.9, nw, 14, rot + 20)), stroke=line, sw=1.8, fill=nfill)
    for _ in range(nucleoli):
        a = rnd.uniform(0, 2 * math.pi); r = rnd.uniform(0.1, 0.45)
        f.raw(f'<ellipse cx="{ncx + rx * nuc * r * math.cos(a):.1f}" cy="{ncy + ry * nuc * 0.8 * r * math.sin(a):.1f}" '
              f'rx="{max(3, rx * 0.07):.1f}" ry="{max(2.5, ry * 0.06):.1f}" fill="{WARM}"/>')
    return (ncx, ncy)


def immune_cell(f, x, y, r=15, seed=0):
    """면역세포: 위족이 난 울퉁불퉁한 몸 + 여러 갈래 핵(초록 계열)"""
    f.path(blob(x, y, r, seed, n=9, jit=0.22), GREEN, 1.8, MGREEN)
    f.path(blob(x - 3, y + 1, r * 0.33, seed + 7, n=6, jit=0.25), GREEN, 1, GREEN)
    f.path(blob(x + 5, y - 3, r * 0.28, seed + 9, n=6, jit=0.25), GREEN, 1, GREEN)


def rbc(f, x, y, face=False, rot=0):
    """적혈구: 가운데가 오목한 원반(옆모습, face=True면 정면). 회색 계열 — 암세포(WARM)와 혼동 방지"""
    if face:
        f.raw(f'<circle cx="{x}" cy="{y}" r="12" fill="#cbd3d7" stroke="{GRAY}" stroke-width="1.4"/>'
              f'<circle cx="{x}" cy="{y}" r="5" fill="#e4e8ea"/>')
    else:
        d = ('M-16,0 C-16,-9 -9,-9.5 -4.5,-5.5 C-1.8,-3.6 1.8,-3.6 4.5,-5.5 C9,-9.5 16,-9 16,0 '
             'C16,9 9,9.5 4.5,5.5 C1.8,3.6 -1.8,3.6 -4.5,5.5 C-9,9.5 -16,9 -16,0 Z')
        f.raw(f'<path d="{d}" transform="translate({x},{y}) rotate({rot})" fill="#cbd3d7" stroke="{GRAY}" stroke-width="1.4"/>')


def endo_wall(f, x0, x1, y, th, gaps=(), top=True):
    """혈관 내피세포 한 줄: 납작하고 긴 세포 + 혈관 안쪽으로 볼록한 핵. gaps=[(xa,xb)]는 틈(전이 통로)"""
    segs, x, L = [], x0, 84
    while x < x1:
        segs.append((x, min(x + L, x1))); x += L + 4
    out = []
    for a, b in segs:
        pieces = [(a, b)]
        for g0, g1 in gaps:
            nxt = []
            for p0, p1 in pieces:
                if p1 <= g0 or p0 >= g1:
                    nxt.append((p0, p1))
                else:
                    if p0 < g0 - 8: nxt.append((p0, g0))
                    if p1 > g1 + 8: nxt.append((g1, p1))
            pieces = nxt
        out += pieces
    for a, b in out:
        if b - a < 14:
            continue
        mid = (a + b) / 2; sgn = 1 if top else -1
        yi = y + th if top else y; yo = y if top else y + th; cy_ = yi + sgn * 9
        if b - a < 56:
            f.raw(f'<rect x="{a:.1f}" y="{y:.1f}" width="{b - a:.1f}" height="{th}" rx="6" fill="#c3d6e1" '
                  f'stroke="{BLUE}" stroke-width="1.6"/>')
            continue
        d = (f'M{a + 6:.1f},{yo:.1f} L{b - 6:.1f},{yo:.1f} Q{b:.1f},{yo:.1f} {b:.1f},{(yo + yi) / 2:.1f} '
             f'Q{b:.1f},{yi:.1f} {b - 6:.1f},{yi:.1f} L{mid + 22:.1f},{yi:.1f} '
             f'C{mid + 12:.1f},{cy_:.1f} {mid - 12:.1f},{cy_:.1f} {mid - 22:.1f},{yi:.1f} '
             f'L{a + 6:.1f},{yi:.1f} Q{a:.1f},{yi:.1f} {a:.1f},{(yo + yi) / 2:.1f} Q{a:.1f},{yo:.1f} {a + 6:.1f},{yo:.1f} Z')
        f.raw(f'<path d="{d}" fill="#c3d6e1" stroke="{BLUE}" stroke-width="1.6"/>')
        f.raw(f'<ellipse cx="{mid:.1f}" cy="{yi + sgn * 1.5:.1f}" rx="12" ry="4.4" fill="#6d93a9"/>')


def lipid(f, x, y, up=True, head=MWARM, hs=WARM):
    """인지질 한 분자(크게 그릴 때): 친수성 머리(원) + 소수성 꼬리 두 가닥"""
    dy = 1 if up else -1; t0 = y + dy * 9
    for off in (-3.5, 3.5):
        f.path(f'M{x + off:.1f},{t0:.1f} C{x + off + 3:.1f},{t0 + dy * 10:.1f} {x + off - 3:.1f},'
               f'{t0 + dy * 20:.1f} {x + off:.1f},{t0 + dy * 30:.1f}', hs, 1.3)
    f.circle(x, y, 8.5, head, hs, 1.4)


def bilayer_h(f, x1, x2, y, heads=True, step=9, gap=16):
    """가로 인지질 이중층(작게 반복): 위층 y, 아래층 y+gap"""
    f.rect(x1, y, x2 - x1, gap, fill='#e9eef1', stroke='none', sw=0, rx=0)
    x = x1 + step / 2
    while x < x2:
        f.raw(f'<line x1="{x:.1f}" y1="{y + 3:.1f}" x2="{x:.1f}" y2="{y + gap / 2 - 1:.1f}" stroke="{GRAY}" stroke-width="1"/>'
              f'<line x1="{x:.1f}" y1="{y + gap / 2 + 1:.1f}" x2="{x:.1f}" y2="{y + gap - 3:.1f}" stroke="{GRAY}" stroke-width="1"/>')
        if heads:
            f.raw(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.6" fill="{MBLUE}" stroke="{BLUE}" stroke-width="0.8"/>'
                  f'<circle cx="{x:.1f}" cy="{y + gap:.1f}" r="3.6" fill="{MBLUE}" stroke="{BLUE}" stroke-width="0.8"/>')
        x += step


def bilayer_v(f, x, y1, y2, step=9, gap=16, skip=()):
    """세로 인지질 이중층. skip=[(ya,yb)] 구간은 비움(막관통 단백질 자리)"""
    y = y1 + step / 2
    while y < y2:
        if not any(a <= y <= b for a, b in skip):
            f.raw(f'<line x1="{x + 3:.1f}" y1="{y:.1f}" x2="{x + gap / 2 - 1:.1f}" y2="{y:.1f}" stroke="{GRAY}" stroke-width="1"/>'
                  f'<line x1="{x + gap / 2 + 1:.1f}" y1="{y:.1f}" x2="{x + gap - 3:.1f}" y2="{y:.1f}" stroke="{GRAY}" stroke-width="1"/>'
                  f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.6" fill="{MBLUE}" stroke="{BLUE}" stroke-width="0.8"/>'
                  f'<circle cx="{x + gap:.1f}" cy="{y:.1f}" r="3.6" fill="{MBLUE}" stroke="{BLUE}" stroke-width="0.8"/>')
        y += step


def bacterium(f, cx, cy, ang=-20):
    """막대 모양 세균(편모 포함) — 장내미생물"""
    f.raw(f'<g transform="translate({cx},{cy}) rotate({ang})">'
          f'<path d="M-30,-12 L30,-12 A12,12 0 0 1 30,12 L-30,12 A12,12 0 0 1 -30,-12 Z" '
          f'fill="{LBLUE}" stroke="{BLUE}" stroke-width="2"/>'
          f'<ellipse cx="-6" cy="0" rx="12" ry="4" fill="none" stroke="{BLUE}" stroke-width="1.2"/>'
          f'<path d="M42,0 q7,-7 14,0 t14,0" fill="none" stroke="{BLUE}" stroke-width="1.6"/>'
          f'<path d="M-42,0 q-8,8 -16,0 t-16,0" fill="none" stroke="{BLUE}" stroke-width="1.6"/></g>')


# ── 분자 ──────────────────────────────────────────────────────
def hexv(cx, cy, s):
    """꼭짓점이 위아래인 육각형 꼭짓점: 위, 오른위, 오른아래, 아래, 왼아래, 왼위"""
    h = s * math.sqrt(3) / 2
    return [(cx, cy - s), (cx + h, cy - s / 2), (cx + h, cy + s / 2), (cx, cy + s), (cx - h, cy + s / 2), (cx - h, cy - s / 2)]


def dammarane(ax, ay, s):
    """스테로이드·담마레인형 4고리 골격(6-6-6-5). A고리 중심(ax,ay), 한 변 s.
       반환: (탄소번호→좌표 사전, 고리 꼭짓점 목록 4개, 고리 중심 4개). 당·곁사슬은 C[3], C[6], C[20 방향=C[17]]에 붙인다."""
    h = s * math.sqrt(3) / 2
    A = hexv(ax, ay, s); B = hexv(ax + 2 * h, ay, s); Cr = hexv(ax + 3 * h, ay - 1.5 * s, s)
    C = {}
    C[1], C[10], C[5], C[4], C[3], C[2] = A
    C[9], C[8], C[7], C[6] = B[0], B[1], B[2], B[3]
    C[12], C[13], C[14], C[11] = Cr[0], Cr[1], Cr[2], Cr[5]
    ex, ey = C[13][0], (C[13][1] + C[14][1]) / 2
    ap = s / (2 * math.tan(math.radians(36))); R = s / (2 * math.sin(math.radians(36)))
    pcx, pcy = ex + ap, ey
    pv = lambda deg: (pcx + R * math.cos(math.radians(deg)), pcy - R * math.sin(math.radians(deg)))
    C[17], C[16], C[15] = pv(72), pv(0), pv(-72)
    rings = [A, B, Cr, [C[13], C[17], C[16], C[15], C[14]]]
    return C, rings, [(ax, ay), (ax + 2 * h, ay), (ax + 3 * h, ay - 1.5 * s), (pcx, pcy)]


def draw_rings(f, rings, stroke=INK, sw=3):
    for r in rings:
        f.poly(r, 'none', stroke, sw, close=True)


def sugar(f, cx, cy, r=15, fill=LGOLD, stroke=GOLD, dash=None, sw=2):
    """포도당(피라노스) 육각 고리 기호 + 산소 자리 점"""
    pts = [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))) for a in (30, 90, 150, 210, 270, 330)]
    d = f' stroke-dasharray="{dash}"' if dash else ''
    f.raw(f'<polygon points="{" ".join(P(*p) for p in pts)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d} stroke-linejoin="round"/>')
    f.raw(f'<circle cx="{cx + r * 0.87:.1f}" cy="{cy - r * 0.5:.1f}" r="2.6" fill="{stroke}"/>')


def chain(f, x0, y0, ang, n, r=15, gap=10, fill=LGOLD, stroke=GOLD, dash=None, bond=GOLD):
    """(x0,y0)에서 ang(도, 수학 방향) 쪽으로 당 n개를 잇는다. dash를 주면 '떨어져 나간 당'(점선) 표현. 반환: 중심 목록"""
    cs = []; ux, uy = math.cos(math.radians(ang)), -math.sin(math.radians(ang)); px, py = x0, y0
    for _ in range(n):
        cx, cy = px + ux * (gap + r), py + uy * (gap + r)
        f.line(px, py, cx - ux * r * 0.9, cy - uy * r * 0.9, bond, 2.2, dash)
        sugar(f, cx, cy, r, fill, stroke, dash); cs.append((cx, cy))
        px, py = cx + ux * r * 0.9, cy + uy * r * 0.9
    return cs


def ginsenoside_icon(f, cx, cy, s=8.5, fill=DGOLD, stroke=GOLD, halo=True):
    """작은 성분 표지(육각 3 + 오각 1 + 당 하나). halo=True: 흰 테두리를 먼저 깔아 배경과 분리(흑백 대비).
       다른 책에서는 '천연물 성분'·'스테로이드 호르몬' 표지로 색만 바꿔 쓴다."""
    h = s * math.sqrt(3); x0, y0 = cx - h * 1.25, cy + s * 0.45
    bx, by = x0 + h * 2, y0 - s * 1.5
    rings = [[(x + s * math.cos(math.radians(60 * k + 30)), y + s * math.sin(math.radians(60 * k + 30))) for k in range(6)]
             for x, y in ((x0, y0), (x0 + h, y0), (x0 + h * 1.5, y0 - s * 1.5))]
    rings.append([(bx, by - s * 0.5), (bx + s * 1.25, by - s * 0.95), (bx + s * 1.9, by + s * 0.05),
                  (bx + s * 1.2, by + s * 1.0), (bx, by + s * 0.5)])
    sug = (x0 - h * 1.25, y0 + s * 1.6)
    if halo:
        for pts in rings:
            f.poly(pts, WHITE, WHITE, 6, close=True)
        f.line(x0 - h * 0.5, y0 + s * 0.5, sug[0], sug[1], WHITE, 6)
        f.circle(sug[0], sug[1], s * 0.55 + 3, WHITE, WHITE, 1)
    for pts in rings:
        f.poly(pts, fill, stroke, 1.4, close=True)
    f.line(x0 - h * 0.5, y0 + s * 0.5, x0 - h * 1.05, y0 + s * 1.3, stroke, 1.6)
    f.circle(sug[0], sug[1], s * 0.55, fill, stroke, 1.2)


def hexagon(f, cx, cy, r, fill, stroke, sw=1.5, rot=0):
    f.poly([(cx + r * math.cos(math.radians(60 * k + rot)), cy + r * math.sin(math.radians(60 * k + rot))) for k in range(6)],
           fill, stroke, sw, close=True)


def drug(f, cx, cy, r=9):
    """약 분자 표지: 짙은 육각형 + 곁가지(진세노사이드 금색과 명도로 구분)"""
    f.line(cx + r * 0.87, cy - r * 0.5, cx + r * 1.6, cy - r * 0.95, DRUG, 2)
    hexagon(f, cx, cy, r, DRUG, DRUG, 1.2, rot=30)
    hexagon(f, cx, cy, r * 0.45, WHITE, WHITE, 0.5, rot=30)


def receptor(f, x, y, s=1.0, fill=MWARM, stroke=DWARM):
    """수용체(자물쇠) 기호: 위가 열린 컵 모양 단백질 — 리간드(열쇠)가 들어갈 자리"""
    d = (f'M{x - 20 * s:.1f},{y - 12 * s:.1f} Q{x - 23 * s:.1f},{y + 20 * s:.1f} {x:.1f},{y + 20 * s:.1f} '
         f'Q{x + 23 * s:.1f},{y + 20 * s:.1f} {x + 20 * s:.1f},{y - 12 * s:.1f} L{x + 10 * s:.1f},{y - 12 * s:.1f} '
         f'Q{x + 10 * s:.1f},{y + 7 * s:.1f} {x:.1f},{y + 7 * s:.1f} Q{x - 10 * s:.1f},{y + 7 * s:.1f} '
         f'{x - 10 * s:.1f},{y - 12 * s:.1f} Z')
    f.path(d, stroke, 1.8, fill)


# ── 식물·기관 ────────────────────────────────────────────────
def leaflet(f, x, y, ang, L, fill=MGREEN, stroke=GREEN):
    """잎 한 장(밑동 (x,y)에서 ang도 방향, 길이 L) + 주맥·측맥"""
    W = 0.36 * L
    d = (f'M0,0 C{0.2*L:.1f},{0.28*W:.1f} {0.58*L:.1f},{0.78*W:.1f} {0.9*L:.1f},{0.36*W:.1f} '
         f'Q{1.0*L:.1f},{0.12*W:.1f} {1.12*L:.1f},0 Q{1.0*L:.1f},{-0.12*W:.1f} {0.9*L:.1f},{-0.36*W:.1f} '
         f'C{0.58*L:.1f},{-0.78*W:.1f} {0.2*L:.1f},{-0.28*W:.1f} 0,0 Z')
    veins = ''.join(f'<path d="M{t*L:.1f},0 Q{(t+0.08)*L:.1f},{sg*0.32*W:.1f} {(t+0.16)*L:.1f},{sg*0.52*W:.1f}" '
                    f'fill="none" stroke="{stroke}" stroke-width="1" opacity="0.8"/>' for t in (0.25, 0.45, 0.65) for sg in (1, -1))
    f.raw(f'<g transform="translate({x:.1f},{y:.1f}) rotate({-ang:.1f})">'
          f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="1.8" stroke-linejoin="round"/>'
          f'<line x1="0" y1="0" x2="{1.02*L:.1f}" y2="0" stroke="{stroke}" stroke-width="1.3"/>{veins}</g>')


def compound_leaf(f, nx, ny, tx, ty, base_ang, Lmax, fill=MGREEN, stroke=GREEN):
    """잎자루(nx,ny)→(tx,ty) + 작은잎 5장(손바닥 모양 겹잎: 인삼·오갈피 등)"""
    f.path(f'M{P(nx, ny)} Q{P((nx + tx) / 2, min(ny, ty) - 12)} {P(tx, ty)}', GREEN, 3.2)
    for da, k in ((-70, 0.52), (70, 0.52), (-35, 0.82), (35, 0.82), (0, 1.0)):
        leaflet(f, tx, ty, base_ang + da, Lmax * k, fill, stroke)
    f.circle(tx, ty, 3.5, GREEN, GREEN, 1)


def tube(f, pts, width, fill, stroke, sw=2.0):
    """관 모양(혈관·장·요관·카테터): 굵은 테두리 선 위에 조금 가는 채움 선을 겹친다"""
    d = smooth_open(pts)
    f.path(d, stroke, width + 2 * sw, 'none')
    f.path(d, fill, width, 'none')


# ── 통계 그래프 ──────────────────────────────────────────────
def logx(v, lo, hi, x0, w):
    return x0 + (math.log(v) - math.log(lo)) / (math.log(hi) - math.log(lo)) * w


def log_axis(f, lo, hi, x0, w, y, ticks, fs=22, ytop=None, ref=1.0):
    """가로 로그축 + 눈금 + 기준선(1 = 차이 없음, 점선)"""
    f.line(x0, y, x0 + w, y, INK, 1.6)
    for t in ticks:
        xx = logx(t, lo, hi, x0, w)
        f.line(xx, y, xx, y + 8, INK, 1.6)
        f.text(xx, y + 8 + fs * 1.05, f'{t:g}', fs, 400, 'middle', INK)
    if ytop is not None and ref:
        xr = logx(ref, lo, hi, x0, w)
        f.line(xr, ytop, xr, y, GRAY, 1.6, dash='6 5')


def marker(f, kind, x, y, sig=True, color=BLUE):
    """숲그림 표지: sq=개별 연구, dia=종합(메타분석), pt=점. sig=False면 속을 비워 흑백에서도 유의·비유의 구분"""
    fill = color if sig else WHITE
    if kind == 'sq':
        f.raw(f'<rect x="{x - 8:.1f}" y="{y - 8:.1f}" width="16" height="16" fill="{fill}" stroke="{color}" stroke-width="2.4"/>')
    elif kind == 'dia':
        f.raw(f'<polygon points="{x:.1f},{y - 12:.1f} {x + 12:.1f},{y:.1f} {x:.1f},{y + 12:.1f} {x - 12:.1f},{y:.1f}" '
              f'fill="{fill}" stroke="{color}" stroke-width="2.4"/>')
    else:
        f.raw(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="{fill}" stroke="{color}" stroke-width="2.4"/>')


def ci_row(f, y, est, lo_, hi_, lo, hi, x0, w, kind='sq', sig=True, color=BLUE):
    """숲그림 한 줄: 신뢰구간 선 + 양 끝 눈금 + 추정값 표지"""
    if lo_ is not None:
        f.line(logx(lo_, lo, hi, x0, w), y, logx(hi_, lo, hi, x0, w), y, color, 3.2)
        for v in (lo_, hi_):
            xx = logx(v, lo, hi, x0, w); f.line(xx, y - 7, xx, y + 7, color, 2.4)
    marker(f, kind, logx(est, lo, hi, x0, w), y, sig, color)


def person(f, cx, cy, s=1.0, fill=LBLUE, stroke=BLUE):
    """사람 아이콘(머리 + 둥근 어깨 몸통). (cx,cy)=머리 중심 — 연구 대상자·코호트 도식"""
    r = 8.5 * s
    f.circle(cx, cy, r, fill, stroke, 1.6)
    top = cy + r + 3 * s; w = 13 * s; h = 22 * s
    f.path(f'M{cx - w:.1f},{top + h:.1f} L{cx - w:.1f},{top + 8 * s:.1f} Q{cx - w:.1f},{top:.1f} {cx - w + 8 * s:.1f},{top:.1f} '
           f'L{cx + w - 8 * s:.1f},{top:.1f} Q{cx + w:.1f},{top:.1f} {cx + w:.1f},{top + 8 * s:.1f} L{cx + w:.1f},{top + h:.1f} Z',
           stroke, 1.6, fill)
