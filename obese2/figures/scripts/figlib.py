# -*- coding: utf-8 -*-
"""생물·의학 대중서 그림 생성 라이브러리 (좌표 명시 SVG) — biofig_kit (원본: 「인삼과 암치유」 2026-09)

좌표계: viewBox 폭 800, 출력 폭 120mm  →  1단위 = 0.15mm = 0.425pt
  · 글자 최소 22단위(≈9.4pt).  book1.md 기준(700폭에서 18 = 8.2pt)보다 엄격하다.
  · 제목 26 이상, 수치 강조 28 이상 권장.
모든 글자의 예상 경계상자를 기록해 두었다가 save() 때
  ① 글자↔글자 겹침  ② 캔버스 밖 넘침  ③ 상자 넘침(tbox)  ④ 글자 위에 나중에 그린 불투명 도형
을 검사해 WARN에 쌓는다.  report()가 0건이어야 완성이다.

색 규칙(책 전체 통일, 흑백 인쇄에서도 명도 차로 구분):
  정상세포·일반구조 = BLUE 계열,  암세포 = WARM 계열,  면역세포 = GREEN 계열,
  인삼·진세노사이드 = GOLD 계열,  보조선·주석 = GRAY
"""
import os, math

UNIT_PT = 120.0 / 800 * 72 / 25.4
MIN_FS = 22
FONT = "'Noto Sans CJK KR',sans-serif"

INK    = '#1b2a33'
BLUE   = '#2f5f7a'; LBLUE = '#dbe7ee'; FILL = '#eef3f6'
GRAY   = '#7a8a92'; LGRAY = '#f2f4f5'; MGRAY = '#c9d1d5'
WARM   = '#9c4f2e'; LWARM = '#f3e3da'; MWARM = '#d9a48a'
GREEN  = '#3b6a4f'; LGREEN = '#e1ede5'; MGREEN = '#9cc0a9'
GOLD   = '#8a6a2c'; LGOLD = '#f3ead6'; MGOLD = '#d6bd84'
WHITE  = '#ffffff'

WARN = []


def _w(s, fs):
    """문자열 렌더링 폭 추정(단위). 한글·한자=1.0em, 영문·숫자=0.58em, 좁은 기호=0.32em"""
    t = 0.0
    for c in s:
        o = ord(c)
        if o > 0x1100 and not (0x2000 <= o <= 0x206f):
            t += 1.0
        elif c == ' ':
            t += 0.32
        elif c in 'ilj.,·|()[]:;\'"!':
            t += 0.32
        elif c in 'mwMW':
            t += 0.85
        else:
            t += 0.58
    return t * fs


def _ov(a, b):
    ix = min(a[2], b[2]) - max(a[0], b[0])
    iy = min(a[3], b[3]) - max(a[1], b[1])
    if ix <= 0 or iy <= 0:
        return 0.0
    sa = (a[2] - a[0]) * (a[3] - a[1]); sb = (b[2] - b[0]) * (b[3] - b[1])
    return ix * iy / max(1e-6, min(sa, sb))


