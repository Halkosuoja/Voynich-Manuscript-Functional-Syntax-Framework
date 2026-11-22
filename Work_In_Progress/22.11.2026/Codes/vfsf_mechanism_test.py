#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2026 Juho Olavi Laakso
# SPDX-License-Identifier: MIT
"""
VFSF Mechanism Test (Suunta A & Suunta B)
- Suunta B: Rakentaa 1-askeleen rajakytkentägeneraattorin (ZL3b-n.txt) ja vertaa
  sen tuottamaa tekstiä aitoon Voynichiin (Etäisyys 1/2, päätesointu, toistot, sanavarasto).
- Suunta A: Muuntaa luonnollista tekstiä (Plinius / Matteus1548) kolmella mekaanisella
  säännöllä ja tarkistaa, saako mikään niistä aikaan Voynichin rajakäyttäytymistä.
"""
import re
import sys
import os
import math
import random
from collections import Counter, defaultdict


def load_lines(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
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


def calc_mi(pairs):
    n = len(pairs)
    if n == 0:
        return 0.0
    ca = Counter(a for a, _ in pairs)
    cb = Counter(b for _, b in pairs)
    cab = Counter(pairs)
    return sum((c / n) * math.log2((c / n) / ((ca[a] / n) * (cb[b] / n)))
               for (a, b), c in cab.items())


def end_tag(w):
    for s in ('dy', 'ey', 'hy', 'ol', 'or', 'al', 'ar', 'aiin', 'ain'):
        if w.endswith(s) and len(w) > len(s):
            return s
    return None


def measure_profile(label, lines, iters=60):
    all_w = [w for _, _, ws in lines for w in ws]
    rng = random.Random(1337)
    buckets = defaultdict(list)
    for pid, is_par, ws in lines:
        n = len(ws)
        for i, w in enumerate(ws):
            pos = 'S' if n == 1 else ('PF' if (i == 0 and is_par) else ('LF' if i == 0 else ('LL' if i == n - 1 else 'LM')))
            buckets[(pid, pos)].append(w)

    def char_mi(src, d):
        return calc_mi([(ws[i][-1], ws[i + d][0]) for _, _, ws in src if len(ws) > d for i in range(len(ws) - d)])

    sd1, sd2 = [], []
    for _ in range(iters):
        sb = {k: v.copy() for k, v in buckets.items()}
        for k in sb:
            rng.shuffle(sb[k])
        cnt = defaultdict(int)
        sl = []
        for pid, is_par, ws in lines:
            n = len(ws)
            nw = []
            for i in range(n):
                pos = 'S' if n == 1 else ('PF' if (i == 0 and is_par) else ('LF' if i == 0 else ('LL' if i == n - 1 else 'LM')))
                nw.append(sb[(pid, pos)][cnt[(pid, pos)]])
                cnt[(pid, pos)] += 1
            sl.append((pid, is_par, nw))
        sd1.append(char_mi(sl, 1))
        sd2.append(char_mi(sl, 2))

    r1, r2 = char_mi(lines, 1), char_mi(lines, 2)
    m1, m2 = sum(sd1) / iters, sum(sd2) / iters
    net1, net2 = r1 - m1, r2 - m2
    ret = (net2 * 100 / net1) if net1 > 0 else 0.0

    # Toisto ja päätesointu
    rep1 = tot1 = rep2 = tot2 = harm1 = htot1 = harm2 = htot2 = 0
    for _, _, ws in lines:
        for i in range(len(ws) - 1):
            tot1 += 1
            if ws[i] == ws[i + 1]:
                rep1 += 1
            else:
                e1, e2 = end_tag(ws[i]), end_tag(ws[i + 1])
                if e1 and e2:
                    htot1 += 1
                    if e1 == e2:
                        harm1 += 1
        for i in range(len(ws) - 2):
            tot2 += 1
            if ws[i] == ws[i + 2]:
                rep2 += 1
            else:
                e1, e2 = end_tag(ws[i]), end_tag(ws[i + 2])
                if e1 and e2:
                    htot2 += 1
                    if e1 == e2:
                        harm2 += 1

    # Vahvin sidottu 2-merkin alku
    prev_all = Counter(ws[i][-1] for _, _, ws in lines for i in range(len(ws) - 1))
    tot_p = sum(prev_all.values()) or 1
    pmap = defaultdict(Counter)
    for _, _, ws in lines:
        for i in range(len(ws) - 1):
            if len(ws[i + 1]) >= 3:
                pmap[ws[i + 1][:2]][ws[i][-1]] += 1
    top_bind = "-"
    best_diff = -1.0
    for p2, cnts in pmap.items():
        tp2 = sum(cnts.values())
        if tp2 < max(25, len(all_w) * 0.01):
            continue
        ch, tc = cnts.most_common(1)[0]
        diff = tc * 100 / tp2 - prev_all[ch] * 100 / tot_p
        if diff > best_diff:
            best_diff = diff
            top_bind = f"'{p2}-'({tp2*100/len(all_w):.1f}%)<-'{ch}'({tc*100/tp2:.0f}%,+{diff:.0f}%)"

    print(f"\n [{label}] Sanat: {len(all_w):,} | Uniikit: {len(set(all_w)):,}")
    print(f"   Etäisyys 1 MI: {r1:.5f} vs {m1:.5f} (x{r1/m1 if m1 else 0:5.2f}, netto {net1:+.5f})")
    print(f"   Etäisyys 2 MI: {r2:.5f} vs {m2:.5f} (x{r2/m2 if m2 else 0:5.2f}, netto {net2:+.5f}) | Säilyvyys: {ret:4.1f}%")
    print(f"   Sama sana toisto: d1={rep1*100/max(1,tot1):.2f}% | d2={rep2*100/max(1,tot2):.2f}%")
    print(f"   Päätesointu (w1!=w2): d1={harm1*100/max(1,htot1):.2f}% | d2={harm2*100/max(1,htot2):.2f}%")
    print(f"   Vahvin rajakytkentä: {top_bind}")


def build_1step_connector_gen(lines):
    rng = random.Random(2026)
    starts_pf = []
    starts_lf = []
    trans = defaultdict(list)
    singles = []

    for _, is_par, ws in lines:
        n = len(ws)
        if n == 1:
            singles.append(ws[0])
            continue
        if is_par:
            starts_pf.append(ws[0])
        else:
            starts_lf.append(ws[0])
        for i in range(n - 1):
            pos = 'LL' if i + 1 == n - 1 else 'LM'
            trans[(ws[i][-1], pos)].append(ws[i + 1])

    fallback = [w for _, _, ws in lines for w in ws]
    gen_lines = []
    for pid, is_par, ws in lines:
        n = len(ws)
        if n == 1:
            gen_lines.append((pid, is_par, [rng.choice(singles)]))
            continue
        first = rng.choice(starts_pf if is_par and starts_pf else starts_lf)
        out = [first]
        for i in range(n - 1):
            pos = 'LL' if i + 1 == n - 1 else 'LM'
            pool = trans.get((out[-1][-1], pos), fallback)
            out.append(rng.choice(pool))
        gen_lines.append((pid, is_par, out))
    return gen_lines


def transform_boundary_shift(lines):
    out = []
    for pid, is_par, ws in lines:
        if len(ws) < 2:
            out.append((pid, is_par, ws))
            continue
        nws = []
        carry = ""
        for i, w in enumerate(ws):
            if i == 0:
                nws.append(w)
            else:
                if len(w) >= 2:
                    nws[-1] = nws[-1] + w[0]
                    nws.append(w[1:])
                else:
                    nws.append(w)
        out.append((pid, is_par, nws))
    return out


def transform_split_before_stops(lines):
    out = []
    for pid, is_par, ws in lines:
        joined = "".join(ws)
        chunks = []
        cur = ""
        for ch in joined:
            if ch in ('c', 'k', 'p', 't', 'q') and len(cur) >= 3:
                chunks.append(cur)
                cur = ch
            else:
                cur += ch
        if cur:
            chunks.append(cur)
        if chunks:
            out.append((pid, is_par, chunks))
    return out


def transform_bigram_cipher(lines, voynich_vocab):
    rng = random.Random(99)
    vocab_pool = list(voynich_vocab)
    rng.shuffle(vocab_pool)
    bmap = {}
    idx = 0
    out = []
    for pid, is_par, ws in lines:
        joined = "".join(ws)
        nws = []
        for i in range(0, len(joined) - 1, 2):
            bg = joined[i:i + 2]
            if bg not in bmap:
                bmap[bg] = vocab_pool[idx % len(vocab_pool)]
                idx += 1
            nws.append(bmap[bg])
        if nws:
            out.append((pid, is_par, nws))
    return out


def main():
    if len(sys.argv) < 2:
        print("Käyttö: python vfsf_mechanism_test.py ZL3b-n.txt [luonnollinen_teksti.txt]")
        return

    v_path = sys.argv[1]
    if not os.path.exists(v_path):
        print(f"Virhe: '{v_path}' ei löydy.")
        return

    v_lines = load_lines(v_path)
    v_vocab = set(w for _, _, ws in v_lines for w in ws)

    print("=" * 80)
    print(" SUUNTA B: AITO VOYNICH vs. 1-ASKELEEN LIITIN-GENERAATTORI")
    print("=" * 80)
    measure_profile("AITO VOYNICH (ZL3b-n.txt)", v_lines)
    gen_b = build_1step_connector_gen(v_lines)
    measure_profile("SUUNTA B: 1-askeleen Liitin-generaattori", gen_b)

    if len(sys.argv) > 2 and os.path.exists(sys.argv[2]):
        n_path = sys.argv[2]
        n_lines = load_lines(n_path)
        print("\n" + "=" * 80)
        print(f" SUUNTA A: LUONNOLLISEN KIELEN MEKAANISET MUUNNOKSET ('{n_path}')")
        print("=" * 80)
        measure_profile(f"Alkuperäinen '{n_path}'", n_lines)
        measure_profile("A1: 1-merkin rajasiirto (sanan eka merkki edelliseen)", transform_boundary_shift(n_lines))
        measure_profile("A2: Jako ennen c/k/p/t/q -merkkejä", transform_split_before_stops(n_lines))
        measure_profile("A3: 2-merkin bigrammikoodi Voynich-sanastolla", transform_bigram_cipher(n_lines, v_vocab))
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()