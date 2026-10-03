# -*- coding: utf-8 -*-
"""
================================================================================
VOYNICH SYNTAX MATRIX INTERPRETER (VFSF-1.6 — Expanded State Machine 2026)
Author: Juho Laakso, Paimio (Finland)
License: Creative Commons Attribution 4.0 International (CC BY 4.0)
Category: Pure Rule-Based Ideographic Process Flow & Security Latch Analyzer
================================================================================
"""
import re

class VoynichSyntaxMatrix16:
    def __init__(self):
        # A. OPERATIONAL PREFIXES (How / Quality / Chronological Boundary)
        self.prefixes = {
            "qokch": "Intense-Force-Isolation",
            "qok": "Intense-Force/Pressure",
            "oteot": "External-Cycle-On-Inner-Rim",
            "ot": "Absolute-Time/Macrocycle",       # Calendar / Natural extraction boundary
            "yt": "System-Runtime/Internal-Duration", # Execution duration since initialization
            "te": "Iteration-Counter/Loop-Tracker",   # Numerical loop/cycle count
            "ol": "Passive-Natural-State",           # Medium moves/acts under its own gravity
            "ch": "Controlled-Adjustment-Phase",     # Operator-driven manual adjustment
            "sh": "Controlled-Adjustment-Phase",
            "pd": "Activation-Mutation",
            "p": "Initial-Activation",               # Command to activate pipeline/channel
            "f": "Physical-Filtration/Purging",      # Mechanical separation of spent matter
            "d": "Phase-Alteration/Conversion"       # State shift bridge (e.g., condensation)
        }
        
        # B. CORE PROCESS ROOTS (What / System Component)
        self.roots = {
            "zepchy": "Critical-Safety-Latch/Intercept", # Threat, toxicity or critical boiling point stop
            "ched": "Equilibrium/Stabilization",
            "chey": "Equilibrium/Stabilization",
            "dal": "Active-Pressure-Pumping-Upward",  # Force-driven upward movement (sap ascent)
            "dol": "Free-Flow/Descending-Vector",     # Gravity-driven fluid descent
            "dar": "Static-Container/Basin",         # Vat, barrel, stem jacket or solid repository
            "cfh": "Pressurized-Discharge/Jet-Flow", # Active fluid emission via a narrow nozzle
            "cph": "Uniform-Drainage/Passive-Flow",  # Passive drainage without additional pressure
            "kch": "Mechanical-Extraction/Isolation",# Extracting the target medium from solid matter
            "ckh": "Boundary-Setting/Gated-Valve",   # Throttling valve or internal system restriction
            "or": "Conduit-Conveyance/Discharge",    # Physical movement of matter along a path
            "ar": "Basal-Stratum/Concentrate-Sediment"# Solid residue under fluid level / cycle baseline
        }
        
        # C. INDEPENDENT CHANNEL STATES (Where / Physical Substrate Environment)
        self.channel_states = {
            "aiin": "Pressurized-Closed-Conduit",    # Enclosed/high-intensity specialized pipeline
            "ain": "Open-Flow-Channel",               # Low-pressure free conduit / tapping gutter
            "ldy": "[NODE-ANCHOR]",                   # Firmly tied to this physical connection point
            "dy": "[NODE-ANCHOR]",
            "chy": "[NODE-ANCHOR]",
            "am": "[CONTINUITY-LINK]"                 # Sequentially chained into the subsequent token
        }
        
        # D. TERMINAL CODELOCKS & FLAGS (Absolute System Flags)
        self.flags = {
            "daiin": "[CLOSED-LOCK-COMPLETE]",        # Enclosed phase successfully completed (return 0)
            "saiin": "[REGULATION-LOCK-COMPLETE]",    # Stabilization phase successfully reached and locked
            "dain": "[ROUTING-LINK-FORWARD]",         # Pass open phase output down the pipeline path
            "z": "[EMERGENCY-STOP-LATCH]",            # Mechanical lock/valve intercept at discharge port
            "j": "[EMERGENCY-STOP-LATCH]",
            "g": "[INERT-RESIDUE/DRY-WASTE-STOP]"     # Final spent dry matter / fluidless system halt
        }

    def clean_line(self, line):
        """Cleans headers, layout commentary and page tags from the raw transcript string."""
        line = re.sub(r'<[^>]+>', '', line)       # Removes identifiers like <f70v1.1>
        line = re.sub(r'#[^\n]*', '', line)        # Removes internal transcript comments
        line = line.replace("!", "").replace("$", "")
        return line.strip()

    def translate_word_matrix(self, word):
        """Executes a pure, modular VFSF-1.6 matrix breakdown for a single token."""
        # Clean specific punctuation artifacts for mechanical processing
        word = word.lower().replace(",", "").replace(".", "").replace("?", "").replace("*", "")
        if not word or word == "<%>" or word == "%":
            return None
            
        found_prefix = "Undefined-Prefix"
        found_root = "Undefined-Target"
        found_channel = "Default-Flow-Matrix"
        found_flag = ""
        duration = ""
        
        # 1. Absolute Code Flag Intercept from the terminal end
        for flag in sorted(self.flags.keys(), key=len, reverse=True):
            if word.endswith(flag):
                found_flag = f" -> {self.flags[flag]}"
                word = word[:-len(flag)]
                break
                
        # 2. Independent Channel State Extraction from the terminal end
        for chan in sorted(self.channel_states.keys(), key=len, reverse=True):
            if word.endswith(chan):
                found_channel = self.channel_states[chan]
                word = word[:-len(chan)]
                break
                
        # 3. Infix Duration Extender Multiplier Isolation
        if "eee" in word or "ee" in word:
            duration = "-Prolonged"
            word = word.replace("eee", "").replace("ee", "")
        elif "e" in word:
            duration = "-Continuous"
            word = word.replace("e", "")

        # 4. Operational Prefix Isolation from the front
        for pref in sorted(self.prefixes.keys(), key=len, reverse=True):
            if word.startswith(pref):
                found_prefix = self.prefixes[pref]
                word = word[len(pref):]
                break
                
        # 5. Core Process Root Identification from the core
        for root in self.roots.keys():
            if root in word or word in root and len(word) > 0:
                found_root = self.roots[root]
                break
                
        return f"[{found_prefix}{duration} -> {found_root} @ {found_channel}]{found_flag}"

    def translate_line(self, raw_line):
        """Decomposes a full transcript line into a logical mechanical sequence array."""
        cleaned = self.clean_line(raw_line)
        if not cleaned:
            return None
            
        # Voynich tokens are strictly split by period punctuation delimiters
        words = cleaned.split(".")
        translated_words = []
        
        for w in words:
            translated = self.translate_word_matrix(w)
            if translated:
                translated_words.append(translated)
                
        if not translated_words:
            return None
            
        return " -> \n  ".join(translated_words)

