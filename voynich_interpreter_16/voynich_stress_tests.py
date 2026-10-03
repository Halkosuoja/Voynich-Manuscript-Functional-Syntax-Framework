# -*- coding: utf-8 -*-
"""
================================================================================
VOYNICH INTEGRATED STRESS TESTS (VFSF-1.6.2.3 — Verification Engine)
Author: Juho Laakso, Paimio (Finland)
License: Creative Commons Attribution 4.0 International (CC BY 4.0)
Category: Quantitative Vector Direction & Terminal Stop-Flag Analyzer
================================================================================
"""
import re
import os

class VoynichStressTests:
    def __init__(self, filepath):
        self.filepath = filepath
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Source file '{filepath}' not found.")

    def run_test_a_vectors(self):
        """KOE A: Laske -dal- (pumppaus ylös) vs -dol- (valuma alas) suhde osioittain."""
        print("================================================================================")
        print("STRESS TEST A: QUANTITATIVE VECTOR DIRECTION ANALYSIS (-dal- vs -dol-)")
        print("================================================================================\n")
        
        counts = {"aries": {"dal": 0, "dol": 0}, "taurus": {"dal": 0, "dol": 0}, "biomed": {"dal": 0, "dol": 0}}
        
        with open(self.filepath, "r", encoding="utf-8") as f:
            for line in f:
                line_lower = line.lower()
                # Tunnistetaan makrokonteksti sivutunnisteen perusteella
                context = "biomed"
                if "f70v1" in line_lower:
                    context = "aries"
                elif "f71v" in line_lower or "f72r1" in line_lower:
                    context = "taurus"
                elif not any(x in line_lower for x in ["f75", "f76", "f77", "f78", "f79", "f80", "f81", "f82", "f83", "f84", "f101", "f102", "f116"]):
                    continue # Skannataan vain kontrollisivut
                
                # Lasketaan juurien esiintymät puhtaasti merkkijonoina
                counts[context]["dal"] += len(re.findall(r'dal', line_lower))
                counts[context]["dol"] += len(re.findall(r'dol', line_lower))
                
        for ctx, data in counts.items():
            total = data["dal"] + data["dol"]
            dal_pct = (data["dal"] / total * 100) if total > 0 else 0
            dol_pct = (data["dol"] / total * 100) if total > 0 else 0
            print(f"CONTEXT PROFILE: {ctx.upper()}")
            print(f"  Active Upward Vector (-dal-): {data['dal']} counts ({dal_pct:.1f}%)")
            print(f"  Passive Descending Vector (-dol-): {data['dol']} counts ({dol_pct:.1f}%)")
            print("-" * 50)

    def run_test_b_flags(self):
        """KOE B: Paikallista kaikki harvinaiset -g loppuliput (Inert Residue)."""
        print("\n================================================================================")
        print("STRESS TEST B: TERMINAL STOP-FLAG LOCATOR (-g / -damg / -dlyg)")
        print("================================================================================\n")
        
        found_counter = 0
        with open(self.filepath, "r", encoding="utf-8") as f:
            for line in f:
                # Etsitään sanoja, jotka päättyvät kirjaimeen 'g' ennen erotusmerkkejä tai rivin loppua
                words = re.findall(r'\b\w+g(?=[\s\.,<$])', line.lower())
                if words:
                    clean_line = line.strip()
                    line_match = re.search(r'<[^>]+>', clean_line)
                    loc = line_match.group(0) if line_match else "<Unknown>"
                    print(f"MATCH FOUND AT {loc}: {words}")
                    print(f"  RAW LINE: {clean_line}")
                    print("-" * 80)
                    found_counter += len(words)
                    
        print(f"\nScan completed. Located {found_counter} absolute dry-waste stop flags.")

if __name__ == "__main__":
    try:
        tester = VoynichStressTests("ZL3b-n.txt")
        tester.run_test_a_vectors()
        tester.run_test_b_flags()
    except Exception as e:
        print(f"Execution Error: {e}")
