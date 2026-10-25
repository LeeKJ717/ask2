import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib import font_manager as fm
here = os.path.dirname(os.path.abspath(__file__)); out = os.path.join(here, "..", "out")
for f in fm.findSystemFonts():
    if "NotoSansCJK" in f or "alg" in f.lower() and "malgun" in f.lower(): fm.fontManager.addfont(f)
names = {x.name for x in fm.fontManager.ttflist}
plt.rcParams["font.family"] = "Malgun Gothic" if "Malgun Gothic" in names else "Noto Sans CJK KR"
def draw(bw, path):
    fig, ax = plt.subplots(figsize=(6.93, 4.4), dpi=300); ax.set_xlim(0, 100); ax.set_ylim(0, 62); ax.axis("off")
    c = dict(a="#DCE9F5", b="#FBE3C8", c="#E3F1DC", d="#F6D5D5") if not bw else dict(a="#ffffff", b="#e0e0e0", c="#c8c8c8", d="#a8a8a8")
    def box(x, y, w, h, t, col, fs=10, bold=False):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=2", fc=col, ec="black", lw=1))
        ax.text(x + w/2, y + h/2, t, ha="center", va="center", fontsize=fs, fontweight="bold" if bold else "normal", linespacing=1.4)
    def arrow(p, q):
        ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=14, lw=1.4, color="black"))
    box(3, 38, 26, 16, "섭취 에너지\n(식사: 탄수화물·지방·\n단백질)", c["a"])
    box(37, 22, 26, 18, "에너지 저장고\n지방조직\n(중성지방)", c["d"], 11, True)
    box(71, 38, 26, 16, "소비 에너지\n(기초대사·활동·\n식후 열발생)", c["b"])
    box(3, 4, 26, 14, "시상하부\n(식욕·에너지 소비 조절)", c["c"], 9.5)
    box(71, 4, 26, 14, "호르몬 신호\n(렙틴·인슐린·\n인크레틴)", c["c"], 9.5)
    arrow((29, 44), (42, 40.5)); arrow((58, 40.5), (71, 44))
    arrow((16, 18.5), (16, 37)); arrow((84, 18.5), (84, 37))
    arrow((71, 11), (29, 11)); arrow((50, 21.5), (82, 18.8))
    ax.text(50, 58, "에너지 수지: 들어온 양 − 나간 양 = 저장량 변화", ha="center", fontsize=10.5, fontweight="bold")
    fig.subplots_adjust(left=0,right=1,bottom=0,top=1); fig.savefig(path); plt.close(fig)
draw(False, os.path.join(out, "그림1-2.png")); draw(True, os.path.join(out, "그림1-2-흑백.png"))
