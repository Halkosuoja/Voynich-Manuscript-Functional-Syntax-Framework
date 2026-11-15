#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===================================================================================
THE VFSF GLOBAL STRESS TESTER v3.8.2 (The Isomorphic Master Core)
===================================================================================
Tekijä: Juho Olavi Laakso (Paimio, Finland)
Konteksti: Voynich Manuscript Functional Syntax Framework (VFSF)
Lisenssi: MIT License (Copyright (c) 2026 Juho Olavi Laakso)
Päivitykset v3.8.2:
  - Harmonisoitu laajennettu ydinmorfeemisto (or, kair, sheky, sory, res, dan)
  - Korjattu Smart Auto-Init lataamaan täysi nestemassa V=4 kuivakäynnin estämiseksi
  - Palautettu joustava sumea kaskadiuomien halkaisija UNKNOWN-kohinan minimoimiseksi
===================================================================================
"""
import re
import sys
import os
import random
from collections import defaultdict

# =================================================================================
# GLOBAALI HARDWARE-REKISTERI JA LAITETAGIT (Järjestetty pituuden mukaan)
# =================================================================================
MATRIX_MAP_ORDERED = [
    # 1. Monimutkaiset korkeapaine- ja erikoislohkot (6-7 merkkiä)
    ('qokchain', 'FORCED_OPEN_CHANNEL_FLUSH'),
    ('qokchedy', 'PRESSURIZED_CALIBRATION'),
    ('qokchdy', 'PRESSURIZED_CALIBRATION'),
    ('qokch', 'PRESSURIZED_CALIBRATION'),
    ('qokain', 'FORCED_OPEN_CHANNEL_FLUSH'),
    ('qotal', 'PRESSURE_BOOST_THROTTLE'),
    ('qokor', 'FORCED_EVACUATION_CYCLE'),
    ('qokedy', 'PRESSURIZED_CALIBRATION'),
    ('ckhhey', 'CHECK_VALVE_ISOLATION'),
    ('chcthy', 'VALVE_CALIBRATION'),
    ('cholchiky', 'VALVE_CALIBRATION'),
    ('sheteal', 'SYSTEM_REBOOT'),
    ('shekey', 'SYSTEM_REBOOT'),
    ('fachys', 'MECHANICAL_FILTER'),
    ('syaiir', 'SYSTEM_REBOOT'),
    ('cthardan', 'REFRACTORY_RESTART'),

    # 2. Piktografiset Gallows-ligatuurit ja toimilaitteet (Slot 4)
    ('qokkey', 'HIGH_PRESSURE_OVERRIDE'),
    ('qokey', 'HIGH_PRESSURE_OVERRIDE'),
    ('qok', 'HIGH_PRESSURE_OVERRIDE'),
    ('qot', 'PRESSURE_BOOST_THROTTLE'),
    ('qop', 'INIT_ACTIVATION'),
    ('qof', 'FORCED_EVACUATION_CYCLE'),
    ('qol', 'BYPASS_FREE_FLOW'),
    ('pched', 'INIT_ACTIVATION'),
    ('oteog', 'BATCH_SHUTDOWN'),
    ('daiin', 'COMPLETED_LOCK_HALT'),

    # 3. Säiliöt ja allasvaraukset (Nostavat REG V -tasoa)
    ('dair', 'CONTAINMENT_RECEPTACLE'),
    ('dar', 'CONTAINMENT_RECEPTACLE'),

    # 4. Aktiiviset siirtovektorit, uutot ja stabiloinnit
    ('dal', 'ACTIVE_UPWARD_VECTOR'),
    ('dol', 'GRAVITY_DRAIN_DOWN'),
    ('cfh', 'JET_FLOW_DISCHARGE'),
    ('cph', 'PASSIVE_CROSS_FLOW'),
    ('cthy', 'THERMAL_INFUSION'),
    ('cthey', 'THERMAL_INFUSION'),
    ('chedy', 'FLUID_STABILIZATION'),
    ('ched', 'FLUID_STABILIZATION'),
    ('chey', 'FLUID_STABILIZATION'),
    ('chol', 'FLUID_STABILIZATION'),
    ('chor', 'KINETIC_CONDUIT'),

    # 5. Järjestelmäohjaukset, säädöt ja paluuvirtaukset
    ('sheky', 'SYSTEM_REBOOT'),
    ('shedy', 'SYSTEM_REBOOT'),
    ('sholdy', 'SYSTEM_REBOOT'),
    ('shol', 'SYSTEM_REBOOT'),
    ('shory', 'SYSTEM_REBOOT'),
    ('shor', 'SYSTEM_REBOOT'),
    ('shdy', 'SYSTEM_REBOOT'),
    ('sory', 'SYSTEM_REBOOT'),
    ('sor', 'SYSTEM_REBOOT'),
    ('kair', 'CONDUIT_DISCHARGE'),
    ('ckhar', 'REFRACTORY_RESTART'),
    ('cthar', 'REFRACTORY_RESTART'),
    ('okor', 'REFRACTORY_RESTART'),
    ('okaiir', 'REFRACTORY_RESTART'),
    ('kor', 'CONDUIT_DISCHARGE'),
    ('dain', 'OPEN_LOW_PRESSURE_LINE'),
    ('dan', 'OPEN_LOW_PRESSURE_LINE'),
    ('chly', 'VALVE_CALIBRATION'),
    ('chal', 'VALVE_CALIBRATION'),
    ('oror', 'FINAL_SYSTEM_EVACUATION'),
    ('res', 'THERMAL_INFUSION'),
    ('ase', 'SYSTEM_REBOOT'),
    ('ar', 'SEDIMENT_SETTLING'),
    ('al', 'ACTIVE_UPWARD_VECTOR'),
    ('aiin', 'CLOSED_HIGH_PRESSURE_LINE'),
    ('ain', 'OPEN_LOW_PRESSURE_LINE'),
    ('am', 'CONTINUOUS_SEQUENCE_LINK'),
    ('ol', 'BYPASS_FREE_FLOW'),
    ('or', 'KINETIC_CONDUIT'),
    ('ckh', 'CHECK_VALVE_ISOLATION'),
    ('pd', 'INIT_ACTIVATION'),
('ch', 'CHANNEL_ADDRESS_HOLD'),
('sh', 'SYSTEM_REBOOT'),
('ot', 'GRAVITY_FEED_HOLD'),
    ('ok', 'CHANNEL_ADDRESS_HOLD'),
    ('sy', 'SYSTEM_REBOOT'),
    ('so', 'SYSTEM_REBOOT'),
    ('cth', 'THERMAL_INFUSION'),
    ('qo', 'GRAVITY_FEED_HOLD'),
    ('ky', 'CHANNEL_ADDRESS_HOLD'),
    ('dy', 'CHANNEL_ADDRESS_HOLD'),
    ('do', 'PHASE_CONVERSION_HOLD'),
    ('sa', 'SYSTEM_REBOOT'),

    # 6. Yksittäiset toimilaitteet (Täsmähaku: VAIN jos len(key) == 1 ja token == key)
    ('k', 'CHECK_VALVE_ISOLATION'),
    ('t', 'VALVE_CALIBRATION'),
    ('p', 'INIT_ACTIVATION'),
    ('f', 'CHECK_VALVE_ISOLATION'),
    ('s', 'SYSTEM_REBOOT'),
    ('r', 'REFRACTORY_RESTART'),
    ('d', 'PHASE_CONVERSION_HOLD'),
    ('o', 'GRAVITY_FEED_HOLD'),
    ('y', 'CHANNEL_ADDRESS_HOLD'),
    ('l', 'OPEN_OUTLET_DRAIN'),
    ('n', 'TERMINAL_RESTRICTOR'),
    ('g', 'INERT_WASTE_FLAG')
]

SPLITTABLE_STEMS = [
    'qokch', 'qokain', 'qotal', 'qokor', 'qok', 'qot', 'qop', 'qof', 'qol',
    'cthy', 'daiin', 'dain', 'chol', 'shol', 'dal', 'dol', 'dar', 'dair', 
    'oror', 'ckhy', 'ched', 'chey', 'kair', 'dan', 'cho'
]

GALLOWS_PIVOTS = ['k', 't', 'p', 'f']
MAX_HIGH_PRESSURE_DURATION = 4
MAX_IDLE_STREAK = 15
# =================================================================================
# PUHDISTUS JA JÄSENNYS (SUMEA KASKADIHALKAISU)
# =================================================================================

def clean_and_extract_tokens(raw_line):
    """ Suorittaa raakadatalle tiukan mekaanisen esipuhdistuksen """
    line_str = raw_line.strip()
    if not line_str or line_str.startswith('#'): return [], None
    
    locus_match = re.search(r'<f(\d+[rv])', line_str.lower())
    current_folio = locus_match.group(1) if locus_match else None
    
    clean_text = re.sub(r'<[^>]+>', '', line_str)
    clean_text = re.sub(r'\{[^}]+\}', '', clean_text)
    clean_text = re.sub(r'\[[^\]]+\]', '', clean_text)
    clean_text = re.sub(r'@[0-9;]+', '', clean_text)
    clean_text = clean_text.replace("'", "").replace("’", "")
    clean_text = re.sub(r'[{}\[\]!@%<>?:*#$,=+\-]', ' ', clean_text)
    
    raw_tokens = [t.strip().lower() for t in re.split(r'[\s.]+', clean_text) if t]
    filtered_tokens = [t for t in raw_tokens if not re.match(r'^f\d+[rv]$', t)]
    return filtered_tokens, current_folio

def parse_token(token):
    """ Jäsentää tokenit laitetagoiksi estäen 1-merkkiset alimerkkijonoansat """
    if token == "oror": return 'FINAL_SYSTEM_EVACUATION'
    if token == "qokey" or token == "qokkey": return 'HIGH_PRESSURE_OVERRIDE'
    
    for key, tag in MATRIX_MAP_ORDERED:
        if len(key) == 1:
            if token == key: 
                return tag
        else:
            if key == token or key in token: 
                return tag
    return "UNKNOWN"

def tokenize_and_split_with_multiplier(token):
    """ Erottaa dynaamiset aikaviiveet ja suorittaa sumean kaskadihalkaisun """
    cleaned = token.lower()
    multiplier = 1
    
    if 'eee' in cleaned:
        multiplier = 3
        cleaned = cleaned.replace('eee', '', 1)
    elif 'ee' in cleaned:
        multiplier = 2
        cleaned = cleaned.replace('ee', '', 1)
        
    if parse_token(cleaned) != "UNKNOWN":
        return [(cleaned, multiplier)]
        
    # --- PROSESSIOHJATTU GALLOWS PIVOT -HALKAISU ---
    for pivot in GALLOWS_PIVOTS:
        if pivot in cleaned and len(cleaned) > 2:
            idx = cleaned.find(pivot)
            part1, part2 = cleaned[:idx], cleaned[idx:]
            sub_tokens = []
            if part1 and parse_token(part1) != "UNKNOWN": 
                sub_tokens.append((part1, 1))
            if part2 and parse_token(part2) != "UNKNOWN": 
                sub_tokens.append((part2, multiplier))
            if len(sub_tokens) >= 2: 
                return sub_tokens
                
    # --- VARALINJA: AGGLUTINOITUNEET JÄRJESTELMÄVARRET ---
    for stem in SPLITTABLE_STEMS:
        if stem in cleaned and len(cleaned) > len(stem):
            idx = cleaned.find(stem)
            if idx == 0:
                part1 = cleaned[:len(stem)]
                part2 = cleaned[len(stem):]
            else:
                part1 = cleaned[:idx]
                part2 = cleaned[idx:]
                
            sub_tokens = []
            if part1 and parse_token(part1) != "UNKNOWN": 
                sub_tokens.append((part1, 1))
            if part2 and parse_token(part2) != "UNKNOWN": 
                sub_tokens.append((part2, multiplier))
                
            if len(sub_tokens) >= 2 or (sub_tokens and len(sub_tokens[0][0]) < len(cleaned)):
                return sub_tokens
            
    return [(cleaned, multiplier)]
# =================================================================================
# FYSIIKKAMOOTTORI JA SIVUNSISÄINEN MONTE CARLO (VERIFIOITU MASTER CORE)
# =================================================================================

def run_simulation_engine(tokens_with_locus, generate_logs=False):
    """
    Ajaa tekstivirran dynaamisen osatila-automaatin läpi.
    Valvoo nestetaseita, ylipainerasituksia ja latensseja askel askeleelta.
    """
    system_initialized = False
    vessel_fluid_units = 0
    pressure_state = "IDLE"
    logical_contradictions = 0
    step = 0
    high_pressure_duration = 0
    idle_streak = 0
    log_lines = []
    last_folio = None
    
    for raw_token, folio in tokens_with_locus:
        sub_tokens = tokenize_and_split_with_multiplier(raw_token)
        
        for token, multiplier in sub_tokens:
            step += 1
            
            # --- LOHKORESETOINTI SIVUN VAIHTUESSA ---
            if folio and last_folio and folio != last_folio:
                system_initialized, vessel_fluid_units, pressure_state, high_pressure_duration, idle_streak = False, 0, "IDLE", 0, 0
                if generate_logs:
                    log_lines.append(f"Askel {step:05d} | {'[FOLIO_SWITCH]':<15} | {'BLOCK_RESET':<26} | {'0':<4} | {'IDLE':<12} | INFO: Sivu vaihtunut <f{folio}>. Rekisterit nollattu.")
            if folio: last_folio = folio
                
            tag = parse_token(token)
            
            if tag == "UNKNOWN":
                if generate_logs:
                    log_lines.append(f"Askel {step:05d} | {token:<15} | {'UNKNOWN':<26} | {'-':<4} | {'-':<12} | Varoitus: Tuntematon operaattori.")
                continue
                
            error_msg = ""
            is_error_step = False
            
            # 1. Eksplisiittiset master-herättäjät
            if token in ["tsheos", "potchokor", "osar", "daiin", "fachys"]:
                system_initialized, vessel_fluid_units, high_pressure_duration, idle_streak = True, 4, 0, 0
                pressure_state = "LOW_PRESSURE" if pressure_state == "IDLE" else pressure_state
                if generate_logs:
                    log_lines.append(f"Askel {step:05d} | {token:<15} | {tag:<26} | {vessel_fluid_units:<4} | {pressure_state:<12} | MASTER_HERÄTYS: Puskuri V=4 asetettu.")
                continue

            # 2. ÄLYKÄS AUTO-INIT PROTOKOLLA
            if not system_initialized:
                if tag in ['CONTAINMENT_RECEPTACLE', 'SEDIMENT_SETTLING', 'BYPASS_FREE_FLOW', 'OPEN_LOW_PRESSURE_LINE', 'INIT_ACTIVATION', 'SYSTEM_REBOOT', 'CHANNEL_ADDRESS_HOLD', 'GRAVITY_FEED_HOLD', 'PHASE_CONVERSION_HOLD']:
                    system_initialized = True
                    pressure_state = "LOW_PRESSURE"
                    vessel_fluid_units = 4
                    idle_streak = 0
                    if generate_logs:
                        log_lines.append(f"Askel {step:05d} | {token:<15} | {tag:<26} | {vessel_fluid_units:<4} | {pressure_state:<12} | AUTO_INIT: Linjasto herätetty syöttötilasta (V=4).")
                    continue
                else:
                    logical_contradictions += 1
                    if generate_logs:
                        log_lines.append(f"Askel {step:05d} | {token:<15} | {tag:<26} | {'-':<4} | {pressure_state:<12} | RISTIRIITA: Komento ennen herätystä!")
                    continue

            current_hold_latency = multiplier
            
            # 3. Dynaamiset siirtymäsäännöt ja ainetaseet (Mass Balance)
            if tag in ['INIT_ACTIVATION', 'SYSTEM_REBOOT', 'VALVE_CALIBRATION', 'SEDIMENT_SETTLING']:
                system_initialized = True
                if pressure_state == "IDLE": pressure_state = "LOW_PRESSURE"
                if tag in ['SYSTEM_REBOOT', 'SEDIMENT_SETTLING']:
                    idle_streak += current_hold_latency
                    if idle_streak > MAX_IDLE_STREAK: 
                        logical_contradictions, error_msg, is_error_step = logical_contradictions + 1, " [Joutokäyntiviive ylittynyt!]", True
                else: 
                    idle_streak = 0
                
            elif tag in ['CHANNEL_ADDRESS_HOLD', 'PHASE_CONVERSION_HOLD', 'GRAVITY_FEED_HOLD', 'TERMINAL_RESTRICTOR', 'OPEN_OUTLET_DRAIN']:
                if pressure_state == "IDLE": pressure_state = "LOW_PRESSURE"
                idle_streak += current_hold_latency
                if idle_streak > MAX_IDLE_STREAK:
                    logical_contradictions, error_msg, is_error_step = logical_contradictions + 1, " [Joutokäyntiviive ylittynyt!]", True
                
            elif tag == 'CONTAINMENT_RECEPTACLE': 
                vessel_fluid_units, idle_streak = vessel_fluid_units + (2 * current_hold_latency), 0
                
            elif tag in ['HYDROSTATIC_PUMP_UP', 'PRESSURE_BOOST_THROTTLE', 'PRESSURIZED_CALIBRATION', 'CLOSED_HIGH_PRESSURE_LINE', 'HIGH_PRESSURE_OVERRIDE', 'ACTIVE_UPWARD_VECTOR', 'CHECK_VALVE_ISOLATION']:
                if vessel_fluid_units <= 0: 
                    logical_contradictions, error_msg, is_error_step = logical_contradictions + 1, " [Kuivapumppaus ilman nestesyöttöä!]", True
                pressure_state = "HIGH_PRESSURE"
                vessel_fluid_units = max(0, vessel_fluid_units - current_hold_latency)
                idle_streak = 0
                high_pressure_duration += current_hold_latency
                if high_pressure_duration > MAX_HIGH_PRESSURE_DURATION: 
                    logical_contradictions, error_msg, is_error_step = logical_contradictions + 1, error_msg + " [Putkiston ylipainerasitus!]", True
                    
            elif tag == 'THERMAL_INFUSION':
                if vessel_fluid_units <= 0 and pressure_state == "HIGH_PRESSURE": 
                    logical_contradictions, error_msg, is_error_step = logical_contradictions + 1, " [Tyhjän reaktorin kuivakeitto!]", True
                pressure_state = "THERMAL_VAPOR"
                vessel_fluid_units = max(0, vessel_fluid_units - current_hold_latency)
                idle_streak = 0
                high_pressure_duration = 0
                
            elif tag in ['OPEN_LOW_PRESSURE_LINE', 'CONDUIT_DISCHARGE', 'KINETIC_CONDUIT', 'BYPASS_FREE_FLOW', 'PASSIVE_CROSS_FLOW']: 
                pressure_state = "LOW_PRESSURE"
                vessel_fluid_units = max(0, vessel_fluid_units - current_hold_latency)
                high_pressure_duration = 0
                idle_streak = 0
                
            elif tag in ['BATCH_SHUTDOWN', 'COMPLETED_LOCK_HALT', 'FINAL_SYSTEM_EVACUATION', 'INERT_WASTE_FLAG']:
                high_pressure_duration = idle_streak = 0
                if tag == 'COMPLETED_LOCK_HALT': 
                    pressure_state = "PRESSURE_LOCK"
                else:
                    vessel_fluid_units, pressure_state = 0, "IDLE"
                    if tag == 'FINAL_SYSTEM_EVACUATION': system_initialized = False
                    
            if generate_logs:
                duration_txt = f"{current_hold_latency}x Viive"
                status_text = "RISTIRIITA:" + error_msg if is_error_step else "Mekaaninen vaihe OK."
                log_lines.append(f"Askel {step:05d} | {token:<15} | {tag:<26} | {vessel_fluid_units:<4} | {pressure_state:<12} | {status_text} ({duration_txt})")
            
    return logical_contradictions, log_lines
def shuffle_within_folios(tokens_with_locus, rng):
    """ Ryhmittelee ja sekoittaa sanat poikkeuksetta VAIN kunkin oman sivun sisällä """
    folio_groups = defaultdict(list)
    folio_order = []
    
    for token, folio in tokens_with_locus:
        if folio not in folio_groups:
            folio_order.append(folio)
        folio_groups[folio].append(token)
        
    shuffled_result = []
    for folio in folio_order:
        tokens = folio_groups[folio].copy()
        rng.shuffle(tokens)
        for t in tokens:
            shuffled_result.append((t, folio))
            
    return shuffled_result

def process_stress_test(filepath):
    """
    Pääohjelma: Lataa korpuksen, tyhjentää muistin, ajaa aineiston sekvenssin
    sekä suorittaa 1 000 akateemista sivunsisäistä Monte Carlo -permutaatioajoa.
    """
    # Varmistetaan, että filepath on puhdas merkkijono
    if isinstance(filepath, list):
        if len(filepath) > 1:
            filepath = filepath[1]
        else:
            print("Virhe: Tiedostopolku puuttuu.")
            return

    if not os.path.exists(filepath):
        print(f"Virhe: Tiedostoa '{filepath}' ei löydy.")
        return
        
    print(f"Ladataan kohde-korpusta: '{filepath}'...")
    tokens_with_locus = []
    current_locus_folio = None
    
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            tokens, folio = clean_and_extract_tokens(line)
            if folio: current_locus_folio = folio
            for t in tokens: tokens_with_locus.append((t, current_locus_folio))
            
    total_words = len(tokens_with_locus)
    if total_words == 0: 
        print("Virhe: Puhdistettua aineistoa ei löytynyt.")
        return
        
    print(f"Puhdistus valmis. Käsitellään {total_words:,} genuine-tokenia...")
    
    # 1. Ajetaan aito teksti dynaamisen fysiikka- ja gallows-saranamoottorin läpi
    orig_errors, visual_logs = run_simulation_engine(tokens_with_locus, generate_logs=True)
    actual_steps = len(visual_logs)
    orig_compliance = ((actual_steps - orig_errors) / actual_steps * 100) if actual_steps > 0 else 0
    
    # 2. Käynnistetään akateeminen Within-Folio Monte Carlo -kontrollitestaus
    iterations = 1000
    print(f"Käynnistetään {iterations:,} iteraation sivukohtainen (Within-Folio) sekoitusajo...")
    shuffled_errors = []
    rng = random.Random(1337)
    
    for idx in range(iterations):
        shuffled_list = shuffle_within_folios(tokens_with_locus, rng)
        errors, _ = run_simulation_engine(shuffled_list, generate_logs=False)
        shuffled_errors.append(errors)
        
    avg_shuffled_errors = sum(shuffled_errors) / iterations
    min_shuffled = min(shuffled_errors)
    max_shuffled = max(shuffled_errors)
    p_value = (sum(x <= orig_errors for x in shuffled_errors) + 1) / (iterations + 1)
    
    print("\n" + "="*85)
    print(" VFSF GLOBAL STRESS TESTER v3.8.2 — TULOSYHTEENVETO")
    print("="*85)
    print(f" Aito järjestys virheet:              {orig_errors} kpl / {actual_steps} askelta ({orig_compliance:.2f} % OK)")
    print(f" Satunnaiskohinan keskiarvovirheet:   {avg_shuffled_errors:.2f} kpl")
    print(f" Satunnaiskohinan virheväli (Min/Max): {min_shuffled} - {max_shuffled} kpl")
    print(f" Empiirinen p-arvo (Sattumatodennäköisyys): {p_value:.6f}")
    print("-" * 85)
    if p_value < 0.05:
        print(" TULOS: ERITTÄIN MERKITSEVÄ (p < 0.05). Sanajärjestyksen teollinen signaali vahvistettu!")
    else:
        print(" TULOS: Ei tilastollisesti merkitsevä globaalissa putkessa.")
    print("="*85)

    output_report_name = "vfsf_stress_test_report_v382.txt"
    with open(output_report_name, 'w', encoding='utf-8') as out_f:
        out_f.write("="*125 + "\n")
        out_f.write(" VFSF GLOBAL STRESS TESTER v3.8.2 — MASTER TELEMETRIALOKI JA TILASTORAPORTTI\n")
        out_f.write(" Tekijäoikeus (C) 2026 Juho Olavi Laakso (Paimio, Finland) | MIT License\n")
        out_f.write("="*125 + "\n")
        out_f.write(f" Käsitelty tiedosto: {filepath} | Tokeneita: {total_words:,} | Vaiheita: {actual_steps:,}\n")
        out_f.write("-" * 125 + "\n")
        out_f.write(f"{'ASKEL':<11} | {'TOKEN':<15} | {'LAITETAGI / OPERAATTORI':<26} | {'REG':<4} | {'PAINETILA':<12} | {'SUORITUSLOKI / STATUS'}\n")
        out_f.write("-" * 125 + "\n")
        for line in visual_logs: out_f.write(line + "\n")
        out_f.write("-" * 125 + "\n\n")
        out_f.write(f"Aito virheet: {orig_errors} | Kohinan keskiarvo: {avg_shuffled_errors:.2f} | p-arvo: {p_value:.6f}\n")
        
    print(f"\nTäysi lokiraportti tallennettu tiedostoon: '{output_report_name}'")

if __name__ == "__main__":
    if len(sys.argv) > 1: 
        process_stress_test(sys.argv[1])
    else:
        print("Käyttö: python vfsf_global_tester_v382.py <tiedostonnimi.txt>")
