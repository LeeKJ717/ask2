# 가상 자료 생성기: 알려진 참값에서 용량-반응 자료를 만들어 분석 코드가 참값을 되찾는지 시험한다.
# 아래 매개변수는 모두 설명용 가상 값이며 실제 약물의 측정값이 아니다.
import numpy as np, json, sys
rng = np.random.default_rng(20261102)        # 시드 고정
Em = 1.0
def op(logA, logKA, logtau):                 # 작용 모형(전달 기울기 n=1), 반응은 계 최대에 대한 비율
    A, KA, tau = 10**logA, 10**logKA, 10**logtau
    return Em*tau*A/(KA + A*(1+tau))
TRUE = {   # (logKA, logtau)
 'ref':  {'cAMP': (-9.0, 1.0), 'arr': (-8.0, 0.5)},
 'test': {'cAMP': (-9.0, 1.0), 'arr': (-8.0, -0.3)},   # 시험 리간드: 베타-어레스틴 쪽 전달만 낮음
}
logA = np.linspace(-12, -6, 10); REP = 3; SD = 0.03
rows = []
for lig in TRUE:
    for path in TRUE[lig]:
        kA, t = TRUE[lig][path]
        for r in range(REP):
            y = op(logA, kA, t) + rng.normal(0, SD, logA.size)
            for a, v in zip(logA, y): rows.append((lig, path, r+1, float(a), float(v)))
with open('synth-dr.csv', 'w') as f:
    f.write('ligand,pathway,replicate,logconc,response\n')
    for r in rows: f.write(','.join(map(str, r)) + '\n')
print('rows', len(rows)); json.dump({'true': TRUE, 'sd': SD, 'seed': 20261102}, open('synth-truth.json', 'w'))
