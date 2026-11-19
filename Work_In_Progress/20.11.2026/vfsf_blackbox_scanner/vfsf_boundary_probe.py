#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2026 Juho Olavi Laakso
# SPDX-License-Identifier: MIT
"""
VFSF Boundary & Distance Probe v1.0
Testaa:
1) Säilyykö Suffix -> Next Prefix -signaali kappaleen sisäisessä sekoituksessa?
2) Onko signaali välitön (etäisyys 1 vs. etäisyys 2)?
3) Miten ilmiö eroaa osioiden (Herbal, Biological, Recipes, Astro) välillä?
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


def parse_slots(word):
    w = word.lower()
    prefix = 'NONE'
    for p in ('qo', 'ot', 'yt', 'ok', 'yk', 'te', 'op', 'ol', 'or', 'ch', 'sh', 'da', 'so', 'sa', 'q', 'o', 'y', 'd', 's', 'p', 'f', 'k', 't'):
        if w.startswith(p) and len(w) > len(p):
            prefix = p
            break

    suffix = 'OTHER'
    for suf in ('aiin', 'aiiin', 'oiin', 'ain', 'iin', 'dy', 'ey', 'hy', 'ky', 'ty', 'ly', 'ry', 'sy', 'am', 'om', 'ol', 'or', 'ar', 'al', 'g', 'm', 'y', 'n', 'l', 'r', 'd'):
        if w.endswith(suf):
            suffix = suf
            break

    return prefix, suffix, w[-1], w[0]


def load_corpus(filepath):
    lines_data = []
    current_folio = "unknown"
    par_id = 0
    prev_par_end = True

    with open(filepath, 'r', encoding='utf-8') as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith('#'):
                continue

            locus_match = re.search(r'<f(\d+[rv]\d*)([^>]*)>', line.lower())
            is_par_start = False
            if locus_match:
                new_folio = locus_match.group(1)
                meta = locus_match.group(2)
                if new_folio != current_folio or '@p' in meta or prev_par_end:
                    is_par_start = True
                    par_id += 1
                current_folio = new_folio

            prev_par_end = ('<$>' in line)

            clean = re.sub(r'<[^>]+>|\{[^}]+\}|\[[^\]]+\]|@[0-9;]+', '', line)
            clean = clean.replace("'", "").replace("’", "")
            clean = re.sub(r'[{}\[\]!@%<>?:*#$,=+\-]', ' ', clean)
            words = [w.strip().lower() for w in re.split(r'[\s.]+', clean)
                     if w and not re.match(r'^f\d+[rv]\d*$', w.lower())]
            if words:
                lines_data.append({
                    'folio': current_folio,
                    'section': get_section(current_folio),
                    'par_id': par_id,
                    'is_par_start': is_par_start,
                    'words': words
                })
    return lines_data


def calc_mi(pairs):
    n = len(pairs)
    if n == 0:
        return 0.0
    ca = Counter(a for a, _ in pairs)
    cb = Counter(b for _, b in pairs)
    cab = Counter(pairs)
    mi = 0.0
    for (a, b), c in cab.items():
        p_ab = c / n
        mi += p_ab * math.log2(p_ab / ((ca[a] / n) * (cb[b] / n)))
    return mi


def get_pairs(lines_data, cache, dist, pair_type, section_filter=None):
    pairs = []
    for row in lines_data:
        if section_filter and row['section'] != section_filter:
            continue
        w = row['words']
        if len(w) <= dist:
            continue
        for i in range(len(w) - dist):
            p1, s1, lc1, _ = cache[w[i]]
            p2, s2, _, fc2 = cache[w[i + dist]]
            if pair_type == 'morpheme':
                pairs.append((s1, p2))
            elif pair_type == 'char':
                pairs.append((lc1, fc2))
            elif pair_type == 'prefix':
                pairs.append((p1, p2))
    return pairs


def shuffle_within_paragraph(lines_data, rng):
    buckets = defaultdict(list)
    for row in lines_data:
        pid = row['par_id']
        n = len(row['words'])
        for i, w in enumerate(row['words']):
            pos = 'SINGLE' if n == 1 else ('PAR_FIRST' if (i == 0 and row['is_par_start']) else ('LINE_FIRST' if i == 0 else ('LINE_LAST' if i == n - 1 else 'LINE_MID')))
            buckets[(pid, pos)].append(w)

    for k in buckets:
        rng.shuffle(buckets[k])

    counters = defaultdict(int)
    out = []
    for row in lines_data:
        pid = row['par_id']
        n = len(row['words'])
        nw = []
        for i in range(n):
            pos = 'SINGLE' if n == 1 else ('PAR_FIRST' if (i == 0 and row['is_par_start']) else ('LINE_FIRST' if i == 0 else ('LINE_LAST' if i == n - 1 else 'LINE_MID')))
            idx = counters[(pid, pos)]
            nw.append(buckets[(pid, pos)][idx])
            counters[(pid, pos)] += 1
        out.append({
            'folio': row['folio'],
            'section': row['section'],
            'par_id': pid,
            'is_par_start': row['is_par_start'],
            'words': nw
        })
    return out


def eval_test(lines_data, shufs, cache, dist, pair_type, section=None):
    real_mi = calc_mi(get_pairs(lines_data, cache, dist, pair_type, section))
    shuf_mis = [calc_mi(get_pairs(sc, cache, dist, pair_type, section)) for sc in shufs]
    mu = sum(shuf_mis) / len(shuf_mis)
    sd = math.sqrt(sum((x - mu) ** 2 for x in shuf_mis) / len(shuf_mis))
    z = (real_mi - mu) / (sd if sd > 0 else 1e-9)
    return real_mi, mu, z


def main(filepath, iterations=100):
    if not os.path.exists(filepath):
        print(f"Virhe: Tiedostoa '{filepath}' ei löydy.")
        return
    lines_data = load_corpus(filepath)
    cache = {w: parse_slots(w) for r in lines_data for w in r['words']}
    rng = random.Random(1337)
    shufs = [shuffle_within_paragraph(lines_data, rng) for _ in range(iterations)]

    print("\n" + "=" * 80)
    print(" 1. KAPPALEENSISÄINEN KONTROLLI: ETÄISYYS 1 vs. ETÄISYYS 2")
    print("=" * 80)
    for label, dist, ptype in [
        ("Suffix(i) -> Prefix(i+1)  [Etäisyys 1]", 1, 'morpheme'),
        ("Suffix(i) -> Prefix(i+2)  [Etäisyys 2]", 2, 'morpheme'),
        ("Vika merkki -> Eka merkki [Etäisyys 1]", 1, 'char'),
        ("Vika merkki -> Eka merkki [Etäisyys 2]", 2, 'char'),
        ("Prefix(i) -> Prefix(i+1)  [Etäisyys 1]", 1, 'prefix'),
        ("Prefix(i) -> Prefix(i+2)  [Etäisyys 2]", 2, 'prefix'),
    ]:
        r_mi, s_mi, z = eval_test(lines_data, shufs, cache, dist, ptype)
        print(f" {label:<42} | MI: {r_mi:.5f} vs {s_mi:.5f} | Z = {z:+6.2f}")

    print("\n" + "=" * 80)
    print(" 2. SUFFIX(i) -> PREFIX(i+1) OSIOITTAIN (Kappale & riviasema lukittu)")
    print("=" * 80)
    for sec in ("Herbal", "Astro/Zodiac", "Biological", "Cosmo/Rosettes", "Pharmaceutical", "Recipes"):
        r_mi, s_mi, z = eval_test(lines_data, shufs, cache, 1, 'morpheme', section=sec)
        ratio = r_mi / s_mi if s_mi > 0 else 0
        print(f" {sec:<16} | MI: {r_mi:.5f} vs {s_mi:.5f} (x{ratio:4.2f}) | Z = {z:+6.2f}")
    print("=" * 80)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Käyttö: python vfsf_boundary_probe.py ZL3b-n.txt")