#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2026 Juho Olavi Laakso
# SPDX-License-Identifier: MIT
"""
VFSF Repeat X-Ray (d1: A-A ja d2: A-X-A)
Näyttää, mitkä sanat toistuvat peräkkäin tai kahden sanan päässä
ja ylittävätkö toistot kappale- & riviasemalukitun satunnaisuuden.
"""
import re
import sys
import os
import math
import random
from collections import Counter, defaultdict


def load_lines(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            raw_text = f.read()
    except UnicodeDecodeError:
        with open(filepath, 'r', encoding='cp1252', errors='replace') as f:
            raw_text = f.read()

    is_ivtff = ('<$>' in raw_text or len(re.findall(r'<f\d+[rv]', raw_text.lower())) >= 3)
    lines = []
    par_id = 0
    cur_fol = None
    prev_end = True

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
    return lines


def analyze_repeats(label, lines, iters=150):
    d1_words = Counter()
    d2_words = Counter()
    d2_triplets = Counter()
    tot1 = tot2 = 0

    for _, _, ws in lines:
        for i in range(len(ws) - 1):
            tot1 += 1
            if ws[i] == ws[i + 1]:
                d1_words[ws[i]] += 1
        for i in range(len(ws) - 2):
            tot2 += 1
            if ws[i] == ws[i + 2]:
                d2_words[ws[i]] += 1
                d2_triplets[f"{ws[i]} - {ws[i+1]} - {ws[i+2]}"] += 1

    # Kappale- ja riviasemalukittu Monte Carlo
    rng = random.Random(1337)
    buckets = defaultdict(list)
    for pid, is_par, ws in lines:
        n = len(ws)
        for i, w in enumerate(ws):
            pos = 'S' if n == 1 else ('PF' if (i == 0 and is_par) else ('LF' if i == 0 else ('LL' if i == n - 1 else 'LM')))
            buckets[(pid, pos)].append(w)

    s1_pcts, s2_pcts = [], []
    for _ in range(iters):
        sb = {k: v.copy() for k, v in buckets.items()}
        for k in sb:
            rng.shuffle(sb[k])
        cnt = defaultdict(int)
        c1 = c2 = 0
        for pid, is_par, ws in lines:
            n = len(ws)
            nw = []
            for i in range(n):
                pos = 'S' if n == 1 else ('PF' if (i == 0 and is_par) else ('LF' if i == 0 else ('LL' if i == n - 1 else 'LM')))
                nw.append(sb[(pid, pos)][cnt[(pid, pos)]])
                cnt[(pid, pos)] += 1
            for i in range(n - 1):
                if nw[i] == nw[i + 1]:
                    c1 += 1
            for i in range(n - 2):
                if nw[i] == nw[i + 2]:
                    c2 += 1
        s1_pcts.append(c1 * 100 / max(1, tot1))
        s2_pcts.append(c2 * 100 / max(1, tot2))

    r1 = sum(d1_words.values()) * 100 / max(1, tot1)
    r2 = sum(d2_words.values()) * 100 / max(1, tot2)
    m1, m2 = sum(s1_pcts) / iters, sum(s2_pcts) / iters
    sd1 = math.sqrt(sum((x - m1) ** 2 for x in s1_pcts) / iters) or 1e-9
    sd2 = math.sqrt(sum((x - m2) ** 2 for x in s2_pcts) / iters) or 1e-9
    z1, z2 = (r1 - m1) / sd1, (r2 - m2) / sd2

    long1 = sum(v for k, v in d1_words.items() if len(k) >= 4) * 100 / max(1, sum(d1_words.values()))
    long2 = sum(v for k, v in d2_words.items() if len(k) >= 4) * 100 / max(1, sum(d2_words.values()))

    print("\n" + "=" * 82)
    print(f" TOISTORÖNTGEN: {label}")
    print("=" * 82)
    print(f" d1 (A - A):   {sum(d1_words.values()):3d} kpl ({r1:.2f}% vs. sekoitus {m1:.2f}%) | Z = {z1:+6.2f} | Uniikkeja: {len(d1_words)} | Pitkiä(>=4): {long1:.0f}%")
    print(f" d2 (A - X - A): {sum(d2_words.values()):3d} kpl ({r2:.2f}% vs. sekoitus {m2:.2f}%) | Z = {z2:+6.2f} | Uniikkeja: {len(d2_words)} | Pitkiä(>=4): {long2:.0f}%")
    print(" Top 10 d1 (A - A):     ", ", ".join(f"{k} ({v})" for k, v in d1_words.most_common(10)))
    print(" Top 10 d2 sanat:       ", ", ".join(f"{k} ({v})" for k, v in d2_words.most_common(10)))
    print(" Top 10 d2 (A - X - A): ", ", ".join(f"{k} ({v})" for k, v in d2_triplets.most_common(10)))


def main():
    if len(sys.argv) < 2:
        print("Käyttö: python vfsf_repeat_xray.py ZL3b-n.txt [verrokki.txt]")
        return
    for path in sys.argv[1:]:
        if os.path.exists(path):
            analyze_repeats(path, load_lines(path))
        else:
            print(f"Virhe: '{path}' ei löydy.")
    print("=" * 82)


if __name__ == "__main__":
    main()