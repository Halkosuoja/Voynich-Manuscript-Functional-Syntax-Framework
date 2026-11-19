#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2026 Juho Olavi Laakso
# SPDX-License-Identifier: MIT
"""
VFSF Morpheme & Boundary Verification
1) Testaa -y ja -n sisäiset erot OSIOITTAIN ja KAPPALEEN SISÄLLÄ (poistaa A/B-sekoitusharhan).
2) Tulostaa todelliset todennäköisyysjakaumat (dy vs ey vs hy, aiin vs ain) + esimerkkejä.
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
    if num == 57 or (67 <= num <= 73):
        return "Astro/Zodiac"
    if 75 <= num <= 84:
        return "Biological"
    if 85 <= num <= 86:
        return "Cosmo/Rosettes"
    if (88 <= num <= 89) or (99 <= num <= 102):
        return "Pharmaceutical"
    if 103 <= num <= 116:
        return "Recipes"
    return "Other"


def next_head(w):
    for p in ('qo', 'ch', 'sh', 'ot', 'ok', 'da'):
        if w.startswith(p) and len(w) > len(p):
            return p
    return w[0]


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
            if m:
                nf, meta = m.group(1), m.group(2)
                if nf != cur_fol or '@p' in meta or prev_end:
                    par_id += 1
                cur_fol = nf
            prev_end = ('<$>' in line)
            clean = re.sub(r'<[^>]+>|\{[^}]+\}|\[[^\]]+\]|@[0-9;]+', '', line)
            clean = re.sub(r'[{}\[\]!@%<>?:*#$,=+\-\'’]', ' ', clean)
            words = [w.strip().lower() for w in re.split(r'[\s.]+', clean)
                     if w and not re.match(r'^f\d+[rv]\d*$', w.lower())]
            if words:
                lines.append((get_section(cur_fol), par_id, words))
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


def within_par_test(items, iters=200):
    """ items = [(par_id, label_a, label_b), ...] """
    real_mi = calc_mi([(a, b) for _, a, b in items])
    by_par = defaultdict(list)
    for pid, a, b in items:
        by_par[pid].append((a, b))

    rng = random.Random(1337)
    smis = []
    for _ in range(iters):
        shuf_pairs = []
        for pid, pairs in by_par.items():
            xs = [a for a, _ in pairs]
            ys = [b for _, b in pairs]
            rng.shuffle(xs)
            shuf_pairs.extend(zip(xs, ys))
        smis.append(calc_mi(shuf_pairs))
    mu = sum(smis) / iters
    sd = math.sqrt(sum((x - mu) ** 2 for x in smis) / iters)
    z = (real_mi - mu) / (sd if sd > 0 else 1e-9)
    p = (sum(x >= real_mi for x in smis) + 1) / (iters + 1)
    return real_mi, mu, z, p


def main(filepath):
    if not os.path.exists(filepath):
        print(f"Virhe: '{filepath}' ei löydy.")
        return
    lines = load_lines(filepath)

    y_by_sec = defaultdict(list)
    n_by_sec = defaultdict(list)
    y_all, n_all = [], []
    examples = defaultdict(list)

    for sec, pid, words in lines:
        for i in range(len(words) - 1):
            w1, w2 = words[i], words[i + 1]
            nh = next_head(w2)
            pair_ch = (w1[-1], w2[0])
            if pair_ch in (('r', 'a'), ('s', 'a'), ('o', 'l'), ('y', 'q')) and len(examples[pair_ch]) < 8:
                examples[pair_ch].append(f"{w1}.{w2}")

            if w1.endswith('y') and len(w1) >= 2:
                tag = w1[-2:]
                y_by_sec[sec].append((pid, tag, nh))
                y_all.append((pid, tag, nh))
            elif w1.endswith('n'):
                tag = 'aiin' if w1.endswith('aiin') else ('ain' if w1.endswith('ain') else ('iin' if w1.endswith('iin') else 'other_n'))
                n_by_sec[sec].append((pid, tag, nh))
                n_all.append((pid, tag, nh))

    print("\n" + "=" * 82)
    print(" 1. KAPPALEENSISÄINEN MORFEEMITESTI (A/B-sekoitus ja loppukirjain eliminoitu)")
    print("=" * 82)
    for title, data in [("KAIKKI -y (kappaleen sisällä)", y_all),
                        ("KAIKKI -n (kappaleen sisällä)", n_all)]:
        r, m, z, p = within_par_test(data)
        print(f" {title:<32} | N={len(data):5d} | MI: {r:.5f} vs {m:.5f} | Z={z:+6.2f} | p={p:.4f}")

    print("\n Sama -y testi osioittain (kappaleen sisällä):")
    for sec in ("Herbal", "Biological", "Recipes", "Astro/Zodiac", "Pharmaceutical"):
        if len(y_by_sec[sec]) >= 100:
            r, m, z, p = within_par_test(y_by_sec[sec])
            print(f"   {sec:<16} | N={len(y_by_sec[sec]):5d} | MI: {r:.5f} vs {m:.5f} | Z={z:+6.2f} | p={p:.4f}")

    print("\n" + "=" * 82)
    print(" 2. MITÄ SEURAA ERI -y JA -n PÄÄTTEISTÄ? (Top seuraavat alut %)")
    print("=" * 82)
    for group_name, pairs, keys in [
        ("-y päätteet", [(a, b) for _, a, b in y_all], ['dy', 'ey', 'hy', 'ky', 'ty', 'ly', 'ry', 'sy']),
        ("-n päätteet", [(a, b) for _, a, b in n_all], ['aiin', 'ain', 'iin'])
    ]:
        print(f" [{group_name}]")
        for k in keys:
            sub = [b for a, b in pairs if a == k]
            if len(sub) < 50:
                continue
            top4 = ", ".join(f"{h}:{c*100/len(sub):.1f}%" for h, c in Counter(sub).most_common(5))
            print(f"   -{k:<5} (N={len(sub):4d}) -> {top4}")

    print("\n" + "=" * 82)
    print(" 3. ESIMERKKEJÄ TEKSTISTÄ VAHVIMMISTA RAJAKYTKENNÖISTÄ")
    print("=" * 82)
    for k in (('y', 'q'), ('r', 'a'), ('s', 'a'), ('o', 'l')):
        print(f"   {k[0]} -> {k[1]}: {', '.join(examples[k])}")
    print("=" * 82)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Käyttö: python vfsf_morpheme_check.py ZL3b-n.txt")