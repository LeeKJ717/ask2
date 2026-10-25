import csv, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
here = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(here, "..", "data", "fig2-1-trials.csv"), encoding="utf-8")))
out = os.path.join(here, "..", "out")
for f in fm.findSystemFonts():
    if "NotoSansCJK" in f: fm.fontManager.addfont(f)
names = {x.name for x in fm.fontManager.ttflist}
plt.rcParams["font.family"] = "Malgun Gothic" if "Malgun Gothic" in names else "Noto Sans CJK KR"
plt.rcParams["axes.unicode_minus"] = False
def draw(bw, path):
    fig, ax = plt.subplots(figsize=(6.93, 4.2), dpi=300)
    col = ["#4C78A8", "#9a9a9a", "#F58518", "#E45756", "#B22222", "#9a9a9a"]
    grey = ["#444444", "#dddddd", "#777777", "#555555", "#222222", "#dddddd"]
    hat = ["//", "", "..", "xx", "++", ""]
    pos = [0, 1, 2.6, 3.6, 4.6, 5.6]
    for i, r in enumerate(rows):
        v = float(r["mean_weight_change_pct"])
        ax.bar(pos[i], v, width=0.8, color=(grey[i] if bw else col[i]), edgecolor="black", hatch=(hat[i] if bw else ""), lw=0.8)
        ax.text(pos[i], v - 0.8, f"{v:.1f}%", ha="center", va="top", fontsize=9)
    ax.set_xticks(pos)
    ax.set_xticklabels(["세마글루\n타이드\n2.4 mg", "위약", "티르제파\n타이드\n5 mg", "10 mg", "15 mg", "위약"], fontsize=8.5)
    ax.axhline(0, color="black", lw=0.8)
    ax.set_ylim(-25, 2)
    ax.set_ylabel("체중 변화율 (%)")
    ax.text(0.5, 1.2, "STEP 1 (68주, n=1,961)", ha="center", fontsize=9)
    ax.text(4.1, 1.2, "SURMOUNT-1 (72주, n=2,539)", ha="center", fontsize=9)
    for sp in ("top", "right"): ax.spines[sp].set_visible(False)
    fig.subplots_adjust(left=0.1, right=0.98, bottom=0.2, top=0.93)
    fig.savefig(path); plt.close(fig)
draw(False, os.path.join(out, "그림2-1.png")); draw(True, os.path.join(out, "그림2-1-흑백.png"))
