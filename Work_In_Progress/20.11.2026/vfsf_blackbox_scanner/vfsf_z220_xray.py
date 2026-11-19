#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2026 Juho Olavi Laakso
# SPDX-License-Identifier: MIT
"""
VFSF Z=+220.88 X-Ray Probe
1) Näyttää vahvimmin suositellut ja vältellyt (vika merkki -> eka merkki) -parit.
2) Testaa loppukirjaimen vakioimalla, ennustavatko VFSF-päätteet (dy vs ey vs hy,
   aiin vs ain) seuraavaa sanaa vielä enemmän kuin pelkkä loppukirjain yksin.
"""
import re
import sys
import os
import math
import random
from collections import Counter, defaultdict


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
            clean = re.sub(r'<[^>]+>|\{[^}]+\}|\[[^\]]+\]|@[0-9;]+', '', line)
            clean = re.sub(r'[{}\[\]!@%<>?:*#$,=+\-\'’]', ' ', clean)
            words = [w.strip().lower() for w in re.split(r'[\s.]+', clean)
                     if w and not re.match(r'^f\d+[rv]\d*$', w.lower())]
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


def next_head(w):
    for p in ('qo', 'ch', 'sh', 'ot', 'ok', 'da'):
        if w.startswith(p) and len(w) > len(p):
            return p
    return w[0]


def main(filepath, iters=200):
    if not os.path.exists(filepath):
        print(f"Virhe: '{filepath}' ei löydy.")
        return
    lines = load_lines(filepath)
    rng = random.Random(1337)

    # 1. Vika merkki -> Eka merkki (parit ja kiellot, kappale & riviasema lukittu)
    real_pairs = []
    buckets = defaultdict(list)
    for pid, is_par, words in lines:
        n = len(words)
        for i in range(n - 1):
            real_pairs.append((words[i][-1], words[i + 1][0]))
        for i, w in enumerate(words):
            pos = 'S' if n == 1 else ('PF' if (i == 0 and is_par) else ('LF' if i == 0 else ('LL' if i == n - 1 else 'LM')))
            buckets[(pid, pos)].append(w)

    shuf_counts = defaultdict(list)
    for _ in range(iters):
        shuf_b = {k: v.copy() for k, v in buckets.items()}
        for k in shuf_b:
            rng.shuffle(shuf_b[k])
        cnt = defaultdict(int)
        sp = Counter()
        for pid, is_par, words in lines:
            n = len(words)
            nw = []
            for i in range(n):
                pos = 'S' if n == 1 else ('PF' if (i == 0 and is_par) else ('LF' if i == 0 else ('LL' if i == n - 1 else 'LM')))
                nw.append(shuf_b[(pid, pos)][cnt[(pid, pos)]])
                cnt[(pid, pos)] += 1
            for i in range(n - 1):
                sp[(nw[i][-1], nw[i + 1][0])] += 1
        for k in set(real_pairs) | set(sp):
            shuf_counts[k].append(sp[k])

    rc = Counter(real_pairs)
    ranked = []
    for k in set(rc) | set(shuf_counts):
        obs = rc[k]
        vals = shuf_counts[k]
        mu = sum(vals) / iters if vals else 0.0
        if obs < 30 and mu < 30:
            continue
        sd = math.sqrt(sum((x - mu) ** 2 for x in vals) / iters) if vals else 1.0
        z = (obs - mu) / (sd if sd > 0 else 1.0)
        ranked.append((z, obs, mu, k))
    ranked.sort(reverse=True)

    print("\n" + "=" * 78)
    print(" 1. VAHVIMMAT SUOSITUT JA VÄLTELLYT RAJAKIRJAIMET (w1[-1] -> w2[0])")
    print("=" * 78)
    print(" TOP 10 SUOSITTUA PARIA (esiintyy odotettua useammin):")
    for z, obs, mu, (a, b) in ranked[:10]:
        print(f"   '{a}' -> '{b}'  | Osuma: {obs:4d} (Sekoitus ka: {mu:6.1f}) | Z = {z:+6.2f}")
    print("\n TOP 10 VÄLTELLYINTÄ PARIA (esiintyy odotettua harvemmin):")
    for z, obs, mu, (a, b) in ranked[-10:][::-1]:
        print(f"   '{a}' -> '{b}'  | Osuma: {obs:4d} (Sekoitus ka: {mu:6.1f}) | Z = {z:+6.2f}")

    # 2. Testi vakioidun loppukirjaimen sisällä: -y (dy vs ey vs hy...) ja -n (aiin vs ain...)
    y_pairs = []
    n_pairs = []
    for _, _, words in lines:
        for i in range(len(words) - 1):
            w1, w2 = words[i], words[i + 1]
            nh = next_head(w2)
            if w1.endswith('y') and len(w1) >= 2:
                y_pairs.append((w1[-2:], nh))
            elif w1.endswith('n'):
                n_tag = 'aiin' if w1.endswith('aiin') else ('ain' if w1.endswith('ain') else ('iin' if w1.endswith('iin') else 'other_n'))
                n_pairs.append((n_tag, nh))

    print("\n" + "=" * 78)
    print(" 2. LOPPUKIRJAIMEN SISÄINEN MORFEEMITESTI (Loppukirjain vakioitu)")
    print("=" * 78)
    for label, pairs in [("Kaikki -y sanat (dy/ey/hy/ky... -> seur. alku)", y_pairs),
                         ("Kaikki -n sanat (aiin/ain/iin -> seur. alku)", n_pairs)]:
        real_mi = calc_mi(pairs)
        xs = [a for a, _ in pairs]
        ys = [b for _, b in pairs]
        smis = []
        for _ in range(iters):
            xs_s = xs.copy()
            rng.shuffle(xs_s)
            smis.append(calc_mi(list(zip(xs_s, ys))))
        mu = sum(smis) / iters
        sd = math.sqrt(sum((x - mu) ** 2 for x in smis) / iters)
        z = (real_mi - mu) / (sd if sd > 0 else 1e-9)
        p = (sum(x >= real_mi for x in smis) + 1) / (iters + 1)
        print(f" {label:<50} | N={len(pairs):5d} | MI: {real_mi:.5f} vs {mu:.5f} | Z={z:+5.2f} | p={p:.4f}")
    print("=" * 78)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Käyttö: python vfsf_z220_xray.py ZL3b-n.txt")