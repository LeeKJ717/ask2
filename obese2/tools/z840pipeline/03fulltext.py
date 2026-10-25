#!/usr/bin/env python3
"""03fulltext.py - Europe PMC OA JATS full text (by PMCID) -> fulltexts table.
Papers without a PMCID get ft_status=2 (no OA full text in PMC).
Usage: python3 03fulltext.py [--workers 4] [--limit 0]
"""
import argparse
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from common import *

EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest/%s/fullTextXML"


def jats_to_text(xml_bytes):
    root = ET.fromstring(xml_bytes)
    out = []
    t = root.find(".//front//article-title")
    if t is not None:
        out.append("".join(t.itertext()).strip())
    ab = root.find(".//front//abstract")
    if ab is not None:
        out.append("ABSTRACT")
        out.append(" ".join("".join(ab.itertext()).split()))
    body = root.find(".//body")
    if body is not None:
        for el in body.iter():
            if el.tag in ("title", "p", "label") :
                s = " ".join("".join(el.itertext()).split())
                if s:
                    out.append(s)
    return "\n".join(out)


def work(row):
    pmid, pmcid = row
    db = conn()
    cur = db.cursor()
    try:
        if not pmcid:
            cur.execute("UPDATE papers SET ft_status=2 WHERE pmid=%s", (pmid,))
            return "nopmc"
        r = get(EPMC % pmcid, timeout=90)
        if r.status_code in (404, 403):
            cur.execute("UPDATE papers SET ft_status=2 WHERE pmid=%s", (pmid,))
            return "none"
        r.raise_for_status()
        body = jats_to_text(r.content)
        if len(body) < 500:
            cur.execute("UPDATE papers SET ft_status=2 WHERE pmid=%s", (pmid,))
            return "short"
        cur.execute("REPLACE INTO fulltexts (pmid,source,body,xml) VALUES (%s,%s,%s,%s)",
                    (pmid, "europepmc", body, r.content.decode("utf-8", "replace")))
        cur.execute("UPDATE papers SET ft_status=1 WHERE pmid=%s", (pmid,))
        return "ok"
    except Exception as e:
        cur.execute("UPDATE papers SET ft_status=3 WHERE pmid=%s", (pmid,))
        log("ERR", pmid, pmcid, repr(e)[:200])
        return "err"
    finally:
        db.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--retry-errors", action="store_true")
    a = ap.parse_args()
    db = conn()
    cur = db.cursor()
    st = "(0,3)" if a.retry_errors else "(0)"
    cur.execute("SELECT pmid,pmcid FROM papers WHERE ft_status IN %s ORDER BY pub_year DESC" % st)
    rows = cur.fetchall()
    if a.limit:
        rows = rows[:a.limit]
    log("fulltext todo:", len(rows))
    stats = {}
    with ThreadPoolExecutor(a.workers) as ex:
        for i, res in enumerate(ex.map(work, rows), 1):
            stats[res] = stats.get(res, 0) + 1
            if i % 200 == 0:
                log("  %d/%d %s" % (i, len(rows), stats))
    log("fulltext done", stats)


if __name__ == "__main__":
    main()
