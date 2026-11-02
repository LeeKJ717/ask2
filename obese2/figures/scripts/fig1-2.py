import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib import font_manager as fm
here = os.path.dirname(os.path.abspath(__file__)); out = os.path.join(here, "..", "out")
for f in fm.findSystemFonts():
    if "NotoSansCJK" in f: fm.fontManager.addfont(f)
names = {x.name for x in fm.fontManager.ttflist}
plt.rcParams["font.family"] = "Malgun Gothic" if "Malgun Gothic" in names else "Noto Sans CJK KR"
def draw(bw, path):
    fig, ax = plt.subplots(figsize=(6.93, 4.9), dpi=300); ax.set_xlim(0, 100); ax.set_ylim(0, 70); ax.axis("off")
    c = dict(a="#DCE9F5", b="#FBE3C8", c="#E3F1DC", d="#F6D5D5") if not bw else dict(a="#ffffff", b="#e0e0e0", c="#c8c8c8", d="#a8a8a8")
    def box(x, y, w, h, t, col, fs=9.5, bold=False):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=2", fc=col, ec="black", lw=1))
        ax.text(x + w/2, y + h/2, t, ha="center", va="center", fontsize=fs, fontweight="bold" if bold else "normal", linespacing=1.4)
    def arrow(p, q):
        ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=13, lw=1.4, color="black"))
    ax.text(25, 67, "정상: 세로토닌", ha="center", fontsize=10.5, fontweight="bold")
    ax.text(75, 67, "펜-펜 복용: 노르펜플루라민", ha="center", fontsize=10.5, fontweight="bold")
    ax.plot([50, 50], [3, 65], color="black", lw=0.8)
    # 정상
    box(7, 52, 36, 9, "혈중 세로토닌\n(농도 오르내림)", c["a"])
    box(7, 36, 36, 9, "판막 섬유모세포의\n5-HT2B 수용체: 짧은 활성", c["c"])
    box(7, 20, 36, 9, "세포 증식 신호가\n꺼졌다 켜졌다 함", c["c"])
    box(7, 4, 36, 9, "판막이 얇고\n유연하게 유지", c["c"], 9.5, True)
    # 펜펜
    box(57, 52, 36, 9, "펜플루라민이 간에서\n노르펜플루라민으로 대사", c["b"])
    box(57, 36, 36, 9, "같은 5-HT2B 수용체에\n강하게 결합·지속 활성", c["d"])
    box(57, 20, 36, 9, "증식 신호가\n꺼지지 않음 → 섬유증식", c["d"])
    box(57, 4, 36, 9, "판막 비후·역류\n(심초음파 소견)", c["d"], 9.5, True)
    for x in (25, 75):
        for y0, y1 in ((52, 45.8), (36, 29.8), (20, 13.8)):
            arrow((x, y0 - 0.2), (x, y1))
    fig.subplots_adjust(left=0,right=1,bottom=0,top=1); fig.savefig(path); plt.close(fig)
draw(False, os.path.join(out, "그림1-2.png")); draw(True, os.path.join(out, "그림1-2-흑백.png"))
