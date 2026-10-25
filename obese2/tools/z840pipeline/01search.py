#!/usr/bin/env python3
"""01search.py - PubMed esearch (year-bisected) + efetch -> papers table.
Usage: python3 01search.py [--axes a,b] [--target N] [--from 1985] [--to 2026]
Re-runnable: existing PMIDs only get their axes list merged.
"""
import argparse, datetime, re, sys, time
import xml.etree.ElementTree as ET
from common import *

EU = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
SLEEP = 0.12 if NCBI_KEY else 0.37

DRUG = (
    '(semaglutide[tiab] OR liraglutide[tiab] OR tirzepatide[tiab] OR orforglipron[tiab] '
    'OR cagrilintide[tiab] OR cagrisema[tiab] OR retatrutide[tiab] OR survodutide[tiab] '
    'OR mazdutide[tiab] OR exenatide[tiab] OR dulaglutide[tiab] OR lixisenatide[tiab] '
    'OR "GLP-1 receptor agonist*"[tiab] OR "GLP-1RA*"[tiab] OR "glucagon-like peptide-1"[tiab] '
    'OR "glucagon-like peptide 1"[tiab] OR "GIP receptor"[tiab] OR "GIPR"[tiab] OR "GLP1R"[tiab] '
    'OR "glucose-dependent insulinotropic"[tiab] OR "gastric inhibitory polypeptide"[tiab] '
    'OR incretin*[tiab] OR amylin[tiab] OR "amylin analog*"[tiab] OR "dual agonist*"[tiab] '
    'OR "triple agonist*"[tiab] OR "anti-obesity medication*"[tiab] OR "antiobesity drug*"[tiab] '
    'OR "anti-obesity drug*"[tiab] OR "weight loss drug*"[tiab] OR "weight-loss medication*"[tiab] '
    'OR setmelanotide[tiab] OR "naltrexone-bupropion"[tiab] OR "phentermine-topiramate"[tiab] '
    'OR orlistat[tiab] OR "glucagon receptor"[tiab])'
)

