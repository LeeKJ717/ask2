#!/usr/bin/env python3
"""완성된 SVG 파일을 독립적으로 다시 검사한다 (book1.md 1-1~1-5, 5-2).
   figlib 내부 검사와 별개로, 최종 SVG에서 직접 글자 상자를 계산한다.
   · 글자 ↔ 글자 겹침      · 캔버스 밖 넘침
   · 글자 크기 하한(폭 800 기준 21 = 700 기준 18.4)
   · 글자 위에 나중에 그려진 불투명 도형
사용: python3 tools/check_figs.py [fig/fig13_*.svg ...]   (인자 없으면 fig/*.svg 전체)
"""
import re, sys, glob, pathlib, xml.etree.ElementTree as ET

ROOT = pathlib.Path.cwd()   # 책 프로젝트 루트에서 실행: fig/*.svg 를 검사


def char_w(c):
    o = ord(c)
    if o > 0x1100 and not (0x2000 <= o <= 0x206f):
        return 1.0
    if c == ' ' or c in 'ilj.,·|()[]:;\'"!':
        return 0.32
    if c in 'mwMW':
        return 0.85
    return 0.58


def num(v, d=0.0):
    try:
        return float(v)
    except (TypeError, ValueError):
        return d


def collect(e, order, T, S):
    tag = e.tag.split('}')[-1]
    if tag == 'text':
        s = ''.join(e.itertext()).strip()
        if s:
            fs = num(e.get('font-size'), 22)
            x, y = num(e.get('x')), num(e.get('y'))
            w = sum(char_w(c) for c in s) * fs
            a = e.get('text-anchor', 'start')
            x0 = x - w / 2 if a == 'middle' else (x - w if a == 'end' else x)
            T.append(dict(s=s, fs=fs, box=(x0, y - fs * 0.8, x0 + w, y + fs * 0.18), o=order[0],
                          rot='rotate' in (e.get('transform') or '')))
        order[0] += 1
        return
    if tag in ('rect', 'circle', 'ellipse'):
        fill = (e.get('fill') or '').lower()
        if tag == 'rect':
            x, y = num(e.get('x')), num(e.get('y'))
            b = (x, y, x + num(e.get('width')), y + num(e.get('height')))
        elif tag == 'circle':
            cx, cy, r = num(e.get('cx')), num(e.get('cy')), num(e.get('r'))
            b = (cx - r, cy - r, cx + r, cy + r)
        else:
            cx, cy, rx, ry = (num(e.get(k)) for k in ('cx', 'cy', 'rx', 'ry'))
            b = (cx - rx, cy - ry, cx + rx, cy + ry)
        if fill not in ('none', '') and num(e.get('opacity'), 1) >= .5 and not e.get('transform'):
            S.append(dict(box=b, o=order[0], tag=tag))
        order[0] += 1
        return
    order[0] += 1
    for c in e:
        collect(c, order, T, S)


def ov(a, b):
    ix = min(a[2], b[2]) - max(a[0], b[0]); iy = min(a[3], b[3]) - max(a[1], b[1])
    if ix <= 0 or iy <= 0:
        return 0
    return ix * iy / max(1e-6, min((a[2] - a[0]) * (a[3] - a[1]), (b[2] - b[0]) * (b[3] - b[1])))


def check(p):
    root = ET.parse(p).getroot()
    vb = [float(v) for v in root.get('viewBox').split()]
    W, H = vb[2], vb[3]
    minfs = 18 * W / 700
    T, S = [], []
    collect(root, [0], T, S)
    out = []
    for t in T:
        if t['fs'] < minfs - 0.01:
            out.append(('작은글자', f"{t['fs']:g} < {minfs:.1f} «{t['s'][:24]}»"))
        x0, y0, x1, y1 = t['box']
        if not t['rot'] and (x0 < 0 or x1 > W or y0 < 0 or y1 > H):
            out.append(('넘침', f"«{t['s'][:24]}» x {x0:.0f}~{x1:.0f}/{W:.0f} y {y0:.0f}~{y1:.0f}/{H:.0f}"))
    for i in range(len(T)):
        for j in range(i + 1, len(T)):
            if T[i]['rot'] or T[j]['rot']:
                continue
            r = ov(T[i]['box'], T[j]['box'])
            if r > 0.06:
                out.append(('글자겹침', f"{r:.0%} «{T[i]['s'][:18]}» ↔ «{T[j]['s'][:18]}»"))
    for t in T:
        if t['rot']:
            continue
        for s in S:
            if s['o'] > t['o'] and ov(t['box'], s['box']) > 0.25:
                out.append(('가림', f"«{t['s'][:22]}» ← {s['tag']}"))
    return out


if __name__ == '__main__':
    files = sys.argv[1:] or sorted(glob.glob(str(ROOT / 'fig' / '*.svg')))
    total = 0
    for f in files:
        iss = check(f)
        if iss:
            print('──', pathlib.Path(f).name)
            for k, m in iss:
                print(f'   [{k}] {m}')
            total += len(iss)
    print(f'검사 {len(files)}개 그림 · 경고 {total}건')
    sys.exit(1 if total else 0)
