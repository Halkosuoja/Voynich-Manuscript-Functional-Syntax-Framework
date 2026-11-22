#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VFSF Test A & B: Suffix Harmony (excluding identical repeats) & Bare vs Bridged Gallows
"""
import re
import sys
import os
import math
import random
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


def end_tag(w):
    for s in ('aiin', 'ain', 'iin', 'dy', 'ey', 'hy', 'ky', 'ty', 'ly', 'ol', 'or', 'al', 'ar'):
        if w.endswith(s) and len(w) > len(s):
            return s
    return None


def gal_group(w):
    if w.startswith(('ckh', 'cth', 'cph', 'cfh')):
        return 'BRIDGED_GAL'
    if w.startswith('ch'):
        return 'PLAIN_CH'
    if w.startswith(('k', 't', 'p', 'f')):
        return 'BARE_GAL'
    if w.startswith(('qok', 'qot', 'qop', 'qof')):
        return 'QO_GAL'
    return None


def count_same_endings(lines_src, dist, targets):
    same_c = Counter()
    tot = 0
    for _, _, ws in lines_src:
        if len(ws) <= dist:
            continue
        for i in range(len(ws) - dist):
            w1, w2 = ws[i], ws[i + dist]
            if w1 == w2:
                continue  # Ohitetaan identtisen sanan suora toisto
            e1, e2 = end_tag(w1), end_tag(w2)
            if e1 in targets and e2 in targets:
                tot += 1
                if e1 == e2:
                    same_c[e1] += 1
    return same_c, tot


def main(filepath, iters=200):
    if not os.path.exists(filepath):
        print(f"Virhe: '{filepath}' ei löydy.")
        return

    lines = load_clean_lines(filepath)
    rng = random.Random(1337)
    targets = ('dy', 'ey', 'hy', 'ol', 'or', 'al', 'ar', 'aiin', 'ain')

    buckets = defaultdict(list)
    for pid, is_par, ws in lines:
        n = len(ws)
        for i, w in enumerate(ws):
            pos = 'S' if n == 1 else ('PF' if (i == 0 and is_par) else ('LF' if i == 0 else ('LL' if i == n - 1 else 'LM')))
            buckets[(pid, pos)].append(w)

    shuf_d1_tot, shuf_d2_tot = [], []
    shuf_d1_by_end = defaultdict(list)

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
        c1, t1 = count_same_endings(sl, 1, targets)
        c2, t2 = count_same_endings(sl, 2, targets)
        shuf_d1_tot.append(sum(c1.values()) * 100 / t1 if t1 else 0)
        shuf_d2_tot.append(sum(c2.values()) * 100 / t2 if t2 else 0)
        for t in targets:
            shuf_d1_by_end[t].append(c1[t])

    rc1, rt1 = count_same_endings(lines, 1, targets)
    rc2, rt2 = count_same_endings(lines, 2, targets)
    pct1 = sum(rc1.values()) * 100 / rt1 if rt1 else 0
    pct2 = sum(rc2.values()) * 100 / rt2 if rt2 else 0
    mu1, mu2 = sum(shuf_d1_tot) / iters, sum(shuf_d2_tot) / iters
    sd1 = math.sqrt(sum((x - mu1) ** 2 for x in shuf_d1_tot) / iters)
    sd2 = math.sqrt(sum((x - mu2) ** 2 for x in shuf_d2_tot) / iters)

    print("\n" + "=" * 84)
    print(" A. PÄÄTEKONGRUENSSI (Vain w1 != w2, kappale & riviasema lukittu)")
    print("=" * 84)
    print(f" Etäisyys 1 sama pääte: {pct1:5.2f}% vs sekoitus {mu1:5.2f}% | Z = {(pct1-mu1)/(sd1 or 1):+6.2f}")
    print(f" Etäisyys 2 sama pääte: {pct2:5.2f}% vs sekoitus {mu2:5.2f}% | Z = {(pct2-mu2)/(sd2 or 1):+6.2f}")
    print("\n Päätteittäin (Etäisyys 1, sama pääte kahdella ERI sanalla):")
    for t in targets:
        vals = shuf_d1_by_end[t]
        mu_t = sum(vals) / iters
        sd_t = math.sqrt(sum((x - mu_t) ** 2 for x in vals) / iters)
        z_t = (rc1[t] - mu_t) / (sd_t if sd_t > 0 else 1.0)
        print(f"   -{t:<5} -> -{t:<5} | Osuma: {rc1[t]:4d} (Sekoitus ka: {mu_t:5.1f}) | Z = {z_t:+6.2f}")

    # --- TESTI B: PALJAAT vs SILLOITETUT GALLOWSIT ---
    gal_pos = defaultdict(Counter)
    gal_prev = defaultdict(Counter)
    gal_end = defaultdict(Counter)
    base_prev = Counter()

    for _, is_par, ws in lines:
        n = len(ws)
        for i, w in enumerate(ws):
            pos = 'S' if n == 1 else ('PF' if (i == 0 and is_par) else ('LF' if i == 0 else ('LL' if i == n - 1 else 'LM')))
            if i > 0:
                base_prev[ws[i - 1][-1]] += 1
            g = gal_group(w)
            if not g:
                continue
            gal_pos[g][pos] += 1
            if i > 0:
                gal_prev[g][ws[i - 1][-1]] += 1
            if w.endswith('y'):
                gal_end[g]['-y'] += 1
            elif w.endswith(('aiin', 'ain', 'iin')):
                gal_end[g]['-n'] += 1
            elif w.endswith(('ol', 'or', 'al', 'ar')):
                gal_end[g]['-ol/r'] += 1
            else:
                gal_end[g]['muu'] += 1

    tot_bp = sum(base_prev.values())
    print("\n" + "=" * 84)
    print(" B. PALJAAT GALLOWSIT vs. SILLOITETUT (ckh/cth/cph/cfh) vs. CH vs. QO+GAL")
    print("=" * 84)
    for g in ('BARE_GAL', 'BRIDGED_GAL', 'PLAIN_CH', 'QO_GAL'):
        tot = sum(gal_pos[g].values())
        if tot == 0:
            continue
        pf = gal_pos[g]['PF'] * 100 / tot
        lf = gal_pos[g]['LF'] * 100 / tot
        lm = gal_pos[g]['LM'] * 100 / tot
        ll = gal_pos[g]['LL'] * 100 / tot
        tot_p = sum(gal_prev[g].values()) or 1
        lifts = []
        for ch in ('y', 'n', 'r', 'l', 's', 'o'):
            obs_p = gal_prev[g][ch] / tot_p
            exp_p = base_prev[ch] / tot_bp
            lifts.append(f"-{ch}:{obs_p/exp_p:.2f}x")
        ends_s = ", ".join(f"{k}:{gal_end[g][k]*100/tot:.0f}%" for k in ('-y', '-ol/r', '-n', 'muu'))
        print(f" [{g:<11}] N={tot:4d} | Sijainti PF:{pf:4.1f}% LF:{lf:4.1f}% LM:{lm:4.1f}% LL:{ll:4.1f}%")
        print(f"   Edeltävä loppu: {' | '.join(lifts)}")
        print(f"   Oma loppu:      {ends_s}")
    print("=" * 84)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Käyttö: python vfsf_harmony_and_ligatures.py ZL3b-n.txt")