AXES = {
    "physiology": DRUG + ' AND (physiolog*[tiab] OR appetite[tiab] OR satiety[tiab] OR "gastric emptying"[tiab] '
        'OR hypothalam*[tiab] OR "energy expenditure"[tiab] OR "food intake"[tiab] OR brainstem[tiab] '
        'OR "area postrema"[tiab] OR vagal[tiab] OR "nucleus tractus solitarius"[tiab] OR "reward"[tiab] '
        'OR "body weight regulation"[tiab] OR "insulin secretion"[tiab])',
    "cytology": DRUG + ' AND ("beta cell*"[tiab] OR "β-cell*"[tiab] OR adipocyte*[tiab] OR "signal transduction"[tiab] '
        'OR cAMP[tiab] OR internalization[tiab] OR "beta-arrestin"[tiab] OR endosom*[tiab] OR "cell signaling"[tiab] '
        'OR "cell signalling"[tiab] OR neuron*[tiab] OR apoptosis[tiab] OR autophagy[tiab] OR "cell proliferation"[tiab] '
        'OR "organelle"[tiab] OR mitochondri*[tiab] OR "endoplasmic reticulum"[tiab])',
    "biochemistry": DRUG + ' AND (biochemi*[tiab] OR pharmacokinetic*[tiab] OR "albumin binding"[tiab] '
        'OR "DPP-4"[tiab] OR "dipeptidyl peptidase"[tiab] OR "peptide stability"[tiab] OR lipolysis[tiab] '
        'OR "lipid metabolism"[tiab] OR gluconeogenesis[tiab] OR "glucagon secretion"[tiab] OR "fatty acid"[tiab] '
        'OR "protein kinase"[tiab] OR "second messenger"[tiab] OR "enzyme"[tiab] OR "oral absorption"[tiab] '
        'OR "SNAC"[tiab] OR "half-life"[tiab])',
    "genetics": DRUG + ' AND (genetic*[tiab] OR polymorphism*[tiab] OR "single nucleotide"[tiab] OR GWAS[tiab] '
        'OR pharmacogen*[tiab] OR "gene expression"[tiab] OR transcriptom*[tiab] OR epigen*[tiab] '
        'OR "mendelian randomization"[tiab] OR variant*[tiab] OR knockout[tiab] OR "knock-out"[tiab] '
        'OR "single-cell"[tiab] OR "RNA-seq"[tiab] OR "gene polymorphism"[tiab] OR methylation[tiab])',
    "proteomics_structure": DRUG + ' AND (proteom*[tiab] OR "cryo-EM"[tiab] OR "cryo-electron"[tiab] '
        'OR "crystal structure"[tiab] OR "structural basis"[tiab] OR "molecular dynamics"[tiab] '
        'OR "biased agonism"[tiab] OR "biased signaling"[tiab] OR "receptor structure"[tiab] '
        'OR "mass spectrometry"[tiab] OR "protein structure"[tiab] OR "ligand binding"[tiab] OR "peptide structure"[tiab])',
    "receptor_pharmacology": '("GLP-1 receptor"[tiab] OR "GLP1R"[tiab] OR "GIP receptor"[tiab] OR "GIPR"[tiab] '
        'OR "glucagon receptor"[tiab] OR "amylin receptor"[tiab] OR "calcitonin receptor"[tiab] OR "RAMP"[tiab]) '
        'AND (pharmacolog*[tiab] OR agonist*[tiab] OR "signaling bias"[tiab] OR desensiti*[tiab] '
        'OR "allosteric"[tiab] OR "small molecule"[tiab] OR "non-peptide"[tiab])',
    "organ_effects": DRUG + ' AND (liver[tiab] OR hepat*[tiab] OR MASLD[tiab] OR NAFLD[tiab] OR kidney[tiab] OR renal[tiab] '
        'OR cardiac[tiab] OR cardiovascular[tiab] OR bone[tiab] OR "skeletal muscle"[tiab] OR "lean mass"[tiab] '
        'OR pancrea*[tiab] OR "gut microbiota"[tiab] OR "adipose tissue"[tiab] OR brain[tiab] OR "sleep apnea"[tiab])',
    "clinical_trials": DRUG + ' AND (obesity[tiab] OR overweight[tiab] OR "weight management"[tiab]) '
        'AND ("randomized controlled trial"[pt] OR "clinical trial"[pt] OR "meta-analysis"[pt] OR "systematic review"[pt])',
    "safety_adverse": DRUG + ' AND ("adverse event*"[tiab] OR safety[tiab] OR pancreatitis[tiab] OR gallbladder[tiab] '
        'OR "thyroid C-cell"[tiab] OR "gastrointestinal"[tiab] OR nausea[tiab] OR "weight regain"[tiab] '
        'OR discontinuation[tiab] OR "muscle loss"[tiab] OR retinopath*[tiab])',
    # ---- v2: cell signaling + new-drug discovery axes ----
    "cell_signaling": '("GLP-1 receptor"[tiab] OR GLP1R[tiab] OR "GIP receptor"[tiab] OR GIPR[tiab] '
        'OR "glucagon receptor"[tiab] OR "amylin receptor"[tiab] OR "melanocortin 4 receptor"[tiab] OR MC4R[tiab] '
        'OR "leptin receptor"[tiab] OR GFRAL[tiab] OR incretin*[tiab]) '
        'AND (cAMP[tiab] OR PKA[tiab] OR EPAC*[tiab] OR "beta-arrestin"[tiab] OR "β-arrestin"[tiab] OR MAPK[tiab] '
        'OR ERK[tiab] OR AMPK[tiab] OR mTOR[tiab] OR PI3K[tiab] OR "JAK-STAT"[tiab] OR STAT3[tiab] '
        'OR "calcium signaling"[tiab] OR "G protein"[tiab] OR "signal transduction"[tiab] OR "signaling pathway*"[tiab] '
        'OR "receptor internalization"[tiab] OR "receptor trafficking"[tiab] OR "biased signaling"[tiab] OR "biased agonism"[tiab])',
    "hypothalamic_targets": '(obesity[tiab] OR "body weight"[tiab] OR "food intake"[tiab] OR appetite[tiab]) '
        'AND (leptin[tiab] OR melanocortin*[tiab] OR POMC[tiab] OR AgRP[tiab] OR NPY[tiab] OR "peptide YY"[tiab] OR PYY[tiab] '
        'OR GDF15[tiab] OR GFRAL[tiab] OR ghrelin[tiab] OR cholecystokinin[tiab] OR oxyntomodulin[tiab] '
        'OR "cannabinoid receptor"[tiab] OR "activin receptor"[tiab] OR myostatin[tiab] OR "neuropeptide"[tiab]) '
        'AND (agonist*[tiab] OR antagonist*[tiab] OR therapeutic*[tiab] OR drug*[tiab] OR "clinical trial"[tiab])',
    "drug_discovery": '(obesity[tiab] OR "anti-obesity"[tiab] OR "weight loss"[tiab]) '
        'AND ("drug discovery"[tiab] OR "drug design"[tiab] OR "lead optimization"[tiab] OR "structure-based"[tiab] '
        'OR "small molecule*"[tiab] OR allosteric[tiab] OR "peptide engineering"[tiab] OR "novel target*"[tiab] '
        'OR "high-throughput screening"[tiab] OR pharmacophore[tiab] OR "co-agonist*"[tiab] OR unimolecular[tiab] '
        'OR "structure-activity"[tiab] OR "next-generation"[tiab]) '
        'AND (GLP-1[tiab] OR GLP1R[tiab] OR incretin*[tiab] OR amylin[tiab] OR melanocortin*[tiab] OR GIPR[tiab] '
        'OR glucagon[tiab] OR "G protein-coupled"[tiab] OR GPCR[tiab])',
    "clinical_named": '(semaglutide[tiab] OR tirzepatide[tiab] OR liraglutide[tiab] OR orforglipron[tiab] OR retatrutide[tiab] '
        'OR survodutide[tiab] OR mazdutide[tiab] OR cagrilintide[tiab] OR cagrisema[tiab] OR setmelanotide[tiab] '
        'OR dulaglutide[tiab] OR exenatide[tiab] OR ecnoglutide[tiab] OR efpeglenatide[tiab]) '
        'AND (obesity[tiab] OR overweight[tiab] OR "weight loss"[tiab] OR "body weight"[tiab]) '
        'AND ("randomized controlled trial"[pt] OR "clinical trial"[pt] OR "meta-analysis"[pt] OR "systematic review"[pt])',
    "structure_gpcr": '("GLP-1 receptor"[tiab] OR GLP1R[tiab] OR "GIP receptor"[tiab] OR "glucagon receptor"[tiab] '
        'OR "amylin receptor"[tiab] OR "melanocortin 4 receptor"[tiab] OR "class B GPCR*"[tiab] OR "class B G protein-coupled"[tiab]) '
        'AND ("cryo-EM"[tiab] OR "cryo-electron"[tiab] OR "crystal structure"[tiab] OR "structural basis"[tiab] '
        'OR "binding pocket"[tiab] OR allosteric[tiab] OR "receptor activation"[tiab] OR "molecular dynamics"[tiab])',
    "smallmol_agonist": '("GLP-1 receptor"[tiab] OR GLP1R[tiab] OR GIPR[tiab] OR "glucagon receptor"[tiab] '
        'OR "amylin receptor"[tiab] OR MC4R[tiab]) '
        'AND ("small molecule*"[tiab] OR "non-peptide"[tiab] OR nonpeptide[tiab] OR orforglipron[tiab] OR danuglipron[tiab] '
        'OR "positive allosteric modulator*"[tiab] OR "virtual screening"[tiab] OR docking[tiab] OR "structure-activity"[tiab])',
    "comp_method": '("GLP-1"[tiab] OR GLP1R[tiab] OR incretin*[tiab] OR "class B GPCR*"[tiab] OR "G protein-coupled receptor*"[tiab]) '
        'AND ("biased agonism"[tiab] OR "bias factor*"[tiab] OR "operational model"[tiab] OR "machine learning"[tiab] '
        'OR "deep learning"[tiab] OR "mathematical model*"[tiab] OR "kinetic model*"[tiab] OR "free energy"[tiab] '
        'OR "virtual screening"[tiab] OR "de novo design"[tiab] OR AlphaFold[tiab])',
}


