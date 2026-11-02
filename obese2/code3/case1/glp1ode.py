# GLP1R → Gs → AC → cAMP → PKA 최소 모델과 매개변수 훑기. 모든 매개변수는 설명용 가상 값이다.
import numpy as np, json
from scipy.integrate import solve_ivp
P = dict(kon=1e6, koff=1e-3, kact=0.5, kinact=0.2, kac=1.0, kpde=0.5, Rt=1.0, Gt=1.0)  # 단위: 임의(농도 M, 1/s 등은 가상)
def rhs(t, y, L, p):
    R, LR, Gs, cAMP = y                         # R: 자유 수용체, LR: 결합 수용체, Gs: 활성 Gs 비율, cAMP: 임의 단위
    bind = p['kon']*L*R - p['koff']*LR
    dGs = p['kact']*LR*(p['Gt']-Gs) - p['kinact']*Gs
    dcAMP = p['kac']*Gs - p['kpde']*cAMP
    return [-bind, bind, dGs, dcAMP]
def peak(L, p, T=600):
    s = solve_ivp(rhs, (0, T), [p['Rt'], 0, 0, 0], args=(L, p), t_eval=np.linspace(0, T, 601), rtol=1e-8, atol=1e-10)
    return s.t, s.y[3]
def run():
    doses = [1e-10, 1e-9, 1e-8, 1e-7]
    series = {}
    for L in doses:
        t, c = peak(L, P); series[str(L)] = c[::10].tolist()
    ka = np.logspace(-1, 1, 15); kp = np.logspace(-1, 1, 15)
    grid = np.zeros((15, 15))
    for i, a in enumerate(ka):
        for j, b in enumerate(kp):
            q = dict(P, kact=a, kpde=b); grid[i, j] = peak(1e-8, q)[1].max()
    json.dump({'t': list(range(0, 601, 10)), 'series': series, 'kact': ka.tolist(), 'kpde': kp.tolist(), 'grid': grid.tolist()}, open('ode-result.json', 'w'))
    print('시계열 용량', doses, '최고 cAMP', {k: round(max(v), 4) for k, v in series.items()})
    print('격자 최소/최대', round(grid.min(), 4), round(grid.max(), 4))
run()