class Fig:
    def __init__(self, name, h, w=800):
        self.name, self.w, self.h = name, w, h
        self.parts = []
        self.texts = []      # (box, s, order)
        self.shapes = []     # (box, order)  불투명 도형
        self.order = 0
        self.minfs = 999

    def _add(self, svg, box=None, opaque=False):
        self.parts.append(svg)
        if box and opaque:
            self.shapes.append((box, self.order))
        self.order += 1

    # ── 기본 도형 ──────────────────────────────────────────────
    def rect(self, x, y, w, h, fill=FILL, stroke=BLUE, sw=2, rx=8, dash=None, opacity=1):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        op = f' opacity="{opacity}"' if opacity != 1 else ''
        self._add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" '
                  f'stroke="{stroke}" stroke-width="{sw}"{d}{op}/>',
                  (x, y, x + w, y + h), fill not in ('none', '') and opacity >= .5)

    def circle(self, cx, cy, r, fill=FILL, stroke=BLUE, sw=2, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        self._add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>',
                  (cx - r, cy - r, cx + r, cy + r), fill not in ('none', ''))

    def ellipse(self, cx, cy, rx, ry, fill=FILL, stroke=BLUE, sw=2, rot=0):
        t = f' transform="rotate({rot} {cx} {cy})"' if rot else ''
        self._add(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" '
                  f'stroke-width="{sw}"{t}/>', (cx - rx, cy - ry, cx + rx, cy + ry),
                  fill not in ('none', '') and not rot)

    def line(self, x1, y1, x2, y2, stroke=GRAY, sw=2, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        self._add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def path(self, d, stroke=BLUE, sw=2.5, fill='none', dash=None, opacity=1):
        da = f' stroke-dasharray="{dash}"' if dash else ''
        op = f' opacity="{opacity}"' if opacity != 1 else ''
        self._add(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" '
                  f'stroke-linejoin="round" stroke-linecap="round"{da}{op}/>')

    def poly(self, pts, fill='none', stroke=BLUE, sw=2.5, close=False):
        s = ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts)
        tag = 'polygon' if close else 'polyline'
        self._add(f'<{tag} points="{s}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>')

    def raw(self, svg):
        """직접 작성한 SVG 조각(겹침 검사 대상 아님 — 글자는 반드시 text()로 넣을 것)"""
        self._add(svg)

    def text(self, x, y, s, fs=24, weight=400, anchor='middle', color=INK, italic=False, check=True):
        if fs < MIN_FS:
            WARN.append(f'{self.name}: 글자 크기 {fs} < {MIN_FS} «{s[:20]}»')
            fs = MIN_FS
        self.minfs = min(self.minfs, fs)
        it = ' font-style="italic"' if italic else ''
        esc = s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        w = _w(s, fs)
        x0 = x - w / 2 if anchor == 'middle' else (x - w if anchor == 'end' else x)
        box = (x0, y - fs * 0.80, x0 + w, y + fs * 0.18)
        if check:
            self.texts.append((box, s, self.order))
        self._add(f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{fs}" font-weight="{weight}" '
                  f'text-anchor="{anchor}" fill="{color}"{it}>{esc}</text>')
        return box

    def lines(self, x, y, arr, fs=24, lead=1.32, **kw):
        """여러 줄 글자. arr: 문자열 리스트. 반환: 마지막 줄 y"""
        for i, s in enumerate(arr):
            self.text(x, y + i * fs * lead, s, fs, **kw)
        return y + (len(arr) - 1) * fs * lead

    def arrow(self, x1, y1, x2, y2, stroke=BLUE, sw=2.5, dash=None, head=10):
        ang = math.atan2(y2 - y1, x2 - x1)
        bx, by = x2 - head * math.cos(ang), y2 - head * math.sin(ang)
        self.line(x1, y1, bx, by, stroke, sw, dash)
        p2 = (x2 - head * 1.7 * math.cos(ang - 0.42), y2 - head * 1.7 * math.sin(ang - 0.42))
        p3 = (x2 - head * 1.7 * math.cos(ang + 0.42), y2 - head * 1.7 * math.sin(ang + 0.42))
        pts = ' '.join(f'{px:.1f},{py:.1f}' for px, py in ((x2, y2), p2, p3))
        self._add(f'<polygon points="{pts}" fill="{stroke}"/>')

    def carrow(self, x1, y1, cx, cy, x2, y2, stroke=BLUE, sw=2.5, dash=None, head=10):
        """2차 베지어 곡선 화살표"""
        da = f' stroke-dasharray="{dash}"' if dash else ''
        ang = math.atan2(y2 - cy, x2 - cx)
        bx, by = x2 - head * math.cos(ang), y2 - head * math.sin(ang)
        self._add(f'<path d="M{x1},{y1} Q{cx},{cy} {bx:.1f},{by:.1f}" fill="none" stroke="{stroke}" '
                  f'stroke-width="{sw}"{da}/>')
        p2 = (x2 - head * 1.7 * math.cos(ang - 0.42), y2 - head * 1.7 * math.sin(ang - 0.42))
        p3 = (x2 - head * 1.7 * math.cos(ang + 0.42), y2 - head * 1.7 * math.sin(ang + 0.42))
        pts = ' '.join(f'{px:.1f},{py:.1f}' for px, py in ((x2, y2), p2, p3))
        self._add(f'<polygon points="{pts}" fill="{stroke}"/>')

    def inhibit(self, x1, y1, x2, y2, stroke=WARM, sw=2.5, bar=14):
        """억제 표시(⊣): 선 끝에 가로막대"""
        ang = math.atan2(y2 - y1, x2 - x1)
        self.line(x1, y1, x2, y2, stroke, sw)
        px, py = -math.sin(ang) * bar, math.cos(ang) * bar
        self.line(x2 - px, y2 - py, x2 + px, y2 + py, stroke, sw + 1)

    # ── 조합 도형 ──────────────────────────────────────────────
    def tbox(self, x, y, w, h, lines, fs=24, fill=FILL, stroke=BLUE, sw=2, rx=8,
             color=INK, weight=400, lead=1.3, dash=None, first_bold=False):
        """글자가 든 상자. 폭·높이 초과를 경고한다(글자 폭을 먼저 계산하고 상자를 정할 것)."""
        self.rect(x, y, w, h, fill, stroke, sw, rx, dash)
        n = len(lines)
        total = (n - 1) * fs * lead
        y0 = y + h / 2 - total / 2 + fs * 0.35
        for i, ln in enumerate(lines):
            wgt = 700 if (first_bold and i == 0) else weight
            if _w(ln, fs) > w - 12:
                WARN.append(f'{self.name}: 상자 폭 넘침 «{ln}» {_w(ln, fs):.0f} > {w - 12}')
            self.text(x + w / 2, y0 + i * fs * lead, ln, fs, wgt, 'middle', color)
        if total + fs > h - 8:
            WARN.append(f'{self.name}: 상자 높이 넘침 «{lines[0]}» {total + fs:.0f} > {h - 8}')

    def callout(self, px, py, lx, ly, lines, fs=22, anchor='start', color=INK, dot=True, lead=1.28,
                weight=400, sub=None):
        """리더선 라벨: 부위(px,py)에서 라벨(lx,ly)까지 가는 회색 선.
           라벨은 도형 바깥 여백에 둔다. anchor='start'면 라벨 왼쪽 끝이 lx, 'end'면 오른쪽 끝이 lx.
           sub: 둘째 줄에 작은 글씨(원어 등)"""
        arr = list(lines) if isinstance(lines, (list, tuple)) else [lines]
        gap = 6
        ex = lx - gap if anchor == 'start' else lx + gap
        self.line(px, py, ex, ly - fs * 0.32, GRAY, 1.2)
        if dot:
            self._add(f'<circle cx="{px}" cy="{py}" r="3.2" fill="{GRAY}"/>')
        yy = ly
        for i, s in enumerate(arr):
            self.text(lx, yy, s, fs, 700 if (i == 0 and weight == 700) else weight, anchor, color)
            yy += fs * lead
        if sub:
            self.text(lx, yy - fs * lead + fs * 1.15 + 4, sub, MIN_FS, 400, anchor, GRAY)

    def badge(self, cx, cy, s, r=17, fill=INK, color=WHITE, fs=22):
        """순서 번호 원(①②③ 대용)"""
        self.circle(cx, cy, r, fill, fill, 1)
        self.text(cx, cy + fs * 0.35, s, fs, 700, 'middle', color, check=False)

    def hbar(self, x, y, w, h, frac, fill=BLUE, bg=LGRAY):
        self.rect(x, y, w, h, bg, MGRAY, 1, 3)
        if frac > 0:
            self.rect(x, y, max(2, w * frac), h, fill, fill, 1, 3)

    def axis_label(self, x, y, s, fs=22, color=GRAY):
        """세로축 제목(90도 회전) — 겹침 검사 대상에서 제외"""
        esc = s.replace('&', '&amp;').replace('<', '&lt;')
        self._add(f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{fs}" text-anchor="middle" '
                  f'fill="{color}" transform="rotate(-90 {x} {y})">{esc}</text>')

    # ── 저장 ──────────────────────────────────────────────────
    def _check(self):
        T = self.texts
        for i in range(len(T)):
            for j in range(i + 1, len(T)):
                r = _ov(T[i][0], T[j][0])
                if r > 0.06:
                    WARN.append(f'{self.name}: 글자 겹침 {r:.0%} «{T[i][1][:16]}» ↔ «{T[j][1][:16]}»')
        for box, s, o in T:
            if box[0] < 2 or box[2] > self.w - 2 or box[1] < 2 or box[3] > self.h - 2:
                WARN.append(f'{self.name}: 캔버스 넘침 «{s[:20]}» x{box[0]:.0f}~{box[2]:.0f} y{box[1]:.0f}~{box[3]:.0f}')
            for sb, so in self.shapes:
                if so > o and _ov(box, sb) > 0.25:
                    WARN.append(f'{self.name}: 글자가 나중 도형에 가려짐 «{s[:20]}»')

    def save(self, outdir):
        self._check()
        mm_h = self.h / self.w * 120
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" '
               f'width="120mm" height="{mm_h:.1f}mm">'
               f'<rect x="0" y="0" width="{self.w}" height="{self.h}" fill="#ffffff"/>'
               + ''.join(self.parts) + '</svg>')
        os.makedirs(outdir, exist_ok=True)
        open(os.path.join(outdir, self.name), 'w', encoding='utf-8').write(svg)
        return self.name, self.minfs * UNIT_PT


