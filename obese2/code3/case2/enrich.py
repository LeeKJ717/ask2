# 도킹 점수로 활성 분자와 유인 분자가 구분되는지 평가(AUC, 농축 계수). 점수는 낮을수록 좋다고 가정.
import numpy as np
from sklearn.metrics import roc_auc_score
def evaluate(scores_act, scores_dec, frac=0.01):
    y = np.r_[np.ones(len(scores_act)), np.zeros(len(scores_dec))]
    s = -np.r_[scores_act, scores_dec]            # 점수가 낮을수록 활성 → 부호 반전
    auc = roc_auc_score(y, s)
    n = len(y); top = max(1, int(round(n*frac))); idx = np.argsort(-s)[:top]
    ef = (y[idx].sum()/top) / (y.sum()/n)         # EF = (상위 x%의 활성 비율) / (전체 활성 비율)
    return auc, ef
if __name__ == '__main__':      # 코드 작동 시험: 가상 점수(실제 도킹 결과 아님)
    rng = np.random.default_rng(1)
    act = rng.normal(-8.0, 1.0, 50); dec = rng.normal(-7.0, 1.0, 2500)
    print('AUC, EF1%:', evaluate(act, dec))
