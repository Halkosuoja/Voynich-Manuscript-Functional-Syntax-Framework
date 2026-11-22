#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2026 Juho Olavi Laakso
# SPDX-License-Identifier: MIT
"""
Luo kontrollitekstit universal_syntax_bench.py -vertailua varten:
1) control_slot.txt (35 000 sanan Slot-generaattori)
2) control_selfcite.txt (35 000 sanan Timm-tyylinen kopioi-ja-muunna -generaattori)
3) latin_abbrev.txt (jos syötteenä annetaan .txt-latinateksti, esim. Plinius)
"""
import re
import sys
import os
import random


def abbreviate_latin_word(w):
    # Simuloi keskiajan latinankielisten käsikirjoitusten yleisimpiä aakkosellisia lyhenteitä
    w = w.lower()
    if len(w) <= 2:
        return w
    w = re.sub(r'^(prae|pro|per)', 'p', w)
    w = re.sub(r'^con', 'c', w)
    w = w.replace('qu', 'q')
    if w.endswith('que') and len(w) > 4:
        w = w[:-3] + 'q'
    elif w.endswith(('orum', 'arum', 'erum')) and len(w) > 5:
        w = w[:-3] + 'r'
    elif w.endswith('ibus') and len(w) > 5:
        w = w[:-3] + 'b'
    elif w.endswith('tur') and len(w) > 4:
        w = w[:-3] + 'tr'
    elif w.endswith(('um', 'am', 'em')) and len(w) > 3:
        w = w[:-1]  # nasaalilyhenne jättää loppukonsonantin pois
    elif w.endswith('us') and len(w) > 3:
        w = w[:-2] + 's'
    return w


def make_abbreviated_latin(in_path, out_path="latin_abbrev.txt"):
    with open(in_path, 'r', encoding='utf-8', errors='replace') as f:
        text = f.read()
    out_lines = []
    for line in text.splitlines():
        words = re.findall(r'[a-zA-Z]+', line)
        if not words:
            out_lines.append("")
            continue
        abbr = [abbreviate_latin_word(w) for w in words]
        out_lines.append(" ".join(abbr))
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(out_lines))
    print(f"Luotu lyhennetty latinatiedosto: '{out_path}'")


def gen_slot_word(rng):
    pres = ['', '', 'qo', 'ch', 'sh', 'ok', 'ot', 'da', 'o', 'y']
    cores = ['k', 't', 'p', 'f', 'ch', 'sh', 'cth', 'ckh', 'e', 'ee', 'l', 'r']
    sufs = ['dy', 'ey', 'y', 'ol', 'or', 'ar', 'al', 'aiin', 'ain', 'hy']
    return rng.choice(pres) + rng.choice(cores) + rng.choice(sufs)


def generate_slot_text(n_words=35000, out_path="control_slot.txt"):
    rng = random.Random(42)
    lines = []
    count = 0
    while count < n_words:
        par_lines = rng.randint(3, 8)
        for _ in range(par_lines):
            ln_len = rng.randint(6, 11)
            words = [gen_slot_word(rng) for _ in range(ln_len)]
            lines.append(" ".join(words))
            count += ln_len
            if count >= n_words:
                break
        lines.append("")
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
    print(f"Luotu Slot-generaattoriteksti ({count:,} sanaa): '{out_path}'")


def mutate_word(w, rng):
    chars = list(w)
    if len(chars) >= 3 and rng.random() < 0.6:
        idx = rng.randrange(len(chars))
        chars[idx] = rng.choice(['e', 'o', 'a', 'k', 't', 'c', 'h', 'l', 'r', 'y', 'd'])
        return "".join(chars)
    return gen_slot_word(rng) if rng.random() < 0.3 else w


def generate_selfcite_text(n_words=35000, out_path="control_selfcite.txt"):
    rng = random.Random(42)
    stream = [gen_slot_word(rng) for _ in range(120)]
    while len(stream) < n_words:
        if rng.random() < 0.85:
            src = stream[-rng.randint(1, min(100, len(stream)))]
            w = mutate_word(src, rng) if rng.random() < 0.50 else src
        else:
            w = gen_slot_word(rng)
        stream.append(w)

    lines = []
    idx = 0
    while idx < n_words:
        par_lines = rng.randint(3, 8)
        for _ in range(par_lines):
            ln_len = rng.randint(6, 11)
            lines.append(" ".join(stream[idx:idx + ln_len]))
            idx += ln_len
            if idx >= n_words:
                break
        lines.append("")
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
    print(f"Luotu Self-citation-generaattoriteksti ({n_words:,} sanaa): '{out_path}'")


if __name__ == "__main__":
    generate_slot_text()
    generate_selfcite_text()
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        make_abbreviated_latin(sys.argv[1])