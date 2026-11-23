# Copyright (c) 2026 Juho Olavi Laakso
# SPDX-License-Identifier: MIT
"""
Voynich Manuscript Functional Syntax Framework (VFSF) - Structural Decoder
Purkaa ZL3b-n.txt-transkription sivuja ja kappaleita laajennetun VFSF-koodikirjan
mukaisiksi toiminnallisiksi tilaketjuiksi ilman foneettisia oletuksia.
"""

import re
import sys

def load_zl3b(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.readlines()
    except UnicodeDecodeError:
        with open(filepath, "r", encoding="cp1252") as f:
            return f.readlines()

def decode_word(word):
    """Purkaa yksittäisen sanan VFSF-koodikirjan mukaisiksi funktionaalisiksi atomeiksi."""
    orig = word
    tags = []

    if word in ("daiin", "dain", "daiiin"):
        med = "MED2" if "ii" in word else "MED1"
        return f"[REF:{orig}({med})]"
    if word in ("ol", "or", "al", "ar", "qol", "qor"):
        return f"[BRIDGE:{orig}]"

    rem = word
    if rem.startswith("qo"):
        tags.append("FLOW")
        rem = rem[2:]
    elif rem.startswith(("ok", "ot")):
        mode = "MODE2(ok)" if rem.startswith("ok") else "MODE1(ot)"
        tags.append(mode)
        rem = rem[2:]
    elif rem.startswith(("p", "t", "k", "f")) and len(rem) > 2:
        tags.append(f"INIT({rem.__getitem__(0)})")
        rem = rem[1:]
    elif rem.startswith(("d", "s", "y")) and len(rem) > 2:
        tags.append(f"SHIFT({rem.__getitem__(0)})")
        rem = rem[1:]
    elif rem.startswith("l") and len(rem) > 2:
        tags.append("MOD(l)")
        rem = rem[1:]

    if "eee" in rem:
        tags.append("DUR:3x")
    elif "ee" in rem:
        tags.append("DUR:2x")
    elif "e" in rem:
        tags.append("DUR:1x")

    if "iii" in rem:
        tags.append("MED:3")
    elif "ii" in rem:
        tags.append("MED:2")
    elif "i" in rem:
        tags.append("MED:1")

    if re.search(r"c(kh|th|ph|fh)", rem):
        tags.append("COMP_STRUCT")
    elif re.search(r"(ch|sh)e", rem):
        tags.append("PROC")
    elif re.search(r"(ch|sh)o", rem):
        tags.append("OBJ")
    elif re.search(r"(ch|sh)", rem):
        tags.append("ACT")

    if rem.endswith(("am", "om")):
        tags.append("END_LOCK")
    elif rem.endswith(("edy", "ody", "ady", "dy", "ey", "y")):
        tags.append("STATE_ACT")
    elif rem.endswith(("al", "ol")):
        tags.append("PARAM_A")
    elif rem.endswith(("ar", "or")):
        tags.append("PARAM_B")
    elif rem.endswith(("aiin", "ain", "in")):
        tags.append("UNIT")

    role_str = "+".join(tags) if tags else "CORE"
    return f"[{role_str}: {orig}]"
def parse_folio(lines, target_folio):
    """Poimii halutun sivun (esim. 'f1r', 'f75r', 'f71r', 'f103r', 'fRos') kaikki lokukset ja sanat."""
    target_folio = target_folio.strip().lower()
    in_folio = False
    folio_meta = ""
    records = []

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # Tunnistetaan varsinainen sivutunniste (ei pistettä lokusnumeron edessä)
        m_f = re.match(r"^<(f[a-zA-Z0-9]+)>\s*(.*)", line)
        if m_f:
            cur_f = m_f.group(1).lower()
            if cur_f == target_folio:
                in_folio = True
                folio_meta = line
            elif in_folio:
                break
            continue

        if not in_folio:
            continue

        m_loc = re.match(r"<([^>]+)>\s*(.*)", line)
        if not m_loc:
            continue
        loc_meta, text = m_loc.groups()
        parts = loc_meta.split(",")
        loc_id = parts.__getitem__(0)
        loc_tag = parts.pop(1).lstrip("@+=*&~") if len(parts) > 1 else ""

        is_para_start = "<%>" in text
        is_para_end = "<$>" in text

        text = re.sub(r"<!.*?>", "", text)
        text = re.sub(r"<.*?>", ".", text)
        text = re.sub(r"\[([^:\]]+):[^\]]+\]", r"\1", text)
        text = re.sub(r"\{[^}]+\}", "", text)
        text = re.sub(r"@\d+;", "", text)

        # Yhdistetään ','-välit VFSF-standardin mukaisesti
        text = text.replace(",", "")
        words = [w.strip(" .!?'-") for w in text.split(".") if w.strip(" .!?'-")]
        words = [w for w in words if w and not w.startswith("?")]

        if words:
            records.append({
                "loc_id": loc_id,
                "loc_tag": loc_tag,
                "is_start": is_para_start,
                "is_end": is_para_end,
                "words": words
            })

    return folio_meta, records

def find_axa_loops(words):
    """Tunnistaa rivin sisäiset A - X - A -vuorottelusilmukat."""
    loops = []
    for i in range(len(words) - 2):
        if words.__getitem__(i) == words.__getitem__(i + 2) and words.__getitem__(i) != words.__getitem__(i + 1):
            loops.append(f"{words.__getitem__(i)} - {words.__getitem__(i + 1)} - {words.__getitem__(i + 2)}")
    return loops

def decode_and_print(filepath, target_folio):
    lines = load_zl3b(filepath)
    meta, records = parse_folio(lines, target_folio)
    if not records:
        print(f"Sivua '{target_folio}' ei löytynyt tiedostosta {filepath}.")
        return

    out_lines = []
    out_lines.append("=" * 78)
    out_lines.append(f"VFSF STRUCTURAL DECODER | Folio: {target_folio}")
    out_lines.append(f"Metadata: {meta}")
    out_lines.append("=" * 78)

    all_words = [w for r in records for w in r["words"]]
    total_w = len(all_words)
    if total_w > 0:
        qo_cnt = sum(1 for w in all_words if w.startswith("qo"))
        ok_cnt = sum(1 for w in all_words if w.startswith("ok"))
        ot_cnt = sum(1 for w in all_words if w.startswith("ot"))
        ee_cnt = sum(1 for w in all_words if "ee" in w)
        e1_cnt = sum(1 for w in all_words if re.search(r"(?<!e)e(?!e)", w))
        out_lines.append(f"Sivun kokonaistilasto (N={total_w} sanaa):")
        out_lines.append(f"  - Jatkuvuusoperaattori (qo-): {qo_cnt/total_w*100:.1f} %")
        out_lines.append(f"  - Tilanvalitsimet:            MODE2(ok)={ok_cnt/total_w*100:.1f} %, MODE1(ot)={ot_cnt/total_w*100:.1f} %")
        out_lines.append(f"  - Kestosuhde ee/(e+ee):       {ee_cnt/max(1, e1_cnt+ee_cnt)*100:.1f} %")
        out_lines.append("-" * 78)

    for r in records:
        prefix = ">>> [PARA_START] " if r["is_start"] else ""
        suffix = " [PARA_END] <<<" if r["is_end"] else ""
        tag_label = f"({r['loc_tag']})"
        decoded_tokens = [decode_word(w) for w in r["words"]]
        loops = find_axa_loops(r["words"])

        out_lines.append(f"{r['loc_id']:10s} {tag_label:5s} | {prefix}{' '.join(r['words'])}{suffix}")
        out_lines.append(f"{'':16s} -> {' '.join(decoded_tokens)}")
        if loops:
            out_lines.append(f"{'':16s} ** A-X-A SILMUKKA: {', '.join(loops)} **")
        out_lines.append("")

    output_text = "\n".join(out_lines)
    print(output_text)

    safe_name = re.sub(r"[^a-zA-Z0-9_-]", "_", target_folio.strip().lower())
    out_filename = f"decoded_{safe_name}.txt"
    with open(out_filename, "w", encoding="utf-8") as f_out:
        f_out.write(output_text + "\n")
    print(f"[Tallennettu tiedostoon: {out_filename}]\n")

if __name__ == "__main__":
    filepath = "ZL3b-n.txt"
    if len(sys.argv) > 1:
        decode_and_print(filepath, sys.argv.__getitem__(1))
    else:
        print("VFSF Structural Decoder (Anna sivutunnus, esim. f1r, f75r, f103r tai 'q' lopettaaksesi)")
        while True:
            folio = input("Folio > ").strip()
            if not folio or folio.lower() in ("q", "quit", "exit"):
                break
            decode_and_print(filepath, folio)
