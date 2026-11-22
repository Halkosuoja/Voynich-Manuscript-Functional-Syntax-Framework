#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VFSF Gallows (k, t, p, f) & Section Connector Matrix Probe
1) Täysi 6x10 liitinmatriisi mukaan lukien kaikki neljä gallowsia (k, t, p, f).
2) Vertaa samoja pääliitinsuhteita Herbal- vs. Biological+Recipes -osioissa.
3) Näyttää tarkat sanaparien osat, jotka aiheuttavat qo-sanojen sisäisen Z=+2.66 jäänteen.
"""
import re
import sys
import os
import math
import random
from collections import Counter, defaultdict


def get_section(folio_str):
    m = re.match(r'^(\d+)([rv])', folio_str.lower())
    if not m:
        return "Other"
    num = int(m.group(1))
    if (1 <= num <= 56) or (65 <= num <= 66) or num in (87, 90) or (93 <= num <= 96):
        return "Herbal"
    if (75 <= num <= 84) or (103 <= num <= 116):
        return "Bio+Recipes"
    return "Other"


def tail_class(w):
    for s in ('aiin', 'ain', 'iin', 'dy', 'ey', 'hy', 'ky', 'ty', 'ly', 'ol', 'or', 'al', 'ar'):
        if w.endswith(s):
            return s
    return w[-1] if w else 'NONE'


def load_lines(filepath):
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
                lines.append((get_section(cur_fol), par_id, is_par, words))
    return lines


def print_matrix(title, pairs, ends, starts):
    tot = len(pairs)
    ca = Counter(a for a, _ in pairs)
    cb = Counter(b for _, b in pairs)
    cab = Counter(pairs)
    print(f"\n [{title}] (N={tot:,})")
    hdr = " LOPPU\\ALKU | " + " | ".join(f"  {s}  " for s in starts)
    print(hdr)
    print("-" * len(hdr))
    for e in ends:
        cells = []
        for s in starts:
            exp = (ca[e] * cb[s]) / tot if tot > 0 else 0
            ratio = cab[(e, s)] / exp if exp > 0 else 0
            cells.append(f"{ratio:4.2f}x")
        print(f"     -{e:<5} | " + " | ".join(cells))


def main(filepath, iters=200):
    if not os.path.exists(filepath):
        print(f"Virhe: '{filepath}' ei löydy.")
        return

    lines = load_lines(filepath)
    all_pairs = [(ws[i][-1], ws[i + 1][0]) for _, _, _, ws in lines for i in range(len(ws) - 1)]
    sec_pairs = defaultdict(list)
    for sec, _, _, ws in lines:
        for i in range(len(ws) - 1):
            sec_pairs[sec].append((ws[i][-1], ws[i + 1][0]))

    ends = ['y', 'n', 'r', 'l', 's', 'o']
    starts_all = ['q', 'k', 't', 'p', 'f', 'c', 'o', 'd', 's', 'a']

    print("\n" + "=" * 86)
    print(" 1. TÄYSI LIITINMATRIISI (Mukaan lukien kaikki 4 gallowsia: k, t, p, f)")
    print("=" * 86)
    print_matrix("KOKO KORPUS", all_pairs, ends, starts_all)

    print("\n" + "=" * 86)
    print(" 2. VERTAILU: HERBAL (Currier A) vs. BIO + RECIPES (Currier B)")
    print("=" * 86)
    starts_cmp = ['q', 'k', 't', 'p', 'c', 'o', 'a']
    print_matrix("HERBAL", sec_pairs["Herbal"], ends, starts_cmp)
    print_matrix("BIO + RECIPES", sec_pairs["Bio+Recipes"], ends, starts_cmp)

    # 3. Mikä aiheuttaa qo-sanojen sisäisen Z=+2.66 jäänteen?
    rng = random.Random(1337)
    qo_grp = defaultdict(list)
    qo_real = Counter()
    for _, pid, is_par, ws in lines:
        n = len(ws)
        for i in range(n - 1):
            w1, w2 = ws[i], ws[i + 1]
            if w2.startswith('qo') and len(w2) > 2:
                pos = 'PF' if (i == 0 and is_par) else ('LF' if i == 0 else 'LM')
                a = tail_class(w1)
                b = f"{w2[2]}+{tail_class(w2[3:]) if len(w2) > 3 else ''}"
                qo_grp[(pid, pos)].append((a, b))
                qo_real[(a, b)] += 1

    shuf_c = defaultdict(list)
    for _ in range(iters):
        sc = Counter()
        for pairs in qo_grp.values():
            xs = [a for a, _ in pairs]
            ys = [b for _, b in pairs]
            rng.shuffle(xs)
            for p in zip(xs, ys):
                sc[p] += 1
        for k in set(qo_real) | set(sc):
            shuf_c[k].append(sc[k])

    ranked = []
    for k, obs in qo_real.items():
        vals = shuf_c[k]
        mu = sum(vals) / iters if vals else 0.0
        if obs < 15 and mu < 15:
            continue
        sd = math.sqrt(sum((x - mu) ** 2 for x in vals) / iters) if vals else 1.0
        z = (obs - mu) / (sd if sd > 0 else 1.0)
        ranked.append((z, obs, mu, k))
    ranked.sort(reverse=True)

    print("\n" + "=" * 86)
    print(" 3. 'qo-' SANOJEN SISÄINEN JÄÄNNE (w1 loppu -> qo:[3.merkki+loppu])")
    print("=" * 86)
    print(" Vahvimmat yliodotukselliset parit:")
    for z, obs, mu, (a, b) in ranked[:8]:
        print(f"   -{a:<5} -> qo{b:<8} | Osuma: {obs:3d} (Sekoitus ka: {mu:5.1f}) | Z = {z:+5.2f}")
    print(" Vahvimmat aliedustetut parit:")
    for z, obs, mu, (a, b) in ranked[-4:][::-1]:
        print(f"   -{a:<5} -> qo{b:<8} | Osuma: {obs:3d} (Sekoitus ka: {mu:5.1f}) | Z = {z:+5.2f}")
    print("=" * 86)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Käyttö: python vfsf_gallows_and_sections_matrix.py ZL3b-n.txt")