#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2026 Juho Olavi Laakso
# SPDX-License-Identifier: MIT
"""
Universal Syntax Benchmark (Kieliriippumaton vertailija)
Mittaa minkä tahansa tekstin (Voynich, suomi, saksa, latina...) samoilla kriteereillä:
1) Vika merkki -> Eka merkki (Etäisyys 1 vs Etäisyys 2, kappale & riviasema lukittu).
2) Tekstin omista top-päätteistä/aluista muodostettujen luokkien suuntaepäsymmetria (Z).
3) Mikä 2-merkin alku riippuu vahvimmin edellisen sanan loppumerkistä.
"""
import re
import sys
import os
import math
import random
from collections import Counter, defaultdict


def load_universal_lines(filepath):
    lines = []
    par_id = 0
    cur_fol = None
    prev_end = True

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            raw_text = f.read()
    except UnicodeDecodeError:
        with open(filepath, 'r', encoding='cp1252', errors='replace') as f:
            raw_text = f.read()

    is_ivtff = ('<$>' in raw_text or len(re.findall(r'<f\d+[rv]', raw_text.lower())) >= 3)

    for raw in raw_text.splitlines():
        line = raw.strip()
        if not line:
            if not is_ivtff:
                prev_end = True
            continue
        if line.startswith('#'):
            continue

        is_par = False
        if is_ivtff:
            m = re.search(r'<f(\d+[rv]\d*)([^>]*)>', line.lower())
            if m:
                nf, meta = m.group(1), m.group(2)
                if nf != cur_fol or '@p' in meta or prev_end:
                    is_par = True
                    par_id += 1
                cur_fol = nf
            prev_end = ('<$>' in line)
            clean = re.sub(r'<[^>]+>|\{[^}]+\}|\[[^\]]+\]|@[0-9;]+', '', line).lower()
            clean = clean.replace('!', '').replace("'", "").replace("’", "").replace(',', '')
            words = [w for w in re.split(r'[\s.]+', clean)
                     if w and w.isalpha() and not re.match(r'^f\d+[rv]\d*$', w)]
        else:
            if prev_end:
                is_par = True
                par_id += 1
                prev_end = False
            words = [w.lower() for w in re.findall(r'[^\W\d_]+', line)]

        if words:
            lines.append((par_id, is_par, words))
    return lines, is_ivtff


def calc_mi(pairs):
    n = len(pairs)
    if n == 0:
        return 0.0
    ca = Counter(a for a, _ in pairs)
    cb = Counter(b for _, b in pairs)
    cab = Counter(pairs)
    return sum((c / n) * math.log2((c / n) / ((ca[a] / n) * (cb[b] / n)))
               for (a, b), c in cab.items())


def asym_stat(pair_counts, min_sum=8):
    keys = sorted({a for a, _ in pair_counts} | {b for _, b in pair_counts})
    total = 0.0
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            cab, cba = pair_counts[(a, b)], pair_counts[(b, a)]
            if cab + cba >= min_sum:
                total += ((cab - cba) ** 2) / (cab + cba)
    return total