def esearch(term, y0, y1, retmax=0, retstart=0):
    p = dict(db="pubmed", term=term, datetype="pdat", mindate=str(y0), maxdate=str(y1),
             retmax=retmax, retstart=retstart, retmode="json")
    if NCBI_KEY:
        p["api_key"] = NCBI_KEY
    throttle(SLEEP)
    r = post(EU + "esearch.fcgi", p)
    r.raise_for_status()
    return r.json()["esearchresult"]


def ranges(term, y0, y1, limit=9000):
    """split year range until each sub-range returns <= limit hits."""
    cnt = int(esearch(term, y0, y1)["count"])
    if cnt == 0:
        return []
    if cnt <= limit or y0 == y1:
        return [(y0, y1, cnt)]
    mid = (y0 + y1) // 2
    return ranges(term, y0, mid, limit) + ranges(term, mid + 1, y1, limit)


def collect_pmids(term, y0, y1, target=0):
    out = []
    for a, b, cnt in ranges(term, y0, y1):
        if cnt > 9990:   # single year >10k: take what esearch allows
            log("WARN range %d-%d has %d hits (esearch cap 10000)" % (a, b, cnt))
        got = 0
        while got < min(cnt, 9999):
            res = esearch(term, a, b, retmax=min(5000, 9999 - got), retstart=got)
            ids = res.get("idlist", [])
            if not ids:
                break
            out.extend(int(x) for x in ids)
            got += len(ids)
        log("  range %d-%d hits=%d fetched=%d" % (a, b, cnt, got))
        if target and len(out) >= target:
            return out[:target]
    return out


def txt(el):
    return "".join(el.itertext()).strip() if el is not None else ""


