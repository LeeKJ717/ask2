# -*- coding: utf-8 -*-
"""원고 마크다운 → 조판 시험본 PDF (B5, 왼쪽 여백 20%, 그림·표 전폭, 쪽번호, 목차 쪽번호, 컬러·흑백).
사용(프로젝트 루트에서):  python tools/buildpdf.py draft   → build/obese2-draft-v1-color.pdf, -bw.pdf
                          python tools/buildpdf.py handoff → build/handoff-v1.pdf
필요: pandoc, playwright(chromium), poppler(pdftotext)"""
import os, re, sys, glob, subprocess, html
from playwright.sync_api import sync_playwright

ROOT = os.getcwd(); BUILD = os.path.join(ROOT, "build"); os.makedirs(BUILD, exist_ok=True)
VERSION = "v1"
CSS_COMMON = """
html{font-family:'Noto Serif CJK KR','Malgun Gothic',serif;font-size:10pt;line-height:1.75;color:#111}
body{margin:0;padding:0}
/* 쪽 좌우 여백은 0으로 두고, 글 요소에만 왼쪽 20%(35.2mm)·오른쪽 14mm를 준다. 그림·표는 여백 없이 쪽 전체 폭(176mm)을 쓴다 */
h1,h2,h3,h4,p,blockquote,ul,ol,.toc,.refs,.cover{margin-left:35.2mm;margin-right:14mm}
h1{font-family:'Noto Sans CJK KR',sans-serif;font-size:17pt;margin-top:0;margin-bottom:4mm}
h2{font-family:'Noto Sans CJK KR',sans-serif;font-size:15pt;margin-top:0;margin-bottom:5mm;page-break-before:always;border-bottom:1.5px solid ACCENT;padding-bottom:2mm}
h1.part{page-break-before:always;font-size:19pt;margin-top:70mm;text-align:left;color:ACCENT}
h1.part + h2{page-break-before:avoid;margin-top:12mm}
h3{font-family:'Noto Sans CJK KR',sans-serif;font-size:11.5pt;margin-top:6mm;margin-bottom:2mm;color:ACCENT}
h4{font-family:'Noto Sans CJK KR',sans-serif;font-size:10.5pt;margin-top:8mm;margin-bottom:2mm}
p{margin-top:0;margin-bottom:2.4mm;text-align:justify;word-break:keep-all}
blockquote{margin-top:3mm;margin-bottom:3mm;padding:2mm 3mm;border-left:3px solid ACCENT;background:BG;font-size:9.5pt}
img{display:block;margin:4mm 0 2mm 0;width:176mm;max-width:none;page-break-inside:avoid}
table{border-collapse:collapse;margin:3mm 0;width:176mm;font-size:9pt;line-height:1.45;page-break-inside:avoid}
th,td{border:1px solid #888;padding:1.6mm 2mm;vertical-align:top}th{background:BG}
.refs{font-size:9pt;line-height:1.5}.refs p{text-align:left;margin-left:0;margin-right:0;margin-bottom:1.6mm;padding-left:6mm;text-indent:-6mm}
.refs h4{margin-left:0;margin-right:0}
.toc{font-family:'Noto Sans CJK KR',sans-serif;font-size:10pt}.toc div{display:flex;margin:1mm 0}.toc span.t{flex:1;border-bottom:1px dotted #888;margin-right:2mm}
.cover{height:200mm;display:flex;flex-direction:column;justify-content:center}
em{font-style:italic}
"""
def prep(md_path, bw):
    s = open(md_path, encoding="utf-8").read()
    s = re.sub(r"^# (제\d+부.*)$", r'# \1 {.part}', s, flags=re.M)
    s = re.sub(r"(#### 참고문헌.*)$", lambda m: "::: refs\n" + m.group(1) + "\n:::", s, flags=re.S)
    if bw:
        s = re.sub(r"(그림\d+-\d+)\.png", r"\1-흑백.png", s)
    return s

def render(htmlfile, pdffile, footer=True):
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        pg.goto("file://" + htmlfile)
        pg.wait_for_load_state("networkidle")
        tmpl = '<div style="font-size:8pt;width:100%;text-align:center;font-family:sans-serif"><span class="pageNumber"></span></div>'
        pg.pdf(path=pdffile, width="176mm", height="250mm", print_background=True, display_header_footer=footer,
               header_template="<div></div>", footer_template=tmpl,
               margin=dict(top="18mm", bottom="20mm", left="0mm", right="0mm"))
        b.close()

def pages_of(pdf):
    n = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout).group(1))
    return [subprocess.run(["pdftotext", "-f", str(i), "-l", str(i), "-layout", pdf, "-"], capture_output=True, text=True).stdout for i in range(1, n + 1)]

