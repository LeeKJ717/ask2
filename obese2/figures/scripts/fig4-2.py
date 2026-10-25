# -*- coding: utf-8 -*-
import os, numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from PIL import Image
for p in fm.findSystemFonts():
    if 'NotoSansCJK' in p or 'Malgun' in p or 'malgun' in p: fm.fontManager.addfont(p)
plt.rcParams['font.family'] = ['Noto Sans CJK KR','sans-serif']
here = os.path.dirname(os.path.abspath(__file__)); out = os.path.join(here, '..', 'out')
t = np.linspace(0, 240, 400)
def pk(t0, tp, w, h, base=0): return base + h*np.exp(-((t-tp)**2)/(2*w**2))*(t>=t0) + (h*np.exp(-((t0-tp)**2)/(2*w**2)))*0
def rise(tp, w, h, base=0, skew=1.0):
    x = np.clip(t, 0, None); return base + h*(x/tp)**skew*np.exp(skew*(1-x/tp))
curves = [  # (이름, 곡선, 선모양, 색, 흑백용 회색)
 ('인슐린', rise(40, 1, 1.0, 0.05, 2.2), '-', '#2b5d7c', '#222222'),
 ('GLP-1·PYY (L세포)', rise(60, 1, 0.9, 0.08, 1.4), '-', '#8a6a25', '#555555'),
 ('GIP (K세포)', rise(45, 1, 0.85, 0.1, 1.8), '--', '#3f6b4a', '#777777'),
 ('콜레시스토키닌', rise(30, 1, 0.7, 0.05, 2.0), ':', '#6b4a8a', '#999999'),
 ('그렐린 (식전 정점→식후 억제)', 0.9-0.7*(1-np.exp(-t/12))*np.exp(-t/110), '-.', '#a0522d', '#333333'),
]
for color in (True, False):
    fig, ax = plt.subplots(figsize=(6.93, 4.3), dpi=300)
    for n, y, ls, c, g in curves:
        ax.plot(t, y, ls, color=c if color else g, lw=2.2, label=n)
    ax.axvspan(0, 15, color='#dddddd' if not color else '#e8e2d0', alpha=.9)
    ax.text(7.5, 1.12, '식사', ha='center', fontsize=9)
    ax.set_xlabel('식사 시작 후 시간(분, 개념도)', fontsize=10); ax.set_ylabel('상대 농도(식전 기준 비교용, 임의 단위)', fontsize=9)
    ax.set_xlim(0, 240); ax.set_ylim(0, 1.2); ax.set_yticks([]); 
    for s in ('top','right'): ax.spines[s].set_visible(False)
    ax.legend(fontsize=8.5, frameon=False, loc='upper center', bbox_to_anchor=(0.5, -0.17), ncol=3)
    fig.tight_layout()
    fn = '그림4-2.png' if color else '그림4-2-흑백.png'
    fig.savefig(os.path.join(out, fn), facecolor='white'); plt.close(fig)
print('ok')