def parse_pubmed(xml_bytes):
    root = ET.fromstring(xml_bytes)
    rows = []
    for art in root.findall(".//PubmedArticle"):
        mc = art.find("MedlineCitation")
        pmid = int(txt(mc.find("PMID")))
        a = mc.find("Article")
        title = txt(a.find("ArticleTitle"))
        abs_parts = []
        for t in a.findall("Abstract/AbstractText"):
            lab = t.get("Label")
            s = txt(t)
            abs_parts.append((lab + ": " if lab else "") + s)
        abstract = "\n".join(abs_parts)
        journal = txt(a.find("Journal/Title"))
        year = None
        y = a.find("Journal/JournalIssue/PubDate/Year")
        if y is not None and txt(y).isdigit():
            year = int(txt(y))
        else:
            md = txt(a.find("Journal/JournalIssue/PubDate/MedlineDate"))
            m = re.search(r"(19|20)\d\d", md)
            if m:
                year = int(m.group(0))
        if year is None:
            for p in a.findall("ArticleDate/Year"):
                if txt(p).isdigit():
                    year = int(txt(p))
        auth = []
        for au in a.findall("AuthorList/Author"):
            ln, ini = txt(au.find("LastName")), txt(au.find("Initials"))
            if ln:
                auth.append((ln + " " + ini).strip())
            elif au.find("CollectiveName") is not None:
                auth.append(txt(au.find("CollectiveName")))
        ptypes = "; ".join(txt(x) for x in a.findall("PublicationTypeList/PublicationType"))
        mesh = "; ".join(txt(x) for x in mc.findall("MeshHeadingList/MeshHeading/DescriptorName"))
        pmcid = doi = None
        for aid in art.findall("PubmedData/ArticleIdList/ArticleId"):
            t = aid.get("IdType")
            if t == "pmc":
                pmcid = txt(aid)
            elif t == "doi":
                doi = txt(aid).lower()
        if doi is None:
            for e in a.findall("ELocationID"):
                if e.get("EIdType") == "doi":
                    doi = txt(e).lower()
        rows.append(dict(pmid=pmid, pmcid=pmcid, doi=doi, title=title, abstract=abstract,
                         journal=journal[:500], year=year, authors="; ".join(auth),
                         ptypes=ptypes, mesh=mesh))
    return rows


def efetch(ids):
    p = dict(db="pubmed", id=",".join(str(i) for i in ids), retmode="xml")
    if NCBI_KEY:
        p["api_key"] = NCBI_KEY
    throttle(SLEEP)
    r = post(EU + "efetch.fcgi", p)
    r.raise_for_status()
    return parse_pubmed(r.content)


UPSERT = (
    "INSERT INTO papers (pmid,pmcid,doi,title,abstract,journal,pub_year,authors,pub_types,mesh,axes) "
    "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
    "ON DUPLICATE KEY UPDATE axes=IF(FIND_IN_SET(%s,axes), axes, IF(axes='', %s, CONCAT(axes,',',%s))), "
    "pmcid=COALESCE(pmcid,VALUES(pmcid)), doi=COALESCE(doi,VALUES(doi))"
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--axes", default=",".join(AXES))
    ap.add_argument("--target", type=int, default=0, help="max PMIDs per axis (0=all)")
    ap.add_argument("--from", dest="y0", type=int, default=1985)
    ap.add_argument("--to", dest="y1", type=int, default=datetime.date.today().year)
    a = ap.parse_args()
    db = conn()
    cur = db.cursor()
    for ax in a.axes.split(","):
        ax = ax.strip()
        if ax not in AXES:
            log("unknown axis", ax)
            continue
        log("axis", ax)
        ids = collect_pmids(AXES[ax], a.y0, a.y1, a.target)
        ids = list(dict.fromkeys(ids))
        cur.execute("SELECT pmid FROM papers WHERE FIND_IN_SET(%s,axes)", (ax,))
        have = {r[0] for r in cur.fetchall()}
        todo = [i for i in ids if i not in have]
        cur.execute("INSERT INTO search_log (axis,yr_from,yr_to,hits) VALUES (%s,%s,%s,%s)",
                    (ax, a.y0, a.y1, len(ids)))
        log("  axis %s: %d ids, %d new for this axis" % (ax, len(ids), len(todo)))
        for i in range(0, len(todo), 200):
            batch = todo[i:i + 200]
            try:
                rows = efetch(batch)
            except Exception as e:
                log("  efetch fail", e)
                continue
            for r in rows:
                cur.execute(UPSERT, (r["pmid"], r["pmcid"], r["doi"], r["title"], r["abstract"],
                                     r["journal"], r["year"], r["authors"], r["ptypes"], r["mesh"], ax,
                                     ax, ax, ax))
            if (i // 200) % 10 == 0:
                log("  %s efetch %d/%d" % (ax, min(i + 200, len(todo)), len(todo)))
    cur.execute("SELECT COUNT(*) FROM papers")
    log("papers total:", cur.fetchone()[0])


if __name__ == "__main__":
    main()
