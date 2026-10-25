#!/bin/bash
# obesepharma_db pipeline: search -> fulltext -> pdf, incremental (safe to re-run).
# Optional env: NCBI_API_KEY (10 req/s instead of 3), UNPAYWALL_EMAIL
cd "$(dirname "$0")"
BASE=/data/safe/dball2/obesepharma_db
mkdir -p "$BASE/logs"
L="$BASE/logs/run-$(date +%Y%m%d-%H%M%S).log"
echo "log: $L"
{
  echo "=== 01search ==="; python3 01search.py "$@" && echo "01 OK" || echo "01 FAIL"
  echo "=== 03fulltext ==="; python3 03fulltext.py && echo "03 OK" || echo "03 FAIL"
  echo "=== 02pdf ===";      python3 02pdf.py && echo "02 OK" || echo "02 FAIL"
  echo "=== counts ==="
  mysql -h127.0.0.1 -uobesepharma -pobesepharma2026 obesepharma_db -e "
    SELECT COUNT(*) papers, SUM(ft_status=1) fulltext_ok, SUM(pdf_status=1) pdf_ok FROM papers;
    SELECT axis, MAX(hits) hits FROM search_log GROUP BY axis;"
} 2>&1 | tee "$L"
