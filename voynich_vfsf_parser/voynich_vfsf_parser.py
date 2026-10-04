#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Voynich Manuscript Process-Control Translator (VFSF-1.6.13 Patch)
Author: Juho Olavi Laakso (Paimio, Finland)
License: Creative Commons Attribution 4.0 International (CC BY 4.0)

Patch Note: Refactored core parsing architecture to evaluate Prefix, Duration,
CoreRoot, and Suffix parameters entirely independently from the stable cleaned string.
This prevents structural tracking flags from causing Undefined-Target drops.
"""

import re

class VoynichVFSFParser:
    def __init__(self):
        self.prefixes = {
            'p': 'INITIALIZATION [Activate Channel/Pipeline]',
            'f': 'FILTRATION [Purge Particulate Matter]',
            'd': 'PHASE-ALTERATION [State Transition/Condensation]',
            'sh': 'CONTROLLED-REGULATION [Adjust Flow/Valve State]',
            'ch': 'CONTROLLED-REGULATION [Adjust Flow/Valve State]'
        }
        
        self.roots = {
            'kch': 'MECHANICAL-EXTRACTION [Physical Maceration/Expression]',
            'ky': 'MECHANICAL-EXTRACTION [Physical Maceration/Expression]',
            'cth': 'THERMAL-INFUSION [Caloric Alembic Processing]',
            'otey': 'EXTERNAL-BATCH-TIMER [Chronological Cycle Clock]',
            'tod': 'EXECUTION-DELAY [Localized Settling/Wait Cycle]',
            'tody': 'EXECUTION-DELAY [Localized Settling/Wait Cycle]',
            'sheo': 'PRESSURE-RELEASE [Gated Vent Hold to Stabilize Velocity]',
            'cfh': 'PRESSURIZED-DISCHARGE [Jet-Flow Nozzle Injection]',
            'ckhh': 'PRESSURIZED-DISCHARGE [Jet-Flow Nozzle Injection]',
            'okor': 'MAIN-CONDUIT-ROUTING [Manifold Distribution Network]',
            'korol': 'MAIN-CONDUIT-ROUTING [Manifold Distribution Network]',
            'qokdal': 'FORCED-UPWARD-INJECTION [High-Pressure Velocity Line Boost]',
            'qokal': 'FORCED-UPWARD-INJECTION [High-Pressure Velocity Line Boost]',
            'qokaly': 'FORCED-UPWARD-INJECTION [High-Pressure Velocity Line Boost]',
            'ar': 'BASAL-STRATUM [High-Density Sediment Settling]',
            'orom': 'BASAL-STRATUM [High-Density Sediment Settling]',
            'ol': 'GRAVITY-DRIVEN-FREE-FLOW [Non-Pressurized Open Discharge]',
            'okol': 'GRAVITY-DRIVEN-FREE-FLOW [Non-Pressurized Open Discharge]',
            'dair': 'STATIC-CONTAINER [Primary Collecting Basin/Vessel]',
            'dar': 'STATIC-CONTAINER [Primary Collecting Basin/Vessel]',
            'dal': 'ACTIVE-UPWARD-HYDROSTATIC-VECTOR [Pressurized Pumping]',
            'dol': 'PASSIVE-DESCENDING-VECTOR [Gravity Drainage Loop]'
        }
        
        self.suffixes = {
            'dain': 'ROUTING-LINK-FORWARD [Conduit Interface Switch]',
            'saiin': 'CLOSED-LOCK-COMPLETE [System Stabilization Reached]',
            'aiin': 'CLOSED-MATRIX [Enclosed High-Intensity Pipeline]'
        }

    def clean_token(self, token):
        """Pre-scrubs raw string inputs to isolate valid grapheme sequences."""
        token = token.lower().strip()
        token = re.sub(r'<[^>]+>', '', token)
        token = re.sub(r'\{[^}]+\}', '', token)
        if '[' in token:
            token = re.sub(r'\[([a-z0-9]+):[a-z0-9]+\]', r'\1', token)
        return re.sub(r'[^a-z]', '', token)

    def parse_token(self, token):
        cleaned = self.clean_token(token)
        if not cleaned:
            return None
            
        result = {
            'token': token.strip(),
            'prefix': 'Default-Flow-Matrix',
            'duration': 'Standard-Duration',
            'root': 'Undefined-Target',
            'suffix': 'Standard-Termination'
        }
        
        # 1. PARSE PREFIX (Evaluated directly from start)
        for pref, desc in self.prefixes.items():
            if cleaned.startswith(pref):
                result['prefix'] = desc
                break

        # 2. PARSE CORE PROCESS ROOTS (Evaluated independently)
        for rt, desc in self.roots.items():
            if rt in cleaned:
                result['root'] = desc
                break

        # 3. PARSE SUFFIXES, BUS ROUTERS AND STOP FLAGS
        suffix_matched = False
        for suf, desc in self.suffixes.items():
            if cleaned.endswith(suf):
                result['suffix'] = desc
                suffix_matched = True
                break
                
        if not suffix_matched:
            if cleaned.endswith('g'):
                result['suffix'] = 'SYSTEM-SHUTDOWN [Inert Solid Residue Stop Flag]'
            elif cleaned.endswith('amam') or cleaned.endswith('am'):
                result['suffix'] = 'SEQUENTIAL-CONTINUITY-LINK [Direct Pointer to Next Node]'

        # 4. PARSE INFIX DURATION MULTIPLIERS
        duration_count = cleaned.count('e') + cleaned.count('o')
        if duration_count >= 2:
            result['duration'] = f'Prolonged-Duration (Coefficient: x{duration_count})'

        return result

    def translate_line(self, line):
        clean_line = re.sub(r'<[^>]+>', '', line).strip()
        tokens = re.split(r'[.,\s]+', clean_line)
        parsed_chain = []
        
        for t in tokens:
            if t.strip():
                parsed = self.parse_token(t)
                if parsed:
                    parsed_chain.append(parsed)
                
        return parsed_chain

if __name__ == '__main__':
    parser = VoynichVFSFParser()
    print("=" * 80)
    print("VOYNICH MANUSCRIPT PROCESS-CONTROL TRANSLATOR (VFSF-1.6.13 Engine)")
    print("Author: Juho Olavi Laakso (Paimio, Finland)")
    print("License: Creative Commons Attribution 4.0 International (CC BY 4.0)")
    print("=" * 80)
    
    while True:
        user_input = input("\nEnter Voynich/EVA code line: ")
        if user_input.lower().strip() == 'exit':
            break
        chain = parser.translate_line(user_input)
        print("\n--- DECRYPTED FINITE-STATE MACHINE SEQUENCE ---")
        for i, node in enumerate(chain, 1):
            print(f"\n[NODE #{i}] -> Source Token: '{node['token']}'")
            print(f"  ├─ Prefix:   {node['prefix']}")
            print(f"  ├─ Infix:    {node['duration']}")
            print(f"  ├─ CoreRoot: {node['root']}")
            print(f"  └─ Suffix:   {node['suffix']}")
