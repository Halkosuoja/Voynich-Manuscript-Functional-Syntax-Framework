#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2026 Juho Olavi Laakso
# SPDX-License-Identifier: MIT
"""
VFSF Directionality & -y Subtype Probe
1) Testaa suunnatun järjestyksen (A->B vs B->A) asymmetriaa (kappale & riviasema lukittu).
2) Mittaa takaperin: mikä edeltää qo-sanoja?
3) Tulostaa -dy / -ey / -hy / -ky / -ty / -ly -ryhmien sijainti- ja rakenneprofiilit.
"""
import re
import sys
import os
import math
import random
from collections import Counter, defaultdict


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
                lines.append((par_id, is_par, words))
    return lines


def asym_stat(pair_counts):
    keys = sorted({a for a, _ in pair_counts} | {b for _, b in pair_counts})
    total = 0.0
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            cab = pair_counts[(a, b)]
            cba = pair_counts[(b, a)]
            if cab + cba >= 10:
                total += ((cab - cba) ** 2) / (cab + cba)
    return total


def main(filepath, iters=200):
    if not os.path.exists(filepath):
        print(f"Virhe: '{filepath}' ei löydy.")
        return

    lines = load_clean_lines(filepath)
    rng = random.Random(1337)

    # Ryhmitellään sanat kappaleiden ja riviasemien mukaan sekoitusta varten
    buckets = defaultdict(list)
    real_pairs = Counter()
    par_words = defaultdict(list)

    for pid, is_par, words in lines:
        n = len(words)
        for i in range(n - 1):
            real_pairs[(word_class(words[i]), word_class(words[i + 1]))] += 1
        for i, w in enumerate(words):
            pos = 'S' if n == 1 else ('PF' if (i == 0 and is_par) else ('LF' if i == 0 else ('LL' if i == n - 1 else 'LM')))
            buckets[(pid, pos)].append(w)
            par_words[pid].append((w, pos))

    real_asym = asym_stat(real_pairs)
    shuf_asyms = []
    shuf_diff_lists = defaultdict(list)

    all_classes = sorted({a for a, _ in real_pairs} | {b for _, b in real_pairs})

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
                sp[(word_class(nw[i]), word_class(nw[i + 1]))] += 1
        shuf_asyms.append(asym_stat(sp))
        for i, a in enumerate(all_classes):
            for b in all_classes[i + 1:]:
                shuf_diff_lists[(a, b)].append(sp[(a, b)] - sp[(b, a)])

    mu = sum(shuf_asyms) / iters
    sd = math.sqrt(sum((x - mu) ** 2 for x in shuf_asyms) / iters)
    z_asym = (real_asym - mu) / (sd if sd > 0 else 1e-9)
    p_asym = (sum(x >= real_asym for x in shuf_asyms) + 1) / (iters + 1)

    print("\n" + "=" * 82)
    print(" 1. SUUNTAEPÄSYMMETRIATESTI (A->B vs B->A, kappale & riviasema lukittu)")
    print("=" * 82)
    print(f" Asymmetriaindeksi: {real_asym:.1f} vs. sekoitus ka. {mu:.1f} | Z = {z_asym:+6.2f} | p = {p_asym:.4f}")
    print("\n Vahvimmat suunnatut parit (verrattuna sekoituksen luonnolliseen asymmetriaan):")
    ranked_asym = []
    for (a, b), vals in shuf_diff_lists.items():
        cab, cba = real_pairs[(a, b)], real_pairs[(b, a)]
        if cab + cba < 40:
            continue
        real_d = cab - cba
        mu_d = sum(vals) / iters
        sd_d = math.sqrt(sum((x - mu_d) ** 2 for x in vals) / iters)
        z_d = (real_d - mu_d) / (sd_d if sd_d > 0 else 1.0)
        ranked_asym.append((abs(z_d), z_d, a, b, cab, cba, mu_d))
    ranked_asym.sort(reverse=True)
    for _, z_d, a, b, cab, cba, mu_d in ranked_asym[:10]:
        arrow = f"{a} -> {b}" if z_d > 0 else f"{b} -> {a}"
        fwd, rev = (cab, cba) if z_d > 0 else (cba, cab)
        print(f"   {arrow:<22} | Suunta: {fwd:4d} vs. Takaisin: {rev:4d} (Sekoitus ero: {mu_d:+5.1f}) | Z={abs(z_d):5.2f}")

    # 2. Mitä tulee ennen qo-sanoja? (aito vs odotusarvo)
    pre_qo = Counter()
    all_prev_chars = Counter()
    for _, _, words in lines:
        for i in range(len(words) - 1):
            all_prev_chars[words[i][-1]] += 1
            if words[i + 1].startswith('qo'):
                pre_qo[words[i][-1]] += 1

    tot_qo = sum(pre_qo.values())
    tot_all = sum(all_prev_chars.values())
    print("\n" + "=" * 82)
    print(f" 2. MIKÄ EDELTÄÄ 'qo-' SANOJA? (N={tot_qo})")
    print("=" * 82)
    for ch, cnt in pre_qo.most_common(6):
        pct_qo = cnt * 100 / tot_qo
        pct_base = all_prev_chars[ch] * 100 / tot_all
        print(f"   Edellinen päättyy '{ch}': {cnt:4d} ({pct_qo:5.1f}% ennen qo- | pohjatason yleisyys: {pct_base:5.1f}%)")

    # 3. -y päätteiden sijainti- ja alkumerkkiprofiilit
    y_pos = defaultdict(Counter)
    y_par_rel = defaultdict(list)
    y_starts = defaultdict(Counter)

    # Lasketaan suhteellinen paikka kappaleessa
    for pid, items in par_words.items():
        m_len = len(items)
        for idx, (w, pos) in enumerate(items):
            if w.endswith('y') and len(w) >= 2:
                suf = w[-2:]
                if suf in ('dy', 'ey', 'hy', 'ky', 'ty', 'ly'):
                    y_pos[suf][pos] += 1
                    y_par_rel[suf].append(idx / max(1, m_len - 1))
                    head = next((p for p in ('qo', 'ch', 'sh', 'ot', 'ok', 'cth', 'ckh', 'da') if w.startswith(p)), w[0])
                    y_starts[suf][head] += 1

    print("\n" + "=" * 82)
    print(" 3. -y PÄÄTTEIDEN SIJAINTI RIVILLÄ, KAPPALEESSA JA ALKUETULIITTEET")
    print("=" * 82)
    for suf in ('dy', 'ey', 'hy', 'ky', 'ty', 'ly'):
        tot = sum(y_pos[suf].values())
        if tot == 0:
            continue
        lf = (y_pos[suf]['LF'] + y_pos[suf]['PF']) * 100 / tot
        lm = y_pos[suf]['LM'] * 100 / tot
        ll = y_pos[suf]['LL'] * 100 / tot
        rel = sum(y_par_rel[suf]) / len(y_par_rel[suf])
        top_st = ", ".join(f"{k}:{v*100/tot:.0f}%" for k, v in y_starts[suf].most_common(4))
        print(f"   -{suf} (N={tot:4d}) | Alku:{lf:4.1f}% Keski:{lm:4.1f}% Loppu:{ll:4.1f}% | Kappale-keskikohta:{rel:.2f} | Alut: {top_st}")
    print("=" * 82)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Käyttö: python vfsf_direction_and_y_probe.py ZL3b-n.txt")