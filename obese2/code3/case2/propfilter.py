# 성질 필터와 PAINS 경고 표시. 입력 CSV: id,smiles  →  출력 CSV: 성질과 통과 여부
import csv, sys
from rdkit import Chem
from rdkit.Chem import Descriptors, Crippen, Lipinski, rdMolDescriptors
from rdkit.Chem.FilterCatalog import FilterCatalog, FilterCatalogParams
P = FilterCatalogParams(); P.AddCatalog(FilterCatalogParams.FilterCatalogs.PAINS); CAT = FilterCatalog(P)
LIM = dict(mw=(150, 600), logp=(-1, 5.5), hbd=(0, 5), hba=(0, 10), rotb=(0, 10))   # 계획서에 사전 기록할 기준(예)
def props(m):
    return dict(mw=Descriptors.MolWt(m), logp=Crippen.MolLogP(m), hbd=Lipinski.NumHDonors(m),
                hba=Lipinski.NumHAcceptors(m), rotb=rdMolDescriptors.CalcNumRotatableBonds(m),
                tpsa=rdMolDescriptors.CalcTPSA(m))
def main(src, dst):
    out, bad = [], 0
    for r in csv.DictReader(open(src)):
        m = Chem.MolFromSmiles(r['smiles'])
        if m is None: bad += 1; continue
        p = props(m); ok = all(LIM[k][0] <= p[k] <= LIM[k][1] for k in LIM)
        pains = CAT.HasMatch(m)
        out.append(dict(id=r['id'], smiles=Chem.MolToSmiles(m), **{k: round(v, 2) for k, v in p.items()}, pass_props=ok, pains=pains))
    with open(dst, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
    print('읽기 실패', bad, '| 입력', len(out)+bad, '| 성질 통과', sum(o['pass_props'] for o in out), '| PAINS 경고', sum(o['pains'] for o in out))
if __name__ == '__main__': main(sys.argv[1], sys.argv[2])
