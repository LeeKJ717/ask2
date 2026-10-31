#!/usr/bin/env python3
"""조판 내용 파서: manuscript/ manuscript2/ 마크다운 + PDF 쪽별 텍스트 -> parsed/"""
import re, json, csv, glob, os, sys, subprocess, hashlib
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'parsed'); os.makedirs(OUT, exist_ok=True)
VOLS = {1: 'manuscript', 2: 'manuscript2'}
FIGRE = re.compile(r'^\*\*(그림 \d+-\d+)\.\s*(.*?)\*\*\s*(.*)$')
TABRE = re.compile(r'^\*\*(표 \d+-\d+)\.\s*(.*?)\*\*\s*(.*)$')
IMGRE = re.compile(r'^!\[.*?\]\((.*?)\)')
def parse_chapter(vol, path):
    lines = open(path, encoding='utf-8').read().split('\n')
    ch = dict(vol=vol, file=os.path.basename(path), part=None, chapter_no=None, title=None, opening=None,
              sections=[], figures=[], tables=[], key_points=[], references=[], paragraphs=[])
    sec = None; mode = 'body'; i = 0; last = None
    while i < len(lines):
        L = lines[i].rstrip()
        if L.startswith('# '): ch['part'] = L[2:].strip()
        elif L.startswith('## '):
            m = re.match(r'## 제(\d+)장\s*(.*)', L)
            ch['chapter_no'] = int(m.group(1)) if m else None; ch['title'] = m.group(2) if m else L[3:]
        elif L.startswith('> **이 장의 출발점**'): ch['opening'] = L.split('**', 2)[2].strip()
        elif L.startswith('### 이 장의 요점'): mode = 'points'; sec = None
        elif L.startswith('#### 참고문헌'): mode = 'refs'
        elif L.startswith('### '):
            mode = 'body'; sec = L[4:].strip(); ch['sections'].append(sec)
        elif FIGRE.match(L):
            m = FIGRE.match(L); f = dict(num=m.group(1), title=m.group(2), caption=m.group(3), image=None, section=sec, interpretation='')
            ch['figures'].append(f); last = ('f', f)
        elif TABRE.match(L):
            m = TABRE.match(L); t = dict(num=m.group(1), title=m.group(2), caption=m.group(3), section=sec, header=[], rows=[], interpretation='')
            ch['tables'].append(t); last = ('t', t)
        elif IMGRE.match(L) and last and last[0] == 'f': last[1]['image'] = IMGRE.match(L).group(1)
        elif L.startswith('|') and last and last[0] == 't':
            cells = [c.strip() for c in L.strip().strip('|').split('|')]
            if all(re.fullmatch(r':?-+:?', c) for c in cells): pass
            elif not last[1]['header']: last[1]['header'] = cells
            else: last[1]['rows'].append(cells)
        elif L.strip() == '': pass
        else:
            if mode == 'points': ch['key_points'].append(re.sub(r'^[-*\d.\s]+', '', L))
            elif mode == 'refs': ch['references'].append(L.strip())
            elif not L.startswith('>'):
                ch['paragraphs'].append(dict(section=sec, text=L))
                if last and not last[1]['interpretation']:
                    last[1]['interpretation'] = L; last = None
        i += 1
    return ch
def w_csv(name, rows, cols):
    with open(os.path.join(OUT, name), 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f); w.writerow(cols)
        for r in rows: w.writerow([r.get(c, '') for c in cols])
chapters = []
for vol, d in VOLS.items():
    cur = None
    for p in sorted(glob.glob(os.path.join(ROOT, d, '*장-v1.md'))):
        c = parse_chapter(vol, p)
        if c['part']: cur = c['part']
        else: c['part'] = cur
        chapters.append(c)