# === EMPIRICAL VALIDATION EXECUTION ENGINE ===
if __name__ == "__main__":
    interpreter = VoynichSyntaxMatrix16()

    test_lines = [
        # 1. Aries Sequence f70v1.1 - Hydrostatic sap-tapping pressure initiation
        "<f70v1.1> dalalody.oteoshey.okoksheo.shokey",
        
        # 2. Taurus Sequence f71v.1 - Fluid batch-finalization and basin-sediment tracking
        "<f71v.1> oteeodaiin.she.ateey.dain.oteokeey",
        
        # 3. Distillation Cycle f102r1.13 - Continuous operational extraction loop
        "<f102r1.13> teesody.qoeol.olcheor.qokey",
        
        # 4. High-Anomaly Control (Hapax Legomena on Schematic Volvelle Rim f67r2.29)
        "<f67r2.29> dolchsody",
        
        # 5. Absolute Final Voynich String f116v.1 - System Shutdown Command
        "<f116v.1> oror.sheey"
    ]

    print("================================================================================")
    print("VOYNICH SYNTAX MATRIX INTERPRETER — VERSION 1.6 REGRESSION LOGS")
    print("Copyright & Intellectual Priority: Juho Laakso, Paimio (Finland)")
    print("================================================================================\n")
    
    for line in test_lines:
        print(f"RAW TRANSCRIPT ENTRY:\n  {line}")
        translation = interpreter.translate_line(line)
        if translation:
            print(f"MECHANICAL PROCESS FLOW ARRAY:\n  {translation}")
        print("-" * 80)
