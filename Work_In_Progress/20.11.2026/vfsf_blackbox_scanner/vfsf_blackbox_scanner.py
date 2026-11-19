#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VFSF Black-Box Structural Scanner v1.0
Mittaa ennakko-oletuksetta:
1) Onko sanojen välillä peräkkäisriippuvuutta riviaseman lukitsemisen jälkeen (MI + Z-score)
2) Miten ligatuurit (cth, ckh, cph, cfh, ch, sh), oror, -g, dal/dol jakautuvat osioittain
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
    """
    Purkaa sanan VFSF-malliin huomioiden EVA-ligatuurit atomeina:
    cth, ckh, cph, cfh, ch, sh -> yksittäisiä perusyksiköitä.
    Palauttaa (prefix, root_lig, infix_e, suffix).
    """
    w = word.lower()

    # 1. Kestoinfiksi (ee / eee / e)
    if 'eee' in w:
        infix_e = 'E3'
        w_core = w.replace('eee', 'E', 1)
    elif 'ee' in w:
        infix_e = 'E2'
        w_core = w.replace('ee', 'E', 1)
    elif 'e' in w:
        infix_e = 'E1'
        w_core = w_core = w
    else:
        infix_e = 'E0'
        w_core = w

    # 2. Etuliite (Operational Quality)
    prefix = 'NONE'
    rest = w_core
    for p in ('qo', 'ot', 'yt', 'ok', 'yk', 'te', 'op', 'ol', 'or', 'ch', 'sh', 'da', 'so', 'sa', 'q', 'o', 'y', 'd', 's', 'p', 'f', 'k', 't'):
        if rest.startswith(p) and len(rest) > len(p):
            prefix = p
            rest = rest[len(p):]
            break

    # 3. Ligatuuri / Pääsydän (Gallows & Benches atomeina)
    root_lig = 'NONE'
    for lig in ('cth', 'ckh', 'cph', 'cfh', 'ch', 'sh', 'dal', 'dol', 'dar', 'dair', 'k', 't', 'p', 'f'):
        if lig in w:
            root_lig = lig
            break

    # 4. Pääte / Tilalukko
    suffix = 'OTHER'
    for suf in ('aiin', 'aiiin', 'oiin', 'ain', 'iin', 'dy', 'ey', 'hy', 'ky', 'ty', 'ly', 'ry', 'sy', 'am', 'om', 'ol', 'or', 'ar', 'al', 'g', 'm', 'y', 'n', 'l', 'r', 'd'):
        if w.endswith(suf):
            suffix = suf
            break

    return prefix, root_lig, infix_e, suffix


