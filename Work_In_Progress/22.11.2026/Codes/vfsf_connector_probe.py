#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VFSF Connector Matrix & qo-Residue Probe
1) Testaa Etäisyys 1 vs 2 sen jälkeen kun (o+l, r+ai, s+ai) on yhdistetty.
2) Purkaa qo-sanojen sisäisen Z=+2.34 jäänteen (qok vs qot vs loppupääte).
3) Tulostaa täyden 6x8 loppukirjain -> alkukirjain yhteensopivuusmatriisin.
"""
import re
import sys
import os
import math
import random
from collections import Counter, defaultdict


def load_clean_lines(filepath):
    lines = []
    par_id = 0
    cur_fol = "unknown"
    prev_end = True
    with open(filepath, 'r', encoding='utf-8') as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith('#'):
                continue
            m = re.search(r'<f(\d+[rv]\d*)([^>]*)>', line.lower())
            is_par = False
            if m:
                nf, meta = m.group(1), m.group(2)
                if nf != cur_fol or '@p' in meta or prev_end:
                    is_par = True
                    par_id += 1
                cur_fol = nf
            prev_end = ('<$>' in line)
            no_tags = re.sub(r'<[^>]+>|\{[^}]+\}|\[[^\]]+\]|@[0-9;]+', '', line).lower()
            no_tags = no_tags.replace('!', '').replace("'", "").replace("’", "").replace(',', '')
            no_tags = re.sub(r'[^a-z.\s]', ' ', no_tags)
            words = [w.strip() for w in re.split(r'[\s.]+', no_tags)
                     if w.strip() and not re.match(r'^f\d+[rv]\d*$', w.strip())]
            if words:
                lines.append((par_id, is_par, words))
    return lines


def calc_mi(pairs):
    n = len(pairs)
    if n == 0:
        return 0.0
    ca = Counter(a for a, _ in pairs)
    cb = Counter(b for _, b in pairs)
    cab = Counter(pairs)
    return sum((c / n) * math.log2((c / n) / ((ca[a] / n) * (cb[b] / n)))
               for (a, b), c in cab.items())


def tail_class(w):
    for s in ('aiin', 'ain', 'iin', 'dy', 'ey', 'hy', 'ky', 'ty', 'ly', 'ol', 'or', 'al', 'ar'):
        if w.endswith(s):
            return s
    return w[-1] if w else 'NONE'


def main(filepath, iters=200):
    if not os.path.exists(filepath):
        print(f"Virhe: '{filepath}' ei löydy.")
        return

    lines = load_clean_lines(filepath)
    rng = random.Random(1337)

    # --- 1. YHDISTETÄÄN o+l, r+ai, s+ai JA MITATAAN ETÄISYYS 1 vs 2 ---
    merged = []
    for pid, is_par, ws in lines:
        mws = []
        i = 0
        while i < len(ws):
            if i + 1 < len(ws):
                w1, w2 = ws[i], ws[i + 1]
                if (w1.endswith('o') and w2.startswith('l')) or (w1.endswith(('r', 's')) and w2.startswith('ai')):
                    mws.append(w1 + w2)
                    i += 2
                    continue
            mws.append(ws[i])
            i += 1
        if mws:
            merged.append((pid, is_par, mws))

    buckets = defaultdict(list)
    for pid, is_par, ws in merged:
        n = len(ws)
        for i, w in enumerate(ws):
            pos = 'S' if n == 1 else ('PF' if (i == 0 and is_par) else ('LF' if i == 0 else ('LL' if i == n - 1 else 'LM')))
            buckets[(pid, pos)].append(w)

    def cmi(src, d):
        return calc_mi([(ws[i][-1], ws[i + d][0]) for _, _, ws in src if len(ws) > d for i in range(len(ws) - d)])

    sd1, sd2 = [], []
    for _ in range(iters):
        sb = {k: v.copy() for k, v in buckets.items()}
        for k in sb:
            rng.shuffle(sb[k])
        cnt = defaultdict(int)
        sl = []
        for pid, is_par, ws in merged:
            n = len(ws)
            nw = []
            for i in range(n):
                pos = 'S' if n == 1 else ('PF' if (i == 0 and is_par) else ('LF' if i == 0 else ('LL' if i == n - 1 else 'LM')))
                nw.append(sb[(pid, pos)][cnt[(pid, pos)]])
                cnt[(pid, pos)] += 1
            sl.append((pid, is_par, nw))
        sd1.append(cmi(sl, 1))
        sd2.append(cmi(sl, 2))

    r1, r2 = cmi(merged, 1), cmi(merged, 2)
    m1, m2 = sum(sd1) / iters, sum(sd2) / iters
    print("\n" + "=" * 78)
    print(" 1. KUN (o+l, r+ai, s+ai) YHDISTETÄÄN: ETÄISYYS 1 vs. ETÄISYYS 2")
    print("=" * 78)
    print(f"   Etäisyys 1 MI: {r1:.5f} vs {m1:.5f} (x{r1/m1:.2f}, netto {r1-m1:+.5f})")
    print(f"   Etäisyys 2 MI: {r2:.5f} vs {m2:.5f} (x{r2/m2:.2f}, netto {r2-m2:+.5f})")

    # --- 2. MIKÄ AIHEUTTAA qo-SANOJEN SISÄISEN Z=+2.34 JÄÄNTEEN? ---
    qo_g_grp = defaultdict(list)
    qo_e_grp = defaultdict(list)
    qo_g_all, qo_e_all = [], []
    for pid, is_par, ws in lines:
        n = len(ws)
        for i in range(n - 1):
            w1, w2 = ws[i], ws[i + 1]
            if w2.startswith('qo') and len(w2) > 2:
                pos = 'PF' if (i == 0 and is_par) else ('LF' if i == 0 else 'LM')
                a = tail_class(w1)
                g_ch = w2[2]  # k, t, p, f, l, e, o...
                e_end = tail_class(w2[3:]) if len(w2) > 3 else w2[2:]
                qo_g_grp[(pid, pos)].append((a, g_ch))
                qo_e_grp[(pid, pos)].append((a, e_end))
                qo_g_all.append((a, g_ch))
                qo_e_all.append((a, e_end))

    print("\n" + "=" * 78)
    print(f" 2. 'qo-' SANOJEN SISÄINEN JÄÄNNE (N={len(qo_g_all)}, kappale & riviasema lukittu)")
    print("=" * 78)
    for label, grp, all_p in [("w1 loppu -> qo:n 3. merkki (k/t/p/f/l/e)", qo_g_grp, qo_g_all),
                              ("w1 loppu -> qo-sanan loppupääte (ilman 3. merkkiä)", qo_e_grp, qo_e_all)]:
        rm = calc_mi(all_p)
        smis = []
        for _ in range(iters):
            sp = []
            for pairs in grp.values():
                xs = [a for a, _ in pairs]
                ys = [b for _, b in pairs]
                rng.shuffle(xs)
                sp.extend(zip(xs, ys))
            smis.append(calc_mi(sp))
        mu = sum(smis) / iters
        sd = math.sqrt(sum((x - mu) ** 2 for x in smis) / iters)
        z = (rm - mu) / (sd if sd > 0 else 1e-9)
        p = (sum(x >= rm for x in smis) + 1) / (iters + 1)
        print(f"   {label:<52} | MI:{rm:.5f} vs {mu:.5f} | Z={z:+5.2f} | p={p:.4f}")

    # --- 3. 6x8 LIITINMATRIISI (w1[-1] -> w2[0], suhde satunnaiseen odotusarvoon) ---
    pairs_ch = [(ws[i][-1], ws[i + 1][0]) for _, _, ws in lines for i in range(len(ws) - 1)]
    tot = len(pairs_ch)
    ca = Counter(a for a, _ in pairs_ch)
    cb = Counter(b for _, b in pairs_ch)
    cab = Counter(pairs_ch)

    ends = ['y', 'n', 'r', 'l', 's', 'o']
    starts = ['q', 'c', 'o', 'd', 's', 'a', 'k', 't']
    print("\n" + "=" * 78)
    print(" 3. LIITINMATRIISI (Havainto / Odotusarvo): >1.5x = suosii, <0.5x = hylkii")
    print("=" * 78)
    header = " LOPPU\\ALKU | " + " | ".join(f"  {s}  " for s in starts)
    print(header)
    print("-" * len(header))
    for e in ends:
        row_cells = []
        for s in starts:
            exp = (ca[e] * cb[s]) / tot if tot > 0 else 0
            ratio = cab[(e, s)] / exp if exp > 0 else 0
            row_cells.append(f"{ratio:4.2f}x")
        print(f"     -{e:<5} | " + " | ".join(row_cells))
    print("=" * 78)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Käyttö: python vfsf_connector_probe.py ZL3b-n.txt")