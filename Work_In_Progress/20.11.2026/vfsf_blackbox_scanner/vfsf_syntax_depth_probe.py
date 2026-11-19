#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2026 Juho Olavi Laakso
# SPDX-License-Identifier: MIT
"""
VFSF Syntax Depth Probe (Productive Grammar vs. Frozen Phrases + Section Breakdown)
1) Näyttää ketjun tarkat yksittäiset sanaparit (esim. CH_DY -> QO_DY).
2) Testaa suuntaepäsymmetrian harvinaisilla/ei-yleisillä sanoilla (kielioppi vs. vakiofraasit).
3) Vertaa suunnattuja ketjuja erikseen Herbal-, Biological-, Recipes- ja Astro-osioissa.
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


def word_class(w):
    if w.startswith('qo') and w.endswith('dy'):
        return 'QO_DY'
    if w.startswith('qo') and w.endswith('ey'):
        return 'QO_EY'
    if w.startswith('qo'):
        return 'QO_OTH'
    if w.startswith(('ch', 'sh')) and w.endswith('dy'):
        return 'CH_DY'
    if w.startswith(('ch', 'sh')) and w.endswith('ey'):
        return 'CH_EY'
    if w.startswith(('ch', 'sh')) and w.endswith(('ol', 'or', 'al', 'ar')):
        return 'CH_OLR'
    if w.startswith(('ch', 'sh')):
        return 'CH_OTH'
    if w.startswith('da') and w.endswith(('aiin', 'ain', 'iin')):
        return 'DA_IIN'
    if w.startswith('da'):
        return 'DA_OTH'
    if w.startswith(('ot', 'ok')) and w.endswith('y'):
        return 'OTK_Y'
    if w.startswith(('ot', 'ok')):
        return 'OTK_OTH'
    if w.endswith(('cthy', 'ckhy', 'cphy', 'cfhy', 'hy')):
        return 'GAL_HY'
    if w.endswith(('ol', 'or', 'al', 'ar')):
        return 'BARE_OLR'
    if w.endswith('y'):
        return 'END_Y'
    if w.endswith('n'):
        return 'END_N'
    return 'OTHER'


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
                lines.append((get_section(cur_fol), par_id, is_par, words))
    return lines


def asym_stat(pair_counts, min_sum=10):
    keys = sorted({a for a, _ in pair_counts} | {b for _, b in pair_counts})
    total = 0.0
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            cab = pair_counts[(a, b)]
            cba = pair_counts[(b, a)]
            if cab + cba >= min_sum:
                total += ((cab - cba) ** 2) / (cab + cba)
    return total


def eval_asym_subset(real_lines, shuf_corpora, cls_cache, freq, filter_fn, sec_filter=None, min_sum=10):
    def count_pairs(lines_src):
        c = Counter()
        for sec, _, _, words in lines_src:
            if sec_filter and sec != sec_filter:
                continue
            for i in range(len(words) - 1):
                w1, w2 = words[i], words[i + 1]
                if filter_fn(w1, w2, freq):
                    c[(cls_cache[w1], cls_cache[w2])] += 1
        return c

    real_c = count_pairs(real_lines)
    real_t = asym_stat(real_c, min_sum=min_sum)
    shuf_ts = []
    shuf_c_list = []
    for sc in shuf_corpora:
        c = count_pairs(sc)
        shuf_c_list.append(c)
        shuf_ts.append(asym_stat(c, min_sum=min_sum))

    n_it = len(shuf_ts)
    mu = sum(shuf_ts) / n_it
    sd = math.sqrt(sum((x - mu) ** 2 for x in shuf_ts) / n_it)
    z = (real_t - mu) / (sd if sd > 0 else 1e-9)
    p = (sum(x >= real_t for x in shuf_ts) + 1) / (n_it + 1)
    return real_c, shuf_c_list, real_t, mu, z, p


def main(filepath, iters=150):
    if not os.path.exists(filepath):
        print(f"Virhe: '{filepath}' ei löydy.")
        return

    lines = load_clean_lines(filepath)
    freq = Counter(w for _, _, _, words in lines for w in words)
    cls_cache = {w: word_class(w) for w in freq}

    # --- OSA 1: TODELlISET SANAPARIT KETJUN TAKANA ---
    chain_targets = [
        ('BARE_OLR', 'CH_DY'),
        ('CH_DY', 'QO_DY'),
        ('QO_DY', 'QO_OTH'),
        ('QO_OTH', 'BARE_OLR'),
    ]
    exact_pairs = defaultdict(Counter)
    for _, _, _, words in lines:
        for i in range(len(words) - 1):
            w1, w2 = words[i], words[i + 1]
            c1, c2 = cls_cache[w1], cls_cache[w2]
            if (c1, c2) in chain_targets:
                exact_pairs[(c1, c2)][f"{w1} -> {w2}"] += 1

    print("\n" + "=" * 82)
    print(" 1. MITKÄ TARKAT SANAPARIT MUODOSTAVAT SUUNNATUN KETJUN? (Top 5 / siirtymä)")
    print("=" * 82)
    for pair in chain_targets:
        tot = sum(exact_pairs[pair].values())
        uniq = len(exact_pairs[pair])
        top5 = ", ".join(f"{k} ({v})" for k, v in exact_pairs[pair].most_common(5))
        print(f" [{pair[0]} -> {pair[1]}] Yht: {tot} kpl, {uniq} eri sanaparia")
        print(f"   Top 5: {top5}")

    # Rakennetaan kappale- ja riviasemalukitut sekoitukset
    rng = random.Random(1337)
    buckets = defaultdict(list)
    for sec, pid, is_par, words in lines:
        n = len(words)
        for i, w in enumerate(words):
            pos = 'S' if n == 1 else ('PF' if (i == 0 and is_par) else ('LF' if i == 0 else ('LL' if i == n - 1 else 'LM')))
            buckets[(pid, pos)].append(w)

    shuf_corpora = []
    for _ in range(iters):
        sb = {k: v.copy() for k, v in buckets.items()}
        for k in sb:
            rng.shuffle(sb[k])
        cnt = defaultdict(int)
        sc = []
        for sec, pid, is_par, words in lines:
            n = len(words)
            nw = []
            for i in range(n):
                pos = 'S' if n == 1 else ('PF' if (i == 0 and is_par) else ('LF' if i == 0 else ('LL' if i == n - 1 else 'LM')))
                nw.append(sb[(pid, pos)][cnt[(pid, pos)]])
                cnt[(pid, pos)] += 1
            sc.append((sec, pid, is_par, nw))
        shuf_corpora.append(sc)

    # --- OSA 2: PRODUKTIIVINEN KIELIOPPI VS. VAKIOFRAASIT ---
    print("\n" + "=" * 82)
    print(" 2. VAKIOFRAASIT vs. HARVINAISET SANAT (Kappale & riviasema lukittu)")
    print("=" * 82)
    filters = [
        ("Kaikki sanat", lambda w1, w2, f: True),
        ("Ainakin toinen harvinainen (freq<=20)", lambda w1, w2, f: min(f[w1], f[w2]) <= 20),
        ("Kumpikaan ei yleissana (molemmat<=50)", lambda w1, w2, f: max(f[w1], f[w2]) <= 50),
    ]
    for label, fn in filters:
        rc, _, rt, mu, z, p = eval_asym_subset(lines, shuf_corpora, cls_cache, freq, fn, min_sum=8)
        n_pairs = sum(rc.values())
        print(f" {label:<42} | Parit={n_pairs:5d} | Asym: {rt:6.1f} vs {mu:5.1f} | Z={z:+6.2f} | p={p:.4f}")

    # --- OSA 3: OSIOITTAINEN SUUNTASYMMETRIA ---
    print("\n" + "=" * 82)
    print(" 3. SUUNTASYKLI OSIOITTAIN (Herbal vs. Biological vs. Recipes vs. Astro)")
    print("=" * 82)
    for sec in ("Herbal", "Biological", "Recipes", "Astro/Zodiac"):
        rc, sc_list, rt, mu, z, p = eval_asym_subset(
            lines, shuf_corpora, cls_cache, freq, lambda w1, w2, f: True, sec_filter=sec, min_sum=8
        )
        print(f"\n [{sec}] Asym: {rt:6.1f} vs {mu:5.1f} | Z = {z:+6.2f} | p = {p:.4f}")
        keys = sorted({a for a, _ in rc} | {b for _, b in rc})
        top_dir = []
        for i, a in enumerate(keys):
            for b in keys[i + 1:]:
                cab, cba = rc[(a, b)], rc[(b, a)]
                if cab + cba < 20:
                    continue
                diffs = [c[(a, b)] - c[(b, a)] for c in sc_list]
                mu_d = sum(diffs) / iters
                sd_d = math.sqrt(sum((x - mu_d) ** 2 for x in diffs) / iters)
                zd = ((cab - cba) - mu_d) / (sd_d if sd_d > 0 else 1.0)
                top_dir.append((abs(zd), zd, a, b, cab, cba))
        top_dir.sort(reverse=True)
        for _, zd, a, b, cab, cba in top_dir[:5]:
            arrow = f"{a} -> {b}" if zd > 0 else f"{b} -> {a}"
            f_c, r_c = (cab, cba) if zd > 0 else (cba, cab)
            print(f"   {arrow:<22} | {f_c:4d} vs {r_c:4d} | Z = {abs(zd):5.2f}")
    print("=" * 82)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Käyttö: python vfsf_syntax_depth_probe.py ZL3b-n.txt")