#!/usr/bin/env python3
"""02pdf.py - OA PDF -> pdf_files table (LONGBLOB; >12MB goes to disk, path stored).
Sources in order: Europe PMC render (PMCID) -> Unpaywall (DOI) -> OA-location PDF links.
Only legal open-access copies are fetched.
Usage: python3 02pdf.py [--workers 4] [--limit 0]
"""
import argparse, hashlib, os
from concurrent.futures import ThreadPoolExecutor
from common import *

EPMC_PDF = "https://europepmc.org/backend/ptpmcrender.fcgi"
UNPAY = "https://api.unpaywall.org/v2/%s"


def fetch_pdf(url, params=None):
    try:
        r = get(url, params=params, timeout=120)
    except Exception:
        return None
    if r.status_code != 200:
        return None
    b = r.content
    if b[:5] != b"%PDF-" or len(b) < 5000:
        return None
    return b


def candidates(pmcid, doi):
    if pmcid:
        yield "europepmc", EPMC_PDF, {"accid": pmcid, "blobtype": "pdf"}
    if doi:
        try:
            r = get(UNPAY % doi, params={"email": MAIL}, timeout=40, tries=2)
            if r.status_code == 200:
                j = r.json()
                seen = set()
                locs = []
                if j.get("best_oa_location"):
                    locs.append(j["best_oa_location"])
                locs += j.get("oa_locations") or []
                for L in locs:
                    u = L.get("url_for_pdf")
                    if u and u not in seen:
                        seen.add(u)
                        yield "unpaywall", u, None
        except Exception:
            pass


def work(row):
    pmid, pmcid, doi = row
    db = conn()
    cur = db.cursor()
    try:
        if not pmcid and not doi:
            cur.execute("UPDATE papers SET pdf_status=2 WHERE pmid=%s", (pmid,))
            return "noid"
        for src, url, params in candidates(pmcid, doi):
            b = fetch_pdf(url, params)
            if b is None:
                continue
            sha = hashlib.sha256(b).hexdigest()
            if len(b) <= BLOB_LIMIT:
                cur.execute("REPLACE INTO pdf_files (pmid,source,size_bytes,sha256,pdf) VALUES (%s,%s,%s,%s,%s)",
                            (pmid, src, len(b), sha, b))
            else:
                os.makedirs(PDF_DIR, exist_ok=True)
                path = os.path.join(PDF_DIR, "%d.pdf" % pmid)
                with open(path, "wb") as f:
                    f.write(b)
                cur.execute("REPLACE INTO pdf_files (pmid,source,size_bytes,sha256,pdf_path) VALUES (%s,%s,%s,%s,%s)",
                            (pmid, src, len(b), sha, path))
            cur.execute("UPDATE papers SET pdf_status=1 WHERE pmid=%s", (pmid,))
            return "ok"
        cur.execute("UPDATE papers SET pdf_status=2 WHERE pmid=%s", (pmid,))
        return "none"
    except Exception as e:
        cur.execute("UPDATE papers SET pdf_status=3 WHERE pmid=%s", (pmid,))
        log("ERR", pmid, repr(e)[:200])
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
    cur.execute("SELECT pmid,pmcid,doi FROM papers WHERE pdf_status IN %s ORDER BY (pmcid IS NULL), pub_year DESC" % st)
    rows = cur.fetchall()
    if a.limit:
        rows = rows[:a.limit]
    log("pdf todo:", len(rows))
    stats = {}
    with ThreadPoolExecutor(a.workers) as ex:
        for i, res in enumerate(ex.map(work, rows), 1):
            stats[res] = stats.get(res, 0) + 1
            if i % 200 == 0:
                log("  %d/%d %s" % (i, len(rows), stats))
    log("pdf done", stats)


if __name__ == "__main__":
    main()