def load_corpus(filepath):
    """
    Lukee IVTFF/ZL-tekstin ja säilyttää folio-, rivi- ja riviasematiedon.
    Palauttaa listan riveistä: [{'folio':..., 'section':..., 'is_par_start':..., 'words': [...]}]
    """
    lines_data = []
    current_folio = "unknown"
    prev_par_end = True

    with open(filepath, 'r', encoding='utf-8') as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith('#'):
                continue

            # Tunnistetaan folio ja kappaleen alku (@P tai uuden sivun alku)
            locus_match = re.search(r'<f(\d+[rv]\d*)([^>]*)>', line.lower())
            is_par_start = False
            if locus_match:
                new_folio = locus_match.group(1)
                meta = locus_match.group(2)
                if new_folio != current_folio:
                    is_par_start = True
                if '@p' in meta or prev_par_end:
                    is_par_start = True
                current_folio = new_folio

            prev_par_end = ('<$>' in line)

            # Siivotaan EVA-merkinnät ja epävarmat korjaukset
            clean = re.sub(r'<[^>]+>', '', line)
            clean = re.sub(r'\{[^}]+\}', '', clean)
            clean = re.sub(r'\[[^\]]+\]', '', clean)
            clean = re.sub(r'@[0-9;]+', '', clean)
            clean = clean.replace("'", "").replace("’", "")
            clean = re.sub(r'[{}\[\]!@%<>?:*#$,=+\-]', ' ', clean)

            words = [w.strip().lower() for w in re.split(r'[\s.]+', clean)
                     if w and not re.match(r'^f\d+[rv]\d*$', w.lower())]
            if not words:
                continue

            lines_data.append({
                'folio': current_folio,
                'section': get_section(current_folio),
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


def extract_adjacent_pairs(lines_data, slot_cache, mode):
    """
    Muodostaa rivin sisäiset peräkkäiset parit (word_i -> word_{i+1}) valitulla tasolla.
    mode: 'prefix', 'root', 'infix', 'suffix', 'suf_to_pre'
    """
    pairs = []
    idx_map = {'prefix': 0, 'root': 1, 'infix': 2, 'suffix': 3}

    for row in lines_data:
        words = row['words']
        if len(words) < 2:
            continue
        for i in range(len(words) - 1):
            s1 = slot_cache[words[i]]
            s2 = slot_cache[words[i + 1]]
            if mode == 'suf_to_pre':
                pairs.append((s1[3], s2[0]))
            else:
                idx = idx_map[mode]
                pairs.append((s1[idx], s2[idx]))
    return pairs


def position_preserving_shuffle(lines_data, rng):
    """
    Sekoittaa sanat VAIN saman folion ja saman riviasemaluokan sisällä:
    PAR_FIRST, LINE_FIRST, LINE_MID, LINE_LAST.
    """
    buckets = defaultdict(list)
    for row in lines_data:
        fol = row['folio']
        words = row['words']
        n = len(words)
        for i, w in enumerate(words):
            if n == 1:
                pos = 'SINGLE'
            elif i == 0:
                pos = 'PAR_FIRST' if row['is_par_start'] else 'LINE_FIRST'
            elif i == n - 1:
                pos = 'LINE_LAST'
            else:
                pos = 'LINE_MID'
            buckets[(fol, pos)].append(w)

    for key in buckets:
        rng.shuffle(buckets[key])

    counters = defaultdict(int)
    shuf_lines = []
    for row in lines_data:
        fol = row['folio']
        n = len(row['words'])
        new_words = []
        for i in range(n):
            if n == 1:
                pos = 'SINGLE'
            elif i == 0:
                pos = 'PAR_FIRST' if row['is_par_start'] else 'LINE_FIRST'
            elif i == n - 1:
                pos = 'LINE_LAST'
            else:
                pos = 'LINE_MID'
            idx = counters[(fol, pos)]
            new_words.append(buckets[(fol, pos)][idx])
            counters[(fol, pos)] += 1
        shuf_lines.append({
            'folio': fol,
            'section': row['section'],
            'is_par_start': row['is_par_start'],
            'words': new_words
        })
    return shuf_lines


def run_scanner(filepath, iterations=200):
    if not os.path.exists(filepath):
        print(f"Virhe: Tiedostoa '{filepath}' ei löydy.")
        return

    lines_data = load_corpus(filepath)
    all_words = [w for r in lines_data for w in r['words']]
    if not all_words:
        print("Virhe: Ei sanoja käsiteltäväksi.")
        return

    slot_cache = {w: parse_slots(w) for w in set(all_words)}
    total_tokens = len(all_words)
    unique_tokens = len(slot_cache)
    print(f"\nLadattu '{filepath}': {len(lines_data):,} riviä, {total_tokens:,} sanaa ({unique_tokens:,} uniikkia).")

    # --- OSA 1: PAIKKATIETOKONTROLLOITU SEKVENSSTESTI ---
    print("\n" + "=" * 82)
    print(" 1. PAIKKATIETOKONTROLLOITU SEKVENSSTESTI (Riviasema lukittu, Within-Folio)")
    print("=" * 82)
    rng = random.Random(1337)
    modes = [
        ('prefix', 'Prefix -> Seuraava Prefix'),
        ('root', 'Ligatuuri/Ydin -> Seuraava Ligatuuri/Ydin'),
        ('infix', 'Kestoinfiksi (e/ee/eee) -> Seuraava'),
        ('suffix', 'Suffix -> Seuraava Suffix'),
        ('suf_to_pre', 'Suffix -> Seuraava Prefix (Rajan yli)')
    ]

    # Kerätään kaikki sekoitukset kerran muistiin vertailun nopeuttamiseksi
    shuffled_corpora = [position_preserving_shuffle(lines_data, rng) for _ in range(iterations)]

    best_mode = None
    best_z = -999.0

    for mode_key, label in modes:
        real_pairs = extract_adjacent_pairs(lines_data, slot_cache, mode_key)
        real_mi = calc_mi(real_pairs)
        shuf_mis = []
        for sc in shuffled_corpora:
            sp = extract_adjacent_pairs(sc, slot_cache, mode_key)
            shuf_mis.append(calc_mi(sp))
        avg_mi = sum(shuf_mis) / iterations
        std_mi = math.sqrt(sum((x - avg_mi) ** 2 for x in shuf_mis) / iterations)
        z = (real_mi - avg_mi) / (std_mi if std_mi > 0 else 1e-9)
        p_val = (sum(x >= real_mi for x in shuf_mis) + 1) / (iterations + 1)
        print(f" {label:<42} | MI: {real_mi:.5f} vs {avg_mi:.5f} | Z={z:+5.2f} | p={p_val:.4f}")
        if z > best_z:
            best_z = z
            best_mode = (mode_key, label)

    # Näytetään vahvimmat todelliset siirtymät parhaasta kerroksesta
    if best_mode:
        m_key, m_label = best_mode
        print(f"\n Vahvimmat yliodotukselliset siirtymät tasolla [{m_label}]:")
        real_c = Counter(extract_adjacent_pairs(lines_data, slot_cache, m_key))
        shuf_c = defaultdict(list)
        for sc in shuffled_corpora:
            c = Counter(extract_adjacent_pairs(sc, slot_cache, m_key))
            for k in real_c:
                shuf_c[k].append(c[k])
        ranked = []
        for k, obs in real_c.items():
            if obs < 15:
                continue
            vals = shuf_c[k]
            mu = sum(vals) / iterations
            sd = math.sqrt(sum((x - mu) ** 2 for x in vals) / iterations)
            z_k = (obs - mu) / (sd if sd > 0 else 1.0)
            ranked.append((z_k, obs, mu, k))
        ranked.sort(reverse=True)
        for z_k, obs, mu, (a, b) in ranked[:10]:
            print(f"   {a:<8} -> {b:<8} | Osuma: {obs:4d} (Sekoitus ka: {mu:5.1f}) | Z = {z_k:+5.2f}")

    # --- OSA 2: OSIOTASON JA PYSÄYTYSKODONIEN FAKTATARKISTUS ---
    print("\n" + "=" * 82)
    print(" 2. VFSF-RAKENNEVÄITTEIDEN TARKISTUS KORPUKSESTA")
    print("=" * 82)

    oror_pos = Counter()
    sec_stats = defaultdict(lambda: Counter())

    for row in lines_data:
        sec = row['section']
        words = row['words']
        n = len(words)
        for i, w in enumerate(words):
            sec_stats[sec]['TOTAL'] += 1
            if w == 'oror':
                pos = 'SINGLE' if n == 1 else ('LINE_FIRST' if i == 0 else ('LINE_LAST' if i == n - 1 else 'LINE_MID'))
                oror_pos[pos] += 1
            if w.endswith('g'):
                sec_stats[sec]['END_G'] += 1
            if 'dal' in w:
                sec_stats[sec]['DAL'] += 1
            if 'dol' in w:
                sec_stats[sec]['DOL'] += 1
            for lig in ('cth', 'ckh', 'cph', 'cfh'):
                if lig in w:
                    sec_stats[sec][lig.upper()] += 1

    print(f" 'oror' yhteensä: {sum(oror_pos.values())} kpl | Sijainnit: {dict(oror_pos)}")
    print("\n Osiojakauma (määrä ja osuus per 1 000 sanaa):")
    print(f" {'OSIO':<15} | {'SANOJA':>6} | {'-g':>4} | {'DAL':>4} | {'DOL':>4} | {'CTH':>4} | {'CKH':>4} | {'CPH':>4} | {'CFH':>4}")
    print("-" * 82)
    for sec in sorted(sec_stats.keys()):
        st = sec_stats[sec]
        tot = st['TOTAL']
        print(f" {sec:<15} | {tot:6d} | {st['END_G']:4d} | {st['DAL']:4d} | {st['DOL']:4d} | "
              f"{st['CTH']:4d} | {st['CKH']:4d} | {st['CPH']:4d} | {st['CFH']:4d}")
    print("=" * 82)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_scanner(sys.argv[1])
    else:
        print("Käyttö: python vfsf_blackbox_scanner.py <ZL3b-n.txt tai Voynich_test_source.txt>")