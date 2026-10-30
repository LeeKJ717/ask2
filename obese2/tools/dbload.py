# -*- coding: utf-8 -*-
"""obese2 조판 관련 데이터를 db/obese2.db(SQLite)에 적재·갱신한다.
사용: 프로젝트 루트(obese2)에서  python tools/dbload.py
파일을 읽어 변경분을 반영한다(해시 비교). DB와 파일은 서로 복제본이며 변경 이력은 git으로 남긴다."""
import os, re, sys, sqlite3, hashlib, time, glob

ROOT = os.getcwd()
if not os.path.isdir(os.path.join(ROOT, "manuscript")):
    sys.exit("obese2 루트에서 실행하세요")
DB = os.path.join(ROOT, "db", "obese2.db")
os.makedirs(os.path.dirname(DB), exist_ok=True)
con = sqlite3.connect(DB)
cur = con.cursor()
SCHEMA = """
CREATE TABLE IF NOT EXISTS meta(k TEXT PRIMARY KEY, v TEXT);
CREATE TABLE IF NOT EXISTS files(path TEXT PRIMARY KEY, kind TEXT, size INTEGER, sha256 TEXT, mtime REAL, text TEXT, blob BLOB, loaded TEXT);
CREATE TABLE IF NOT EXISTS chapters(vol INTEGER, ch INTEGER, part TEXT, title TEXT, version TEXT, path TEXT, md TEXT, chars INTEGER, sha256 TEXT, loaded TEXT, PRIMARY KEY(vol,ch));
CREATE TABLE IF NOT EXISTS figures(vol INTEGER, num TEXT, title TEXT, caption TEXT, kind TEXT, color_png TEXT, bw_png TEXT, data_path TEXT, script_path TEXT, svg_path TEXT, PRIMARY KEY(vol,num));
CREATE TABLE IF NOT EXISTS tables_(vol INTEGER, num TEXT, title TEXT, md TEXT, PRIMARY KEY(vol,num));
CREATE TABLE IF NOT EXISTS refs(id INTEGER PRIMARY KEY AUTOINCREMENT, vol INTEGER, ch INTEGER, apa TEXT, doi TEXT, verified INTEGER DEFAULT 0);
CREATE TABLE IF NOT EXISTS tocheck(id INTEGER PRIMARY KEY AUTOINCREMENT, section TEXT, subsection TEXT, item TEXT, status TEXT DEFAULT 'open');
CREATE TABLE IF NOT EXISTS toc(name TEXT PRIMARY KEY, md TEXT, sha256 TEXT);
CREATE TABLE IF NOT EXISTS rules(name TEXT PRIMARY KEY, md TEXT, sha256 TEXT);
CREATE TABLE IF NOT EXISTS skills(name TEXT PRIMARY KEY, md TEXT, sha256 TEXT);
CREATE TABLE IF NOT EXISTS decisions(id INTEGER PRIMARY KEY AUTOINCREMENT, item TEXT);
CREATE TABLE IF NOT EXISTS typeset(k TEXT PRIMARY KEY, v TEXT, note TEXT);
CREATE TABLE IF NOT EXISTS builds(path TEXT PRIMARY KEY, kind TEXT, size INTEGER, sha256 TEXT, loaded TEXT, blob BLOB);
CREATE TABLE IF NOT EXISTS status(item TEXT PRIMARY KEY, state TEXT, note TEXT);
"""
cur.executescript(SCHEMA)
now = time.strftime("%Y-%m-%d %H:%M:%S")
TEXT_EXT = {".md", ".py", ".sh", ".csv", ".svg", ".txt", ".json", ".sql"}

def sha(b): return hashlib.sha256(b).hexdigest()

# 1. files
cur.execute("DELETE FROM files")
n = 0
for dp, dn, fn in os.walk(ROOT):
    if os.path.relpath(dp, ROOT).split(os.sep)[0] in ("db", ".git", "__pycache__", "build"):
        dn[:] = []
        continue
    dn[:] = [d for d in dn if d not in ("__pycache__", ".git")]
    for f in fn:
        p = os.path.join(dp, f)
        rel = os.path.relpath(p, ROOT).replace(os.sep, "/")
        b = open(p, "rb").read()
        ext = os.path.splitext(f)[1].lower()
        if ext in TEXT_EXT:
            cur.execute("INSERT INTO files VALUES(?,?,?,?,?,?,?,?)", (rel, "text", len(b), sha(b), os.path.getmtime(p), b.decode("utf-8", "replace"), None, now))
        else:
            cur.execute("INSERT INTO files VALUES(?,?,?,?,?,?,?,?)", (rel, "bin", len(b), sha(b), os.path.getmtime(p), None, b, now))
        n += 1

