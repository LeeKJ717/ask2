#!/usr/bin/env python3
"""reviewdbv1.py - obesepharma_db summary for table-of-contents tuning.
Run on z840 inside ~/obesepharmadb :  python3 reviewdbv1.py
Writes ~/obesepharmadb/review-v1.md (markdown report).
"""
import os, re, sys
from collections import Counter
import pymysql

DB = dict(host="127.0.0.1", user="obesepharma", password="obesepharma2026",
          database="obesepharma_db", charset="utf8mb4")
OUT = os.path.expanduser("~/obesepharmadb/review-v1.md")

TERMS = """semaglutide liraglutide tirzepatide exenatide dulaglutide lixisenatide orforglipron retatrutide survodutide
mazdutide cagrilintide cagrisema setmelanotide orlistat naltrexone phentermine glp1r glp-1 gipr gcgr mc4r gfral gdf15
leptin ghrelin pyy amylin oxyntomodulin camp pka epac beta-arrestin arrestin ampk mtor stat3 pi3k erk creb katp calcium
dpp-4 snac cryo-em molecular dynamics docking gwas polymorphism mendelian single-cell rna-seq proteom masld nafld kidney
cardiovascular sleep apnea bone muscle pancreatitis thyroid microbiota ginseng ketone fasting fiber hypothalam
vagal area postrema brown adipose ucp1 autophagy mitochondri endoplasmic reticulum biased agonism allosteric small molecule
machine learning deep learning alphafold""".split("\n")
TERMS = [t for line in TERMS for t in line.split()]
# multiword terms rejoined
MULTI = ["cryo-em", "molecular dynamics", "single-cell", "sleep apnea", "brown adipose", "area postrema",
         "endoplasmic reticulum", "biased agonism", "small molecule", "machine learning", "deep learning"]
SINGLE = [t for t in TERMS if t not in
          {"molecular", "dynamics", "sleep", "apnea", "brown", "adipose", "area", "postrema", "endoplasmic",
           "reticulum", "biased", "agonism", "small", "molecule", "machine", "learning", "deep", "cryo-em",
           "single-cell"}] + ["cryo-em", "single-cell"]
ALL_TERMS = sorted(set(SINGLE + MULTI))


def q(cur, sql, args=None):
    cur.execute(sql, args or ())
    return cur.fetchall()


def md_table(rows, head):
    out = ["| " + " | ".join(head) + " |", "|" + "|".join(["---"] * len(head)) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(x) for x in r) + " |")
    return "\n".join(out)


