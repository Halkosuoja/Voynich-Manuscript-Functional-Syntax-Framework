# -*- coding: utf-8 -*-
"""
================================================================================
VOYNICH BATCH TRANSLATOR (VFSF-1.6.2 — Corpus Translation Module 2026)
Author: Juho Laakso, Paimio (Finland)
License: Creative Commons Attribution 4.0 International (CC BY 4.0)
Category: Automated Sequential Process-Chain & Latch Core Decoder
================================================================================
"""
import re
import os

class VoynichBatchTranslator:
    def __init__(self):
        # Operational Prefixes Matrix
        self.prefixes = {
            "qokch": "Intense-Force-Isolation",
            "qok": "Intense-Force/Pressure",
            "oteot": "External-Cycle-On-Inner-Rim",
            "ot": "Absolute-Time/Macrocycle",       
            "yt": "System-Runtime/Internal-Duration", 
            "te": "Iteration-Counter/Loop-Tracker",   
            "ol": "Passive-Natural-State",           
            "ch": "Controlled-Adjustment-Phase",     
            "sh": "Controlled-Adjustment-Phase",
            "pd": "Activation-Mutation",
            "p": "Initial-Activation",               
            "f": "Physical-Filtration/Purging",      
            "d": "Phase-Alteration/Conversion"       
        }
        
        # Core Process Roots Matrix
        self.roots = {
            "zepchy": "Critical-Safety-Latch/Intercept", 
            "ched": "Equilibrium/Stabilization",
            "chey": "Equilibrium/Stabilization",
            "dal": "Active-Pressure-Pumping-Upward",  
            "dol": "Free-Flow/Descending-Vector",     
            "dar": "Static-Container/Basin",         
            "cfh": "Pressurized-Discharge/Jet-Flow", 
            "cph": "Uniform-Drainage/Passive-Flow",  
            "kch": "Mechanical-Extraction/Isolation",
            "ckh": "Boundary-Setting/Gated-Valve",   
            "or": "Conduit-Conveyance/Discharge",    
            "ar": "Basal-Stratum/Concentrate-Sediment"
        }
        
        # Independent Channel States Matrix
        self.channel_states = {
            "aiin": "Pressurized-Closed-Conduit",    
            "ain": "Open-Flow-Channel",               
            "ldy": "[NODE-ANCHOR]",                   
            "dy": "[NODE-ANCHOR]",
            "chy": "[NODE-ANCHOR]",
            "am": "[CONTINUITY-LINK]"                 
        }
        
        # Terminal Code Flags Matrix
        self.flags = {
            "daiin": "[CLOSED-LOCK-COMPLETE]",        
            "saiin": "[REGULATION-LOCK-COMPLETE]",    
            "dain": "[ROUTING-LINK-FORWARD]",         
            "z": "[EMERGENCY-STOP-LATCH]",            
            "j": "[EMERGENCY-STOP-LATCH]",
            "g": "[INERT-RESIDUE/DRY-WASTE-STOP]"     
        }
        
        # Target triggers for batch capture
        self.triggers = ["oror", "zepchy", "dolchsody"]

    def clean_word(self, word):
        """Cleans specific manuscript artifacts from a token."""
        return word.lower().replace(",", "").replace(".", "").replace("?", "").replace("*", "").replace("<%>", "").replace("%", "")

    def translate_token(self, word):
        """Processes a single token through the VFSF-1.6.2 matrix layers."""
        word = self.clean_word(word)
        if not word:
            return None
            
        found_prefix = "Unassigned-Prefix"
        found_root = "Undefined-Target"
        found_channel = "Default-Flow-Matrix"
        found_flag = ""
        duration = ""
        
        # 1. Flag Intercept
        for flag in sorted(self.flags.keys(), key=len, reverse=True):
            if word.endswith(flag):
                found_flag = f" -> {self.flags[flag]}"
                word = word[:-len(flag)]
                break
                
        # 2. Channel State Extraction
        for chan in sorted(self.channel_states.keys(), key=len, reverse=True):
            if word.endswith(chan):
                found_channel = self.channel_states[chan]
                word = word[:-len(chan)]
                break
                
        # 3. Duration Infix Isolation
        if "eee" in word or "ee" in word:
            duration = "-Prolonged"
            word = word.replace("eee", "").replace("ee", "")
        elif "e" in word:
            duration = "-Continuous"
            word = word.replace("e", "")

        # 4. Operational Prefix Isolation
        for pref in sorted(self.prefixes.keys(), key=len, reverse=True):
            if word.startswith(pref):
                found_prefix = self.prefixes[pref]
                word = word[len(pref):]
                break
                
        # 5. Core Root Verification
        for root in self.roots.keys():
            if root in word or word in root and len(word) > 0:
                found_root = self.roots[root]
                break
                
        return f"[{found_prefix}{duration} -> {found_root} @ {found_channel}]{found_flag}"

    def process_line(self, line):
        """Converts raw line elements into a clean chain array."""
        # Isolate line identification token
        line_id = re.search(r'<[^>]+>', line)
        id_str = line_id.group(0) if line_id else "<Unknown Node>"
        
        # Strip structural system formatting
        line_data = re.sub(r'<[^>]+>', '', line)
        line_data = re.sub(r'#[^\n]*', '', line_data)
        line_data = line_data.replace("!", "").replace("$", "").strip()
        
        words = line_data.split(".")
        translated_tokens = []
        
        for w in words:
            trans = self.translate_token(w)
            if trans:
                translated_tokens.append(trans)
                
        if not translated_tokens:
            return None
            
        chain = " -> \n    ".join(translated_tokens)
        return f"NODE LOCATION: {id_str}\n  PROCESS CHAIN:\n    {chain}"

    def run_batch_translation(self, source_file):
        if not os.path.exists(source_file):
            print(f"ERROR: '{source_file}' not found. Place it in this folder.")
            return

        print("================================================================================")
        print("VOYNICH AUTOMATED BATCH TRANSLATOR — VFSF-1.6.2 PRODUCTION OUTPUT")
        print("Author: Juho Laakso, Paimio (Finland)")
        print("================================================================================\n")

        counter = 0
        with open(source_file, "r", encoding="utf-8") as f:
            for line in f:
                for trigger in self.triggers:
                    if trigger in line.lower():
                        output = self.process_line(line)
                        if output:
                            counter += 1
                            print(f"BATCH RECORD #{counter}")
                            print(output)
                            print("=" * 80)
                            break

if __name__ == "__main__":
    translator = VoynichBatchTranslator()
    translator.run_batch_translation("ZL3b-n.txt")