def build_draft(bw):
    accent, bg = ("#555555", "#eeeeee") if bw else ("#2f5f7a", "#e8eef2")
    css = CSS_COMMON.replace("ACCENT", accent).replace("BG", bg)
    chapters = sorted(glob.glob(os.path.join(ROOT, "manuscript", "*장-v*.md")))
    heads = []  # (level, text)
    parts = []
    lastpart = None
    for c in chapters:
        s = prep(c, bw)
        pm = re.search(r'^# (제\d+부.*?) \{\.part\}$', s, re.M)
        if pm:
            if pm.group(1) == lastpart: s = s.replace(pm.group(0), '')
            lastpart = pm.group(1)
        for m in re.finditer(r"^(#{1,2}) (.+?)(?: \{\.part\})?$", s, re.M):
            heads.append((len(m.group(1)), m.group(2).strip()))
        out = subprocess.run(["pandoc", "-f", "markdown+fenced_divs", "-t", "html", "--wrap=none"], input=s, capture_output=True, text=True).stdout
        parts.append(out)
    body = "\n".join(parts)
    # 이미지 경로는 manuscript 기준(../figures) → build 기준도 동일
    title = f'<div class="cover"><h1 style="font-size:24pt">비만치료약물의 신호전달과 신약 설계</h1><p style="font-size:13pt">1권 원리편 · 조판 시험본 {VERSION} ({"흑백" if bw else "컬러"})</p><p>이광조 · 과학과영성출판사</p></div>'
    def toc_html(pn):
        rows = "".join(f'<div style="{"margin-left:6mm" if lv==2 else "font-weight:700;margin-top:3mm"}"><span class="t">{html.escape(t)}</span><span>{pn.get(t, "")}</span></div>' for lv, t in heads)
        return '<h2 style="page-break-before:always;border:none">차례</h2><div class="toc">' + rows + '</div>'
    def doc(pn):
        return f"<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body>{title}{toc_html(pn)}{body}</body></html>"
    tag = "bw" if bw else "color"
    hf = os.path.join(BUILD, f"draft-{tag}.html"); pf = os.path.join(BUILD, f"obese2-draft-{VERSION}-{tag}.pdf")
    open(hf, "w", encoding="utf-8").write(doc({})); render(hf, pf)
    pn = {}
    pgs = pages_of(pf)
    for lv, t in heads:
        key = re.sub(r"\s+", "", t)[:14]
        for i, txt in enumerate(pgs):
            if i < 2: continue
            if key in re.sub(r"\s+", "", txt):
                pn[t] = i + 1; break
    open(hf, "w", encoding="utf-8").write(doc(pn)); render(hf, pf)
    print(pf, len(pages_of(pf)), "쪽")

def build_handoff():
    css = "html{font-family:'Noto Sans CJK KR',sans-serif;font-size:10pt;line-height:1.6}h1{font-size:19pt;border-bottom:2px solid #2f5f7a}h2{font-size:13.5pt;color:#2f5f7a;margin-top:6mm}table{border-collapse:collapse;width:100%;margin:2mm 0;page-break-inside:avoid}th,td{border:1px solid #999;padding:1.5mm 2mm;font-size:9pt;vertical-align:top}th{background:#e8eef2}code{font-family:'Noto Sans Mono CJK KR',monospace;font-size:8.5pt;background:#f2f4f5}pre{background:#f2f4f5;padding:2mm;font-size:8.5pt;white-space:pre-wrap;page-break-inside:avoid}blockquote{border-left:3px solid #2f5f7a;margin-left:0;padding-left:3mm}"
    md = open(os.path.join(ROOT, "docs", "handoff-v1.md"), encoding="utf-8").read()
    h = subprocess.run(["pandoc", "-f", "markdown", "-t", "html", "--wrap=none"], input=md, capture_output=True, text=True).stdout
    hf = os.path.join(BUILD, "handoff-v1.html"); pf = os.path.join(BUILD, "handoff-v1.pdf")
    open(hf, "w", encoding="utf-8").write(f"<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body>{h}</body></html>")
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(); pg.goto("file://" + hf)
        pg.pdf(path=pf, format="A4", print_background=True, display_header_footer=True, header_template="<div></div>",
               footer_template='<div style="font-size:8pt;width:100%;text-align:center"><span class="pageNumber"></span> / <span class="totalPages"></span></div>',
               margin=dict(top="16mm", bottom="18mm", left="16mm", right="16mm"))
        b.close()
    print(pf)

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "draft"
    if mode == "handoff": build_handoff()
    else:
        build_draft(False); build_draft(True)
