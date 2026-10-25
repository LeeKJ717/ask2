# -*- coding: utf-8 -*-
"""db/obese2.db 에서 프로젝트 폴더 트리를 복원한다.  사용: python tools/dbexport.py 출력폴더"""
import os, sys, sqlite3
out = sys.argv[1] if len(sys.argv) > 1 else "obese2-restored"
con = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "db", "obese2.db"))
n = 0
for path, kind, text, blob in con.execute("SELECT path,kind,text,blob FROM files"):
    p = os.path.join(out, *path.split("/"))
    os.makedirs(os.path.dirname(p), exist_ok=True)
    if kind == "text":
        open(p, "w", encoding="utf-8", newline="").write(text)
    else:
        open(p, "wb").write(blob)
    n += 1
print(n, "개 파일 복원 →", out)
