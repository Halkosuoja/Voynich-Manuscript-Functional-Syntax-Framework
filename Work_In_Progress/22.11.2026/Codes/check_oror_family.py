#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2026 Juho Olavi Laakso
# SPDX-License-Identifier: MIT
"""
Tulostaa kaikki 'oror'-esiintymät koko ZL3b-n.txt -korpuksesta sijainteineen
ja vertaa niiden rivinloppuisuutta tekstin pohjatasoon.
"""
import re
import sys
import os
from collections import Counter


def load_lines(filepath):
    raw_lines = []
    par_id = 0
    cur_fol = "unknown"
    prev_end = True

    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
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
            has_end_tag = ('<$>' in line)
            prev_end = has_end_tag

            no_tags = re.sub(r'<[^>]+>|\{[^}]+\}|\[[^\]]+\]|@[0-9;]+', '', line).lower()
            no_tags = no_tags.replace('!', '').replace("'", "").replace("’", "").replace(',', '')
            no_tags = re.sub(r'[^a-z.\s]', ' ', no_tags)
            words = [w.strip() for w in re.split(r'[\s.]+', no_tags)
                     if w.strip() and not re.match(r'^f\d+[rv]\d*$', w.strip())]
            if words:
                raw_lines.append([cur_fol, par_id, is_par, has_end_tag, words])

    # Merkitään kappaleen viimeinen rivi myös silloin kun par_id vaihtuu seuraavalla rivillä
    for idx in range(len(raw_lines)):
        if idx == len(raw_lines) - 1 or raw_lines[idx + 1][1] != raw_lines[idx][1]:
            raw_lines[idx][3] = True
    return raw_lines


def main(filepath):
    if not os.path.exists(filepath):
        print(f"Virhe: '{filepath}' ei löydy.")
        return

    lines = load_lines(filepath)
    all_pos = Counter()
    or_end_pos = Counter()
    bare_pos = Counter()
    ext_pos = Counter()
    hits = []

    for fol, pid, is_par, is_par_end, ws in lines:
        n = len(ws)
        for i, w in enumerate(ws):
            pos = 'S' if n == 1 else ('PF' if (i == 0 and is_par) else ('LF' if i == 0 else ('LL' if i == n - 1 else 'LM')))
            par_end_mark = (is_par_end and i == n - 1)
            all_pos[pos] += 1
            if w.endswith('or'):
                or_end_pos[pos] += 1
            if 'oror' in w:
                if w == 'oror':
                    bare_pos[pos] += 1
                else:
                    ext_pos[pos] += 1
                prev_w = ws[i - 1] if i > 0 else '-'
                next_w = ws[i + 1] if i < n - 1 else '-'
                hits.append((fol, pos, 'PAR_END' if par_end_mark else '', prev_w, w, next_w))

    print("\n" + "=" * 84)
    print(f" KAIKKI 'oror'-ESIINTYMÄT KORPUKSESSA ({len(hits)} kpl)")
    print("=" * 84)
    for fol, pos, pe, pw, w, nw in hits:
        print(f"   <f{fol:<5}> | {pos:<2} {pe:<7} | {pw:<14} [{w:<14}] {nw}")

    print("\n" + "=" * 84)
    print(" SIJAINTIJAKAUMA VERTAILU (PF=kappale alku, LF=rivi alku, LM=keski, LL=rivi loppu)")
    print("=" * 84)
    for label, cnt in [
        ("Kaikki sanat (pohjataso)", all_pos),
        ("'-or'-päätteiset sanat", or_end_pos),
        ("Pelkkä 'oror'", bare_pos),
        ("Pidemmät '*oror*' sanat", ext_pos),
    ]:
        tot = sum(cnt.values())
        if tot == 0:
            continue
        s = " | ".join(f"{k}:{cnt[k]*100/tot:4.1f}%({cnt[k]})" for k in ('PF', 'LF', 'LM', 'LL', 'S'))
        print(f"   {label:<25} (N={tot:5d}): {s}")
    print("=" * 84)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Käyttö: python check_oror_family.py ZL3b-n.txt")