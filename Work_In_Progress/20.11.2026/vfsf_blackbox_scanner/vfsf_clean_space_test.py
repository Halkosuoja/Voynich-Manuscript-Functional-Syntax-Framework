#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2026 Juho Olavi Laakso
# SPDX-License-Identifier: MIT
"""
VFSF Clean-Space & Strict Position Test
1) Vertaa ',' (epävarma väli) vs '.' (selvä väli) osuutta rajapareissa.
2) Yhdistää ','-välit ja mittaa w1[-1] -> w2[0] uudelleen selvillä sanaväleillä.
3) Testaa -y päätteiden sisäisen eron (dy/ey/hy/ky) lukitsemalla SEKÄ kappaleen ETTÄ riviaseman.
"""
import re
import sys
import os
import math
import random
from collections import Counter, defaultdict


def next_head(w):
    for p in ('qo', 'ch', 'sh', 'ot', 'ok', 'da'):
        if w.startswith(p) and len(w) > len(p):
            return p
    return w[0]


def calc_mi(pairs):
    n = len(pairs)
    if n == 0:
        return 0.0
    ca = Counter(a for a, _ in pairs)
    cb = Counter(b for _, b in pairs)
    cab = Counter(pairs)
    return sum((c / n) * math.log2((c / n) / ((ca[a] / n) * (cb[b] / n)))
               for (a, b), c in cab.items())


def main(filepath, iters=200):
    if not os.path.exists(filepath):
        print(f"Virhe: '{filepath}' ei löydy.")
        return

    comma_counts = Counter()
    dot_counts = Counter()
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
            no_tags = no_tags.replace('!', '').replace("'", "").replace("’", "")

            for a, b in re.findall(r'([a-z]),([a-z])', no_tags):
                comma_counts[(a, b)] += 1
            for a, b in re.findall(r'([a-z])\.([a-z])', no_tags):
                dot_counts[(a, b)] += 1

            # Yhdistetään ',' ja jaetaan vain selvistä '.'- ja tyhjäväleistä
            joined = no_tags.replace(',', '')
            joined = re.sub(r'[^a-z.\s]', ' ', joined)
            words = [w.strip() for w in re.split(r'[\s.]+', joined)
                     if w.strip() and not re.match(r'^f\d+[rv]\d*$', w.strip())]
            if words:
                lines.append((par_id, is_par, words))

    print("\n" + "=" * 78)
    print(" 1. EPÄVARMAT VÄLIT (,) vs. SELVÄT VÄLIT (.) RAJAKIRJAIMISSA")
    print("=" * 78)
    for pair in (('y', 'q'), ('r', 'a'), ('s', 'a'), ('o', 'l'), ('o', 'r'), ('n', 'c')):
        cc, dc = comma_counts[pair], dot_counts[pair]
        tot = cc + dc
        pct = (cc * 100 / tot) if tot else 0.0
        print(f"   '{pair[0]}' -> '{pair[1]}' | Selvä '.' : {dc:4d} | Pilkku ',' : {cc:4d} ({pct:4.1f}% pilkkuja)")

    # 2. Rajakirjaimet uudelleen kun ',' on yhdistetty
    rng = random.Random(1337)
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
        ranked.append(((obs - mu) / (sd if sd > 0 else 1.0), obs, mu, k))
    ranked.sort(reverse=True)

    print("\n" + "=" * 78)
    print(" 2. RAJAKIRJAIMET YHDISTETTYJEN PILKKUJEN JÄLKEEN (Vain selvät välit)")
    print("=" * 78)
    print(" TOP 8 SUOSITTUA:")
    for z, obs, mu, (a, b) in ranked[:8]:
        print(f"   '{a}' -> '{b}' | Osuma: {obs:4d} (Sekoitus ka: {mu:6.1f}) | Z = {z:+6.2f}")
    print(" TOP 6 VÄLTELLYINTÄ:")
    for z, obs, mu, (a, b) in ranked[-6:][::-1]:
        print(f"   '{a}' -> '{b}' | Osuma: {obs:4d} (Sekoitus ka: {mu:6.1f}) | Z = {z:+6.2f}")

    # 3. Tiukin -y testi: pilkut yhdistetty + kappale JA riviasema lukittu
    y_by_group = defaultdict(list)
    y_all_pairs = []
    for pid, is_par, words in lines:
        n = len(words)
        for i in range(n - 1):
            w1, w2 = words[i], words[i + 1]
            if w1.endswith('y') and len(w1) >= 2:
                pos = 'PF' if (i == 0 and is_par) else ('LF' if i == 0 else 'LM')
                a, b = w1[-2:], next_head(w2)
                y_by_group[(pid, pos)].append((a, b))
                y_all_pairs.append((a, b))

    real_y_mi = calc_mi(y_all_pairs)
    smis = []
    for _ in range(iters):
        sp = []
        for g_pairs in y_by_group.values():
            xs = [a for a, _ in g_pairs]
            ys = [b for _, b in g_pairs]
            rng.shuffle(xs)
            sp.extend(zip(xs, ys))
        smis.append(calc_mi(sp))
    mu_y = sum(smis) / iters
    sd_y = math.sqrt(sum((x - mu_y) ** 2 for x in smis) / iters)
    z_y = (real_y_mi - mu_y) / (sd_y if sd_y > 0 else 1e-9)
    p_y = (sum(x >= real_y_mi for x in smis) + 1) / (iters + 1)

    print("\n" + "=" * 78)
    print(" 3. TIUKIN -y MORFEEMITESTI (Pilkut yhdistetty + Kappale & Riviasema lukittu)")
    print("=" * 78)
    print(f" N={len(y_all_pairs)} | MI: {real_y_mi:.5f} vs {mu_y:.5f} | Z = {z_y:+6.2f} | p = {p_y:.4f}")
    print("=" * 78)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Käyttö: python vfsf_clean_space_test.py ZL3b-n.txt")