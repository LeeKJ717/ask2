#!/bin/bash
# obesepharma_db setup (no interactive sudo). Creates DB, user, tables, folders.
cd "$(dirname "$0")"
BASE=/data/safe/dball2/obesepharma_db
echo "[1] folders"; mkdir -p "$BASE/logs" "$BASE/pdfs" && echo OK || echo FAIL
echo "[2] python modules"
python3 -c "import requests, pymysql" 2>/dev/null && echo OK || { pip3 install --user requests pymysql >/dev/null 2>&1 && echo INSTALLED || echo FAIL; }
echo "[3] database"
if mysql -u root < setup.sql 2>/dev/null; then echo "OK (root)";
elif sudo -n mysql < setup.sql 2>/dev/null; then echo "OK (sudo -n)";
elif mariadb -u root < setup.sql 2>/dev/null; then echo "OK (mariadb root)";
else echo "FAIL: DB root 권한 없음 — root 셸에서 'mysql < $(pwd)/setup.sql' 한 번 실행 필요"; fi
echo "[4] check"
mysql -h127.0.0.1 -uobesepharma -pobesepharma2026 obesepharma_db -e "SHOW TABLES;" 2>&1 | head -10