# 2. chapters / figures / tables / refs
for t in ("chapters", "figures", "tables_", "refs"):
    cur.execute(f"DELETE FROM {t}")
for vol, MS, FG in ((1,"manuscript","figures"),(2,"manuscript2","figures2")):
  for p in sorted(glob.glob(os.path.join(ROOT, MS, "*.md"))):
      name = os.path.basename(p)
      m = re.match(r"(\d+)장-v(\d+)", name)
      if not m: continue
      ch, ver = int(m.group(1)), "v" + m.group(2)
      md = open(p, encoding="utf-8").read()
      part = (re.search(r"^# (.+)$", md, re.M) or [None, ""])[1]
      title = (re.search(r"^## (.+)$", md, re.M) or [None, ""])[1]
      cur.execute("INSERT INTO chapters VALUES(?,?,?,?,?,?,?,?,?,?)", (vol, ch, part, title, ver, MS + "/" + name, md, len(md), sha(md.encode()), now))
      for fm in re.finditer(r"\*\*그림 (\d+-\d+)\. (.+?)\.\*\*\s*(.*?)\n\s*\n!\[[^\]]*\]\(([^)]+)\)", md, re.S):
          num, ttl, cap, img = fm.group(1), fm.group(2), fm.group(3).strip(), fm.group(4)
          base = os.path.basename(img)
          stem = os.path.splitext(base)[0]
          bw = FG + "/out/" + stem + "-흑백.png"
          kind = "개념도" if "개념도" in cap else "데이터"
          def ex(rel): return rel if os.path.exists(os.path.join(ROOT, rel)) else None
          cur.execute("INSERT OR REPLACE INTO figures VALUES(?,?,?,?,?,?,?,?,?,?)", (vol, num, ttl, cap, kind,
              ex(FG + "/out/" + base), ex(bw), ex(f"{FG}/data/fig{num}-" + "") ,
              ex(f"{FG}/scripts/fig{num}.py"), ex(f"{FG}/svg/fig{num}.svg")))
      for tm in re.finditer(r"\*\*표 (\d+-\d+)\. (.+?)\.\*\*\s*\n\s*\n((?:\|.*\n?)+)", md):
          cur.execute("INSERT OR REPLACE INTO tables_ VALUES(?,?,?,?)", (vol, tm.group(1), tm.group(2), tm.group(3).strip()))
      rm = re.search(r"#### 참고문헌\s*\n(.*)$", md, re.S)
      if rm:
          for para in [x.strip() for x in rm.group(1).split("\n\n") if x.strip()]:
              d = re.search(r"https://doi\.org/(\S+)", para)
              cur.execute("INSERT INTO refs(vol,ch,apa,doi) VALUES(?,?,?,?)", (vol, ch, para, d.group(1) if d else None))
# 그림 데이터 경로 보정(CSV는 fig{번호}-*.csv)
for vv, num in cur.execute("SELECT vol,num FROM figures").fetchall():
    g = glob.glob(os.path.join(ROOT, "figures" if vv == 1 else "figures2", "data", f"fig{num}-*.csv"))
    cur.execute("UPDATE figures SET data_path=? WHERE num=? AND vol=?", (os.path.relpath(g[0], ROOT).replace(os.sep, "/") if g else None, num, vv))

# 3. tocheck
cur.execute("DELETE FROM tocheck")
tp = os.path.join(ROOT, "refs", "tocheck.md")
if os.path.exists(tp):
    sec = sub = ""
    for ln in open(tp, encoding="utf-8").read().splitlines():
        if ln.startswith("# "): sec = ln[2:].strip(); sub = ""
        elif ln.startswith("## "): sub = ln[3:].strip()
        elif ln.startswith("- "): cur.execute("INSERT INTO tocheck(section,subsection,item) VALUES(?,?,?)", (sec, sub, ln[2:].strip()))