def main(filepath, iters=150):
    if not os.path.exists(filepath):
        print(f"Virhe: '{filepath}' ei löydy.")
        return

    lines, is_ivtff = load_universal_lines(filepath)
    all_words = [w for _, _, ws in lines for w in ws]
    if len(all_words) < 50:
        print("Liian vähän sanoja testiin.")
        return

    # Etsitään tekstin omat yleisimmät 2-merkin alut ja loput automaattisesti
    pre2 = Counter(w[:2] for w in all_words if len(w) >= 3)
    suf2 = Counter(w[-2:] for w in all_words if len(w) >= 3)
    top_pre = [k for k, _ in pre2.most_common(6)]
    top_suf = [k for k, _ in suf2.most_common(6)]

    freq = Counter(all_words)
    short_top = {w for w, c in freq.items() if len(w) <= 2 and c >= max(10, len(all_words) * 0.005)}
    cls_cache = {}
    for w in freq:
        if len(w) <= 2:
            cls_cache[w] = f"SH_{w}" if w in short_top else "SHORT"
        elif w[:2] in top_pre:
            cls_cache[w] = f"PRE_{w[:2]}"
        elif w[-2:] in top_suf:
            cls_cache[w] = f"SUF_{w[-2:]}"
        else:
            cls_cache[w] = "OTHER"

    rng = random.Random(1337)
    buckets = defaultdict(list)
    for pid, is_par, words in lines:
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
        for pid, is_par, words in lines:
            n = len(words)
            nw = []
            for i in range(n):
                pos = 'S' if n == 1 else ('PF' if (i == 0 and is_par) else ('LF' if i == 0 else ('LL' if i == n - 1 else 'LM')))
                nw.append(sb[(pid, pos)][cnt[(pid, pos)]])
                cnt[(pid, pos)] += 1
            sc.append((pid, is_par, nw))
        shuf_corpora.append(sc)

    def char_mi(src, dist):
        return calc_mi([(ws[i][-1], ws[i + dist][0]) for _, _, ws in src if len(ws) > dist for i in range(len(ws) - dist)])

    def cls_asym(src, max_freq=None):
        c = Counter()
        for _, _, ws in src:
            for i in range(len(ws) - 1):
                w1, w2 = ws[i], ws[i + 1]
                if max_freq is None or (freq[w1] <= max_freq and freq[w2] <= max_freq):
                    c[(cls_cache[w1], cls_cache[w2])] += 1
        return asym_stat(c, min_sum=6)

    print("\n" + "=" * 78)
    print(f" YLEISPÄTEVÄ SYNTAKSIVERTAILU: '{filepath}' ({len(all_words):,} sanaa, IVTFF={is_ivtff})")
    print("=" * 78)
    print(f" Tekstin omat top-alut: {top_pre} | top-loput: {top_suf}")

    for dist in (1, 2):
        rm = char_mi(lines, dist)
        sms = [char_mi(sc, dist) for sc in shuf_corpora]
        mu = sum(sms) / iters
        sd = math.sqrt(sum((x - mu) ** 2 for x in sms) / iters)
        z = (rm - mu) / (sd if sd > 0 else 1e-9)
        print(f" Rajakirjain MI [Etäisyys {dist}]: {rm:.5f} vs {mu:.5f} (x{rm/mu if mu>0 else 0:4.2f}) | Z = {z:+6.2f}")

    for label, mf in [("Suuntaepäsymmetria (Kaikki sanat)", None),
                      ("Suuntaepäsymmetria (Ei yleisimmät <=20)", 20)]:
        rt = cls_asym(lines, mf)
        sts = [cls_asym(sc, mf) for sc in shuf_corpora]
        mu = sum(sts) / iters
        sd = math.sqrt(sum((x - mu) ** 2 for x in sts) / iters)
        z = (rt - mu) / (sd if sd > 0 else 1e-9)
        p = (sum(x >= rt for x in sts) + 1) / (iters + 1)
        print(f" {label:<40}: {rt:6.1f} vs {mu:5.1f} | Z = {z:+6.2f} | p = {p:.4f}")

    prev_end_all = Counter(ws[i][-1] for _, _, ws in lines for i in range(len(ws) - 1))
    tot_prev = sum(prev_end_all.values())
    pre_prev_map = defaultdict(Counter)
    for _, _, ws in lines:
        for i in range(len(ws) - 1):
            if len(ws[i + 1]) >= 3:
                pre_prev_map[ws[i + 1][:2]][ws[i][-1]] += 1

    best_lift = []
    if tot_prev > 0:
        for p2, cnts in pre_prev_map.items():
            tot_p2 = sum(cnts.values())
            if tot_p2 < max(25, len(all_words) * 0.01):
                continue
            ch, top_c = cnts.most_common(1)[0]
            pct = top_c * 100 / tot_p2
            base = prev_end_all[ch] * 100 / tot_prev
            best_lift.append((pct - base, p2, tot_p2, ch, pct, base))
    best_lift.sort(reverse=True)

    print("\n Vahvin edellisen sanan loppukirjaimen sitoma 2-merkin alku:")
    for diff, p2, tot_p2, ch, pct, base in best_lift[:4]:
        print(f"   Alku '{p2}-' (N={tot_p2:4d}): edellä '{ch}' {pct:5.1f}% (pohjataso {base:5.1f}%, ero {diff:+5.1f}%)")
    print("=" * 78)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Käyttö: python universal_syntax_bench.py <tiedosto.txt>")