os.makedirs(os.path.join(OUT, 'chapters'), exist_ok=True)
for ch in chapters:
    fn = f"vol{ch['vol']}ch{ch['chapter_no']:02d}.json"
    json.dump(ch, open(os.path.join(OUT, 'chapters', fn), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
with open(os.path.join(OUT, 'all.jsonl'), 'w', encoding='utf-8') as f:
    for ch in chapters: f.write(json.dumps(ch, ensure_ascii=False) + '\n')
w_csv('chapters.csv', [dict(vol=c['vol'], chapter=c['chapter_no'], part=c['part'] or '', title=c['title'], sections=len(c['sections']),
      paragraphs=len(c['paragraphs']), figures=len(c['figures']), tables=len(c['tables']), refs=len(c['references']),
      chars=sum(len(p['text']) for p in c['paragraphs'])) for c in chapters],
      ['vol','chapter','part','title','sections','paragraphs','figures','tables','refs','chars'])
w_csv('figures.csv', [dict(vol=c['vol'], chapter=c['chapter_no'], **f) for c in chapters for f in c['figures']],
      ['vol','chapter','num','title','section','image','caption','interpretation'])
w_csv('tables.csv', [dict(vol=c['vol'], chapter=c['chapter_no'], num=t['num'], title=t['title'], section=t['section'], ncols=len(t['header']),
      nrows=len(t['rows']), header=' | '.join(t['header']), interpretation=t['interpretation']) for c in chapters for t in c['tables']],
      ['vol','chapter','num','title','section','ncols','nrows','header','interpretation'])
w_csv('tablerows.csv', [dict(vol=c['vol'], chapter=c['chapter_no'], num=t['num'], row=i + 1, **{f'c{j+1}': v for j, v in enumerate(r)})
      for c in chapters for t in c['tables'] for i, r in enumerate(t['rows'])], ['vol','chapter','num','row','c1','c2','c3','c4','c5','c6'])
w_csv('refs.csv', [dict(vol=c['vol'], chapter=c['chapter_no'], n=i + 1, ref=r) for c in chapters for i, r in enumerate(c['references'])],
      ['vol','chapter','n','ref'])
w_csv('sections.csv', [dict(vol=c['vol'], chapter=c['chapter_no'], section=s) for c in chapters for s in c['sections']], ['vol','chapter','section'])
# 쪽별 텍스트 + 목차 쪽번호
pdfs = []
for p in sorted(glob.glob('/mnt/user-data/outputs/obese2/pdf/*.pdf')): pdfs.append(p)
pages_n = {}
with open(os.path.join(OUT, 'pages.jsonl'), 'w', encoding='utf-8') as f:
    for p in pdfs:
        txt = subprocess.run(['pdftotext', '-layout', p, '-'], capture_output=True, text=True).stdout
        for n, pg in enumerate(txt.split('\f'), 1):
            if pg.strip(): f.write(json.dumps(dict(pdf=os.path.basename(p), page=n, text=pg), ensure_ascii=False) + '\n')
            pages_n[os.path.basename(p)] = n
# 장 시작 쪽 (컬러 PDF 기준)
toc = []
for p in pdfs:
    if 'color' not in p: continue
    vol = 2 if 'vol2' in p else 1
    pgs = [json.loads(l) for l in open(os.path.join(OUT, 'pages.jsonl'), encoding='utf-8') if json.loads(l)['pdf'] == os.path.basename(p)]
    for ch in [c for c in chapters if c['vol'] == vol]:
        key = f"제{ch['chapter_no']}장 {ch['title']}"
        hit = [x['page'] for x in pgs if key in re.sub(r'\s+', ' ', x['text']) and x['page'] > 2]
        toc.append(dict(pdf=os.path.basename(p), vol=vol, chapter=ch['chapter_no'], title=ch['title'], page=hit[0] if hit else ''))
w_csv('toc.csv', toc, ['pdf','vol','chapter','title','page'])
# 조판 파라미터
css = open(os.path.join(ROOT, 'tools', 'buildpdf.py'), encoding='utf-8').read()
m = re.search(r'CSS\s*=\s*(?:r?[\'"]{3}|r?\')(.*?)(?:[\'"]{3}|\'\n)', css, re.S)
layout = dict(page='B5 176x250mm', margins='top 18, bottom 20, text left 35.2, right 14 (mm)', figure_table_width='176mm',
              font_body="Noto Serif CJK KR 10pt lh1.75", font_head="Noto Sans CJK KR h2 15pt h3 11.5pt h4 10.5pt", footer='page number 8pt center',
              toc='3-pass page numbers', engine='pandoc -> playwright chromium', buildpdf_lines=[l for l in css.split('\n') if l.startswith(('html{', 'h1', 'h2', 'h3', 'h4', 'p{', 'img{', 'table{', 'blockquote', '.refs', '.toc'))])
json.dump(layout, open(os.path.join(OUT, 'layout.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
tot = dict(chapters=len(chapters), figures=sum(len(c['figures']) for c in chapters), tables=sum(len(c['tables']) for c in chapters),
           refs=sum(len(c['references']) for c in chapters), pdfs={os.path.basename(p): hashlib.sha256(open(p, 'rb').read()).hexdigest() for p in pdfs})
json.dump(tot, open(os.path.join(OUT, 'summary.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in tot.items() if k != 'pdfs'}))
