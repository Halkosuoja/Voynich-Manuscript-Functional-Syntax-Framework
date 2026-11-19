#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2026 Juho Olavi Laakso
# SPDX-License-Identifier: MIT
"""
VFSF Concrete Connector & Harmony Examples
Tulostaa konkreettiset sanaparit tilastopiikkien takaa ilman arvailua.
"""
import re
import sys
import os
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


def main(filepath):
    if not os.path.exists(filepath):
        print(f"Virhe: '{filepath}' ei löydy.")
        return

    lines = load_clean_lines(filepath)
    all_words = [w for _, _, ws in lines for w in ws]

    o_bare = Counter()
    o_bridged = Counter()
    s_a = Counter()
    r_a = Counter()
    dy_dy = Counter()
    ey_ey = Counter()
    ol_ol = Counter()

    bridged_sub_pos = defaultdict(Counter)
    bridged_sub_prev = defaultdict(Counter)
    o_only_gal = 0
    word_o_gal = 0

    for _, is_par, ws in lines:
        n = len(ws)
        for i, w in enumerate(ws):
            pos = 'S' if n == 1 else ('PF' if (i == 0 and is_par) else ('LF' if i == 0 else ('LL' if i == n - 1 else 'LM')))
            for b in ('ckh', 'cth', 'cph', 'cfh'):
                if w.startswith(b):
                    bridged_sub_pos[b][pos] += 1
                    if i > 0:
                        bridged_sub_prev[b][ws[i - 1][-1]] += 1

        for i in range(n - 1):
            w1, w2 = ws[i], ws[i + 1]
            pair = f"{w1} -> {w2}"
            if w1.endswith('o') and w2.startswith(('k', 't', 'p', 'f')):
                o_bare[pair] += 1
                if w1 == 'o':
                    o_only_gal += 1
                else:
                    word_o_gal += 1
            if w1.endswith('o') and w2.startswith(('ckh', 'cth', 'cph', 'cfh')):
                o_bridged[pair] += 1
            if w1.endswith('s') and w2.startswith('a'):
                s_a[pair] += 1
            if w1.endswith('r') and w2.startswith('a'):
                r_a[pair] += 1
            if w1 != w2:
                if w1.endswith('dy') and w2.endswith('dy'):
                    dy_dy[pair] += 1
                elif w1.endswith('ey') and w2.endswith('ey'):
                    ey_ey[pair] += 1
                elif w1.endswith('ol') and w2.endswith('ol'):
                    ol_ol[pair] += 1

    inside_ok_ot = sum(1 for w in all_words if w.startswith(('ok', 'ot', 'op', 'of')))

    print("\n" + "=" * 82)
    print(" 1. -o -> PALJAS GALLOWS (2.47x) JA -o -> SILLOITETTU GALLOWS (1.60x)")
    print("=" * 82)
    print(f" Irrallinen 'o' + k/t/p/f: {o_only_gal} | Pidempisana '...o' + k/t/p/f: {word_o_gal}")
    print(f" (Vertailuksi yhteen kirjoitetut ok-/ot-/op-/of-sanat korpuksessa: {inside_ok_ot:,} kpl)")
    print(" Top 10 (-o -> paljas gallows):", ", ".join(f"{k} ({v})" for k, v in o_bare.most_common(10)))
    print(" Top 10 (-o -> silloitettu):   ", ", ".join(f"{k} ({v})" for k, v in o_bridged.most_common(10)))

    print("\n" + "=" * 82)
    print(" 2. -s -> a- (4.68x) JA -r -> a- (2.99x) KONKREETTISET PARIT")
    print("=" * 82)
    print(" Top 10 (-s -> a-):", ", ".join(f"{k} ({v})" for k, v in s_a.most_common(10)))
    print(" Top 10 (-r -> a-):", ", ".join(f"{k} ({v})" for k, v in r_a.most_common(10)))

    print("\n" + "=" * 82)
    print(" 3. SILLOITETTUJEN GALLOWSIEN (ckh/cth/cph/cfh) ALATYYPIT")
    print("=" * 82)
    for b in ('ckh', 'cth', 'cph', 'cfh'):
        tot = sum(bridged_sub_pos[b].values())
        ll = bridged_sub_pos[b]['LL'] * 100 / tot if tot else 0
        lm = bridged_sub_pos[b]['LM'] * 100 / tot if tot else 0
        top_p = ", ".join(f"-{k}:{v}" for k, v in bridged_sub_prev[b].most_common(4))
        print(f"   {b}- (N={tot:3d}) | Keski:{lm:4.1f}% Loppu:{ll:4.1f}% | Edeltävät: {top_p}")

    print("\n" + "=" * 82)
    print(" 4. PÄÄTESOINNUN KONKREETTISET PARIT (w1 != w2)")
    print("=" * 82)
    print(" Top 8 (-dy -> -dy):", ", ".join(f"{k} ({v})" for k, v in dy_dy.most_common(8)))
    print(" Top 8 (-ey -> -ey):", ", ".join(f"{k} ({v})" for k, v in ey_ey.most_common(8)))
    print(" Top 8 (-ol -> -ol):", ", ".join(f"{k} ({v})" for k, v in ol_ol.most_common(8)))
    print("=" * 82)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Käyttö: python vfsf_connector_examples.py ZL3b-n.txt")