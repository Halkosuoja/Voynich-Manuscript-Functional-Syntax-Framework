#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2026 Juho Olavi Laakso
# SPDX-License-Identifier: MIT
"""
VFSF Coupling Origin Probe
Selvittää poikkeuksellisen rajakytkennän (x11.35, 95% pudotus) alkuperän:
1) Esiintyvätkö y+qo, y+lk, r+ai myös yhteen kirjoitettuina vai vain sanarajalla?
2) Kun seuraavan sanan alku (qo-, ch-, sh-, ok-, ot-) vakioidaan, ennustaako
   edellinen sana SILTI seuraavan sanan ydintä/loppua? (Kappale & riviasema lukittu)
3) Mitä Etäisyys 1 vs 2 -arvoille tapahtuu, jos y+qo -parit yhdistetään yhdeksi sanaksi?
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
    all_words = [w for _, _, ws in lines for w in ws]

    # --- TESTI 1: YLI SANARAJAN vs. YHTEEN KIRJOITETTUNA ---
    across = Counter()
    inside = Counter()
    patterns = [('y', 'qo'), ('y', 'lk'), ('r', 'ai'), ('s', 'ai'), ('n', 'ch'), ('o', 'l')]
    for w in all_words:
        for a, b in patterns:
            if (a + b) in w:
                inside[(a, b)] += 1
    for _, _, ws in lines:
        for i in range(len(ws) - 1):
            for a, b in patterns:
                if ws[i].endswith(a) and ws[i + 1].startswith(b):
                    across[(a, b)] += 1

    print("\n" + "=" * 78)
    print(" 1. SANARAJAN YLI (w1 + väli + w2) vs. YHTEEN KIRJOITETTUNA (sanan sisällä)")
    print("=" * 78)
    for a, b in patterns:
        ac, ins = across[(a, b)], inside[(a, b)]
        pct_ac = ac * 100 / (ac + ins) if (ac + ins) > 0 else 0
        print(f"   '{a}' + '{b}' | Välillä: {ac:4d} | Yhteen: {ins:4d} | Välillisiä: {pct_ac:5.1f}%")

    # --- TESTI 2: ENNUSTAAKO w1 SEURAAVAN SANAN LOPPUA KUN ALKU ON VAKIOITU? ---
    rng = random.Random(1337)
    print("\n" + "=" * 78)
    print(" 2. KUN SEURAAVAN SANAN ALKU VAKIOIDAAN, ENNUSTAAKO w1 SEN LOPPUA?")
    print("    (Kappale & riviasema lukittu, N=200 sekoitusta)")
    print("=" * 78)
    for pre in ('qo', 'ch', 'sh', 'ok', 'ot'):
        grouped = defaultdict(list)
        all_p = []
        for pid, is_par, ws in lines:
            n = len(ws)
            for i in range(n - 1):
                w1, w2 = ws[i], ws[i + 1]
                if w2.startswith(pre) and len(w2) > len(pre):
                    pos = 'PF' if (i == 0 and is_par) else ('LF' if i == 0 else 'LM')
                    a = tail_class(w1)
                    b = tail_class(w2[len(pre):]) if len(w2[len(pre):]) >= 2 else w2[len(pre):]
                    grouped[(pid, pos)].append((a, b))
                    all_p.append((a, b))
        real_mi = calc_mi(all_p)
        smis = []
        for _ in range(iters):
            sp = []
            for pairs in grouped.values():
                xs = [a for a, _ in pairs]
                ys = [b for _, b in pairs]
                rng.shuffle(xs)
                sp.extend(zip(xs, ys))
            smis.append(calc_mi(sp))
        mu = sum(smis) / iters
        sd = math.sqrt(sum((x - mu) ** 2 for x in smis) / iters)
        z = (real_mi - mu) / (sd if sd > 0 else 1e-9)
        p = (sum(x >= real_mi for x in smis) + 1) / (iters + 1)
        print(f"   Alku '{pre}-' (N={len(all_p):4d}) -> loppu | MI: {real_mi:.5f} vs {mu:.5f} | Z={z:+5.2f} | p={p:.4f}")

    # --- TESTI 3: MITÄ TAPAHTUU JOS (-y + qo-) YHDISTETÄÄN YHDEKSI SANAKSI? ---
    merged_lines = []
    for pid, is_par, ws in lines:
        mws = []
        i = 0
        while i < len(ws):
            if i + 1 < len(ws) and ws[i].endswith('y') and ws[i + 1].startswith('qo'):
                mws.append(ws[i] + ws[i + 1])
                i += 2
            else:
                mws.append(ws[i])
                i += 1
        if mws:
            merged_lines.append((pid, is_par, mws))

    buckets = defaultdict(list)
    for pid, is_par, ws in merged_lines:
        n = len(ws)
        for i, w in enumerate(ws):
            pos = 'S' if n == 1 else ('PF' if (i == 0 and is_par) else ('LF' if i == 0 else ('LL' if i == n - 1 else 'LM')))
            buckets[(pid, pos)].append(w)

    def char_mi_lines(src, dist):
        return calc_mi([(ws[i][-1], ws[i + dist][0]) for _, _, ws in src if len(ws) > dist for i in range(len(ws) - dist)])

    shuf_d1, shuf_d2 = [], []
    for _ in range(iters):
        sb = {k: v.copy() for k, v in buckets.items()}
        for k in sb:
            rng.shuffle(sb[k])
        cnt = defaultdict(int)
        sl = []
        for pid, is_par, ws in merged_lines:
            n = len(ws)
            nw = []
            for i in range(n):
                pos = 'S' if n == 1 else ('PF' if (i == 0 and is_par) else ('LF' if i == 0 else ('LL' if i == n - 1 else 'LM')))
                nw.append(sb[(pid, pos)][cnt[(pid, pos)]])
                cnt[(pid, pos)] += 1
            sl.append((pid, is_par, nw))
        shuf_d1.append(char_mi_lines(sl, 1))
        shuf_d2.append(char_mi_lines(sl, 2))

    r1 = char_mi_lines(merged_lines, 1)
    r2 = char_mi_lines(merged_lines, 2)
    m1, m2 = sum(shuf_d1) / iters, sum(shuf_d2) / iters
    print("\n" + "=" * 78)
    print(" 3. KOKEELLINEN UUDELLEENJAKO: Jos (-y + qo-) liitetään yhteen sanaksi")
    print("=" * 78)
    print(f"   Uusi sanamäärä: {sum(len(ws) for _,_,ws in merged_lines):,} (oli {len(all_words):,})")
    print(f"   Etäisyys 1 MI: {r1:.5f} vs {m1:.5f} (x{r1/m1:.2f}, netto {r1-m1:+.5f})")
    print(f"   Etäisyys 2 MI: {r2:.5f} vs {m2:.5f} (x{r2/m2:.2f}, netto {r2-m2:+.5f})")
    print("=" * 78)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Käyttö: python vfsf_coupling_origin_probe.py ZL3b-n.txt")