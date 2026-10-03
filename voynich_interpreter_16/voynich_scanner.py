# -*- coding: utf-8 -*-
"""
================================================================================
VOYNICH CORPUS SCANNER (VFSF-1.6.1 — Statistical Anomaly Finder 2026)
Author: Juho Laakso, Paimio (Finland)
License: Creative Commons Attribution 4.0 International (CC BY 4.0)
Category: Automated Anomaly & Pipeline Target Locator
================================================================================
"""
import re
import os

class VoynichCorpusScanner:
    def __init__(self):
        # Definoitut avainkomponentit hakuja varten
        self.targets = ["oror", "zepchy", "dolchsody"]

    def scan_file(self, filename):
        if not os.path.exists(filename):
            print(f"ERROR: File '{filename}' not found in the current directory.")
            print("Please place the 'ZL3b-n.txt' file in the same folder as this script.")
            return

        print("================================================================================")
        print("VOYNICH CORPUS SCANNER — FEATURE EXTRACTION REPORT")
        print("Author: Juho Laakso, Paimio (Finland)")
        print("================================================================================\n")

        found_count = 0
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                # Etsitään tiedostosta ne rivit, jotka sisältävät hakusanamme
                for target in self.targets:
                    if target in line.lower():
                        # Puhdistetaan rivi tulostusta varten
                        clean_line = line.strip()
                        print(f"FOUND TARGET [{target.upper()}] AT LINE:")
                        print(f"  {clean_line}")
                        print("-" * 80)
                        found_count += 1
                        
        print(f"\nScan completed. Total of {found_count} system components located.")

if __name__ == "__main__":
    scanner = VoynichCorpusScanner()
    # Ajetaan skannaus antamaasi aineistoon
    scanner.scan_file("ZL3b-n.txt")
