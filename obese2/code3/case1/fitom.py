# 용량-반응 적합 → log(τ/KA) → 편향 계수 ΔΔlog(τ/KA), 부트스트랩 신뢰구간
import numpy as np, json, csv
from scipy.optimize import curve_fit
rng = np.random.default_rng(7)
D = {}
for r in csv.DictReader(open('synth-dr.csv')):
    D.setdefault((r['ligand'], r['pathway']), []).append((float(r['logconc']), float(r['response'])))
def f(x, emax, logec50): return emax/(1+10**(logec50-x))      # 기울기 1, 바닥 0
def fit(pts):
    x, y = np.array(pts).T
    p, _ = curve_fit(f, x, y, p0=[max(y), np.median(x)], maxfev=20000)
    return p
def logR(p): return np.log10(p[0]) - p[1]        # log(Emax/EC50) = log(τ/KA)+logEm (Em은 차이에서 소거)
def delta(ref, test): return logR(fit(test)) - logR(fit(ref))
def bias(d):
    return delta(d[('ref','cAMP')], d[('test','cAMP')]) - delta(d[('ref','arr')], d[('test','arr')])
est = bias(D)
boot = []
for _ in range(2000):
    d2 = {k: [v[i] for i in rng.integers(0, len(v), len(v))] for k, v in D.items()}
    try: boot.append(bias(d2))
    except Exception: pass
lo, hi = np.percentile(boot, [2.5, 97.5])
out = {'bias_log': est, 'ci95': [lo, hi], 'bias_fold': 10**est, 'n_boot': len(boot),
       'fits': {f'{k[0]}-{k[1]}': list(map(float, fit(v))) for k, v in D.items()}}
json.dump(out, open('fit-result.json', 'w'), indent=1); print(json.dumps(out, indent=1))
