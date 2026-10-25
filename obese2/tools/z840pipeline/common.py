"""obesepharma_db v1 shared helpers."""
import os, sys, time, threading
import requests, pymysql

BASE = os.environ.get("OBESE_BASE", "/data/safe/dball2/obesepharma_db")
PDF_DIR = os.path.join(BASE, "pdfs")
DB = dict(host="127.0.0.1", user="obesepharma", password="obesepharma2026",
          database="obesepharma_db", charset="utf8mb4", autocommit=True,
          max_allowed_packet=256 * 1024 * 1024)
NCBI_KEY = os.environ.get("NCBI_API_KEY", "")
MAIL = os.environ.get("UNPAYWALL_EMAIL", "contact@solmindit.com")
UA = {"User-Agent": "obesepharma-db/1.0 (mailto:%s)" % MAIL}
BLOB_LIMIT = 12 * 1024 * 1024   # larger PDFs go to disk, path recorded in DB


def conn():
    return pymysql.connect(**DB)


_sess = threading.local()


def http():
    s = getattr(_sess, "s", None)
    if s is None:
        s = requests.Session()
        s.headers.update(UA)
        _sess.s = s
    return s


_lock = threading.Lock()
_last = [0.0]


def throttle(interval):
    """global minimum spacing between calls to one host family."""
    with _lock:
        now = time.time()
        wait = _last[0] + interval - now
        if wait > 0:
            time.sleep(wait)
        _last[0] = time.time()


def get(url, params=None, timeout=60, tries=4, stream=False):
    last = None
    for i in range(tries):
        try:
            r = http().get(url, params=params, timeout=timeout, stream=stream)
            if r.status_code in (429, 500, 502, 503, 504):
                time.sleep(2 * (i + 1))
                last = r
                continue
            return r
        except requests.RequestException as e:
            last = e
            time.sleep(2 * (i + 1))
    if isinstance(last, requests.Response):
        return last
    raise RuntimeError("GET failed: %s %s" % (url, last))


def post(url, data, timeout=120, tries=4):
    last = None
    for i in range(tries):
        try:
            r = http().post(url, data=data, timeout=timeout)
            if r.status_code in (429, 500, 502, 503, 504):
                time.sleep(2 * (i + 1))
                last = r
                continue
            return r
        except requests.RequestException as e:
            last = e
            time.sleep(2 * (i + 1))
    if isinstance(last, requests.Response):
        return last
    raise RuntimeError("POST failed: %s %s" % (url, last))


def log(*a):
    print(time.strftime("%F %T"), *a, flush=True)
