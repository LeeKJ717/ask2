import csv, sys, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
here = os.path.dirname(os.path.abspath(__file__))
data = os.path.join(here, "..", "data", "fig1-1-timeline.csv")
out = os.path.join(here, "..", "out")
for f in fm.findSystemFonts():
    if "NotoSansCJK" in f or "Malgun" in f or "malgun" in f:
        fm.fontManager.addfont(f)
cands = [n for n in ("Malgun Gothic", "Noto Sans CJK KR", "Noto Sans CJK JP") if n in {x.name for x in fm.fontManager.ttflist}]
plt.rcParams["font.family"] = cands[0]
plt.rcParams["axes.unicode_minus"] = False
rows = list(csv.DictReader(open(data, encoding="utf-8")))
def draw(bw, path):
    fig, ax = plt.subplots(figsize=(6.93, 4.2), dpi=300)
    hatches = ["", "//", "\\\\", "xx", "..", "++", "oo"]
    colors = ["#4C78A8", "#F58518", "#54A24B", "#E45756", "#B279A2", "#72B7B2", "#9D755D"]
    greys = ["#222222", "#555555", "#888888", "#aaaaaa", "#333333", "#777777", "#bbbbbb"]
    n = len(rows)
    for i, r in enumerate(rows):
        y = n - 1 - i
        s, e = int(r["start_year"]), int(r["end_year"])
        ax.barh(y, e - s, left=s, height=0.55,
                color=(greys[i] if bw else colors[i]), edgecolor="black",
                hatch=(hatches[i] if bw else ""), linewidth=0.8)
        ax.text(s - 1, y, r["drug"], ha="right", va="center", fontsize=9, bbox=dict(fc="white", ec="none", pad=1.5), zorder=5)
        ax.text(e + 1, y, f"{s}–{e}", ha="left", va="center", fontsize=8)
    ax.set_xlim(1900, 2045)
    ax.set_xticks([1930, 1950, 1970, 1990, 2010, 2030]); ax.set_xticklabels(["1930","1950","1970","1990","2010","2030"])
    ax.set_yticks([])
    ax.axvline(1994, color="black", ls="--", lw=0.8, zorder=0)
    ax.text(1994.5, n - 0.35, "1994 렙틴 클로닝", fontsize=8, va="bottom")
    ax.set_xlabel("연도")
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    fig.subplots_adjust(left=0.02, right=0.98, bottom=0.14, top=0.92)
    fig.savefig(path); plt.close(fig)
draw(False, os.path.join(out, "그림1-1.png"))
draw(True, os.path.join(out, "그림1-1-흑백.png"))