def point_in_poly(x, y, poly):
    """점이 다각형(꼭짓점 목록) 안에 있는가 — 광선 교차법"""
    inside, n = False, len(poly)
    for i in range(n):
        x1, y1 = poly[i]; x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            inside = not inside
    return inside


def contain(figname, what, poly, pts, margin_pts=()):
    """포함 검사: 세포 소기관처럼 '어떤 윤곽 안에 있어야 하는' 도형의 점들이 윤곽(poly) 밖으로 나가면 경고.
       poly: 윤곽 다각형(예: 세포막 안쪽선의 점들), pts: 검사할 점들(소기관 외곽점·소낭 중심±반지름 등).
       예) contain('fig02_1.svg', '골지체', cell_inner_pts, golgi_pts)"""
    bad = [(x, y) for x, y in pts if not point_in_poly(x, y, poly)]
    if bad:
        WARN.append(f'{figname}: 포함 위반 «{what}» 점 {len(bad)}개가 윤곽 밖 (예: {bad[0][0]:.0f},{bad[0][1]:.0f})')
    return not bad


def report(prefix=''):
    W = [w for w in WARN if w.startswith(prefix)] if prefix else WARN
    if W:
        print(f'⚠ 경고 {len(W)}건:')
        for w in W:
            print('  ', w)
    else:
        print('✓ 겹침·넘침·글자크기 경고 0건')
    return len(W)