# 4. toc, rules
for t, folder in (("toc", "toc"), ("rules", "docs/rules"), ("skills", "docs/skills")):
    cur.execute(f"DELETE FROM {t}")
    for p in sorted(glob.glob(os.path.join(ROOT, folder, "*.md"))):
        s = open(p, encoding="utf-8").read()
        cur.execute(f"INSERT INTO {t} VALUES(?,?,?)", (os.path.basename(p), s, sha(s.encode())))

# 5. decisions, status (인계서에서 추출)
cur.execute("DELETE FROM decisions"); cur.execute("DELETE FROM status")
hp = os.path.join(ROOT, "docs", "handoff-v1.md")
if os.path.exists(hp):
    h = open(hp, encoding="utf-8").read()
    dm = re.search(r"## 2\. 확정된 결정\n(.*?)\n## ", h, re.S)
    if dm:
        for ln in dm.group(1).splitlines():
            m = re.match(r"\d+\. (.+)", ln)
            if m: cur.execute("INSERT INTO decisions(item) VALUES(?)", (m.group(1),))
    sm = re.search(r"## 3\. 진행 상태\n(.*?)\n## ", h, re.S)
    if sm:
        for ln in sm.group(1).splitlines():
            c = [x.strip() for x in ln.strip("|").split("|")]
            if len(c) == 3 and c[0] not in ("단계", "---"):
                cur.execute("INSERT OR REPLACE INTO status VALUES(?,?,?)", tuple(c))

# 6. 조판 파라미터와 빌드 산출물(PDF) — 향후 같은 판면으로 재조판하기 위한 기록
cur.execute("DELETE FROM typeset"); cur.execute("DELETE FROM builds")
TS = [("판형","B5(176 x 250 mm)","1권 기준"),("본문 폭","176 mm(그림·표 전폭)","buildpdf.py CSS img/table width"),
 ("왼쪽 여백","35.2 mm(본문 폭의 20%)","텍스트만 적용, 그림·표는 전폭"),("오른쪽 여백","14 mm","텍스트"),
 ("PDF 상하 여백","위 18 mm, 아래 20 mm","playwright page.pdf margin"),("쪽번호","모든 쪽 하단 중앙 8 pt","footer_template"),
 ("본문 글꼴","Noto Serif CJK KR 10 pt, 행간 1.75","buildpdf.py"),("제목 글꼴","Noto Sans CJK KR(장 15 pt, 절 11.5 pt)","buildpdf.py"),
 ("변환 도구","pandoc 3.1.3 + playwright Chromium PDF","markdown+fenced_divs -> html -> pdf"),
 ("그림 도구","figlib.py(SVG, viewBox 800) -> cairosvg PNG 2079 px -> PIL 흑백","figures/scripts/figlib.py"),
 ("그림 규칙","컬러/흑백 쌍(-흑백.png), 글자 최소 22 단위, F.report() 겹침 검사","figures/scripts"),
 ("표 규칙","한 쪽에 들어가게(page-break-inside:avoid), 번호+제목","buildpdf.py"),
 ("참고문헌","APA 7th, 장 끝","#### 참고문헌"),("목차","쪽번호 포함, 3회 패스로 번호 확정","buildpdf.py"),
 ("장 템플릿","부 제목(첫 장만) / 장 / 출발점 인용 / N.M 절 / 그림·표 + 해석 / 요점 / 참고문헌","manuscript/*.md")]
cur.executemany("INSERT INTO typeset VALUES(?,?,?)", TS)
for p in sorted(glob.glob(os.path.join(ROOT, "build", "*.pdf"))):
    b = open(p, "rb").read()
    cur.execute("INSERT INTO builds VALUES(?,?,?,?,?,?)", ("build/" + os.path.basename(p), "pdf", len(b), sha(b), now, b))
cur.execute("INSERT OR REPLACE INTO meta VALUES('loaded',?)", (now,))
cur.execute("INSERT OR REPLACE INTO meta VALUES('project','비만치료약물 책 시리즈 (obese2)')")
con.commit()
for t in ("files", "chapters", "figures", "tables_", "refs", "tocheck", "toc", "rules", "skills", "decisions", "status", "typeset", "builds"):
    print(t, cur.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0])
con.close()