def main():
    db = pymysql.connect(**DB)
    cur = db.cursor()
    L = []
    L.append("# obesepharma_db 현황 보고 v1\n")

    tot = q(cur, "SELECT COUNT(*), SUM(abstract<>''), SUM(doi IS NOT NULL), SUM(pmcid IS NOT NULL), "
                 "SUM(ft_status=1), SUM(ft_status=2), SUM(ft_status=0), SUM(ft_status=3), "
                 "SUM(pdf_status=1), SUM(pdf_status=2), SUM(pdf_status=0), SUM(pdf_status=3) FROM papers")[0]
    L.append("## 1. 전체\n")
    L.append(md_table([tot], ["논문", "초록有", "DOI有", "PMCID有", "전문ok", "전문없음", "전문대기", "전문오류",
                              "PDFok", "PDF없음", "PDF대기", "PDF오류"]))
    ftn = q(cur, "SELECT COUNT(*), ROUND(AVG(CHAR_LENGTH(body))), MAX(CHAR_LENGTH(body)) FROM fulltexts")[0]
    L.append("\n전문 저장 %s건, 평균 %s자, 최대 %s자\n" % ftn)

    axes = [r[0] for r in q(cur, "SELECT DISTINCT axis FROM search_log ORDER BY id")]
    rows = []
    for ax in axes:
        r = q(cur, "SELECT COUNT(*), SUM(ft_status=1), SUM(pdf_status=1), MIN(pub_year), MAX(pub_year) "
                   "FROM papers WHERE FIND_IN_SET(%s,axes)", (ax,))[0]
        rows.append((ax,) + tuple(r))
    L.append("## 2. 검색 축별\n")
    L.append(md_table(rows, ["축", "논문", "전문ok", "PDFok", "최소연도", "최대연도"]))

    multi = q(cur, "SELECT (LENGTH(axes)-LENGTH(REPLACE(axes,',',''))+1) n, COUNT(*) FROM papers GROUP BY n ORDER BY n")
    L.append("\n\n## 3. 겹치는 축 수 분포\n")
    L.append(md_table(multi, ["속한 축 수", "논문"]))

    yrs = q(cur, "SELECT FLOOR(pub_year/5)*5 y, COUNT(*) FROM papers WHERE pub_year IS NOT NULL GROUP BY y ORDER BY y")
    L.append("\n\n## 4. 5년 단위 연도 분포\n")
    L.append(md_table([(f"{int(a)}~{int(a)+4}", b) for a, b in yrs], ["연도", "논문"]))

    jr = q(cur, "SELECT journal, COUNT(*) c FROM papers WHERE journal<>'' GROUP BY journal ORDER BY c DESC LIMIT 30")
    L.append("\n\n## 5. 상위 저널 30\n")
    L.append(md_table(jr, ["저널", "논문"]))

    ptypes = Counter()
    mesh = Counter()
    termc = Counter()
    cur2 = db.cursor(pymysql.cursors.SSCursor)
    cur2.execute("SELECT pub_types, mesh, CONCAT_WS(' ', title, abstract) FROM papers")
    n = 0
    for pt, ms, text in cur2:
        n += 1
        for t in (pt or "").split("; "):
            if t:
                ptypes[t] += 1
        for m in (ms or "").split("; "):
            if m:
                mesh[m] += 1
        low = (text or "").lower()
        for t in ALL_TERMS:
            if t in low:
                termc[t] += 1
    cur2.close()

    L.append("\n\n## 6. 출판 유형 상위 15\n")
    L.append(md_table(ptypes.most_common(15), ["유형", "논문"]))
    L.append("\n\n## 7. MeSH 상위 80\n")
    L.append(md_table(mesh.most_common(80), ["MeSH", "논문"]))
    L.append("\n\n## 8. 제목·초록 용어 출현 건수 (총 %d편 중)\n" % n)
    L.append(md_table(sorted(termc.items(), key=lambda x: -x[1]), ["용어", "논문"]))

    L.append("\n\n## 9. 축별 최근 종설(Review) 제목 12편\n")
    for ax in axes:
        rows = q(cur, "SELECT pmid, pub_year, LEFT(title,140) FROM papers "
                      "WHERE FIND_IN_SET(%s,axes) AND pub_types LIKE '%%Review%%' "
                      "ORDER BY pub_year DESC, pmid DESC LIMIT 12", (ax,))
        L.append("\n### %s\n" % ax)
        for pmid, y, t in rows:
            L.append("- %s (%s) %s" % (pmid, y, t))

    L.append("\n\n## 10. 임상시험·메타분석 건수 (축별)\n")
    rows = []
    for ax in axes:
        r = q(cur, "SELECT SUM(pub_types LIKE '%%Randomized Controlled Trial%%'), "
                   "SUM(pub_types LIKE '%%Meta-Analysis%%'), SUM(pub_types LIKE '%%Systematic Review%%') "
                   "FROM papers WHERE FIND_IN_SET(%s,axes)", (ax,))[0]
        rows.append((ax,) + tuple(r))
    L.append(md_table(rows, ["축", "RCT", "메타분석", "체계적 문헌고찰"]))

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print("wrote", OUT, "papers", tot[0])


if __name__ == "__main__":
    main()
