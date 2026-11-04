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
    fig, ax = plt.subplots(figsize=(6.93, 5.2), dpi=300); ax.set_xlim(0, 100); ax.set_ylim(0, 75); ax.axis("off")
    c = dict(n="#DCE9F5", e="#FBE3C8", l="#E3F1DC", s="#F6D5D5", t="#E8DDF0") if not bw else dict(n="#ffffff", e="#e6e6e6", l="#d0d0d0", s="#b0b0b0", t="#c0c0c0")
    def box(x, y, w, h, t, col, fs=8.6, bold=False):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3,rounding_size=1.8", fc=col, ec="black", lw=1))
        ax.text(x + w/2, y + h/2, t, ha="center", va="center", fontsize=fs, fontweight="bold" if bold else "normal", linespacing=1.4)
    def arrow(p, q, label=None, lx=0, ly=0):
        ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=12, lw=1.3, color="black"))
        if label:
            ax.text((p[0]+q[0])/2 + lx, (p[1]+q[1])/2 + ly, label, ha="center", va="center", fontsize=7.6,
                    bbox=dict(fc="white", ec="none", pad=1.2))
    # 천연 GLP-1 (위쪽 중앙)
    box(33, 62, 34, 10, "천연 GLP-1\n반감기 1~2분 · DPP-4가 2번 알라닌 절단", c["n"], 8.4, True)
    # 도마뱀 계열 (왼쪽)
    box(2, 38, 30, 10, "엑센딘-4 (1992)\n길라 몬스터 독 · DPP-4 저항", c["e"])
    box(2, 18, 30, 10, "엑세나타이드 (2005 승인)\n하루 2회 주사", c["e"], 8.6, True)
    # 지방산 계열 (가운데)
    box(35, 38, 30, 10, "서열 개조 + 지방산 곁사슬\n(알부민에 매달기)", c["l"])
    box(35, 18, 30, 10, "리라글루타이드\nC16 · 약 13시간 · 하루 1회", c["l"], 8.6, True)
    # 세마글루타이드 (오른쪽)
    box(68, 38, 30, 10, "8번 Aib 치환 +\nC18 이산 곁사슬", c["s"])
    box(68, 18, 30, 10, "세마글루타이드\n약 1주 · 주 1회 (위고비 2021)", c["s"], 8.6, True)
    # 티르제파타이드
    box(68, 2, 30, 9, "티르제파타이드\nGIP·GLP-1 두 수용체 동시 활성", c["t"], 8.6, True)
    # 화살표
    arrow((42, 62), (17, 48.4), "자연의 DPP-4 저항 분자", -9, 2.5)
    arrow((50, 62), (50, 48.4))
    arrow((17, 38), (17, 28.4))
    arrow((50, 38), (50, 28.4))
    arrow((58, 62), (83, 48.4), "같은 서열에서 더 강한 설계", 9, 3)
    arrow((83, 38), (83, 28.4))
    arrow((83, 18), (83, 11.4), "수용체 하나 더", 9.5, 0)
    ax.text(34, 7, "같은 호르몬, 다른 설계:\n분해 저항과 알부민 결합이 커질수록\n투여 간격이 길어진다", ha="center", va="center", fontsize=8.2, linespacing=1.5)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1); fig.savefig(path); plt.close(fig)
draw(False, os.path.join(out, "그림2-2.png")); draw(True, os.path.join(out, "그림2-2-흑백.png"))
