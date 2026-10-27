#!/usr/bin/env python3
"""
===================================================================================
THE VFSF COMPILER v1.2 (File-Reader Edition)
===================================================================================
Tekijä: Juho Olavi Laakso (Paimio, Finland)
Konteksti: Voynich Manuscript Functional Syntax Framework (VFSF)
Lisenssi: Creative Commons Attribution 4.0 International (CC BY 4.0)
GitHub: Voynich-Manuscript-Functional-Syntax-Framework
Status: Universaali kääntäjämoottori automaattisella tiedostoluvulla (A & B -kielet)
OSA 1/2: Rekisterit, Globaali Kalibrointi ja Sanastorakenne
===================================================================================
"""
import re
import sys
import os

# --- UNIVERSAALI HARDWARE-REKISTERI JA KOMENTOMATRIISI ---
MATRIX_MAP_ORDERED = [
    ('qokch', 'PRESSURIZED_CALIBRATION'),
    ('qokain', 'FORCED_OPEN_CHANNEL_FLUSH'),
    ('qotal', 'PRESSURE_BOOST_THROTTLE'),
    ('qokor', 'FORCED_EVACUATION_CYCLE'),
    ('pched', 'INIT_ACTIVATION'),
    ('oteog', 'BATCH_SHUTDOWN'),
    ('daiin', 'COMPLETED_LOCK_HALT'),
    ('ckhhey', 'CHECK_VALVE_ISOLATION'),
    ('chcthy', 'VALVE_CALIBRATION'),
    ('cholchiky', 'VALVE_CALIBRATION'),
    ('dair', 'CONTAINMENT_RECEPTACLE'),
    ('dar', 'CONTAINMENT_RECEPTACLE'),
    ('dal', 'HYDROSTATIC_PUMP_UP'),
    ('dol', 'GRAVITY_DRAIN_DOWN'),
    ('cfh', 'JET_FLOW_DISCHARGE'),
    ('cph', 'PASSIVE_CROSS_FLOW'),
    ('cthey', 'THERMAL_INFUSION'), 
    ('cthy', 'THERMAL_INFUSION'),
    ('ched', 'FLUID_STABILIZATION'),
    ('chey', 'FLUID_STABILIZATION'),
    ('sheteal', 'SYSTEM_REBOOT'),
    ('shdy', 'SYSTEM_REBOOT'),
    ('shedy', 'SYSTEM_REBOOT'),
    ('shol', 'SYSTEM_REBOOT'),
    ('shekey', 'SYSTEM_REBOOT'),
    ('dain', 'OPEN_LOW_PRESSURE_LINE'),
    ('chly', 'VALVE_CALIBRATION'),
    ('chal', 'VALVE_CALIBRATION'),
    ('okor', 'REFRACTORY_RESTART'),
    ('oror', 'FINAL_SYSTEM_EVACUATION'),
    ('chody', 'STABILIZATION_HOLD'),  
    ('otys', 'SYSTEM_REBOOT'),       
    ('ytch', 'SYSTEM_CHRONO'),       
    ('pd', 'INIT_ACTIVATION'),
    ('p', 'INIT_ACTIVATION'),
    ('s', 'SYSTEM_REBOOT'),
    ('r', 'REFRACTORY_RESTART'),
    ('qok', 'HIGH_PRESSURE_OVERRIDE'),
    ('or', 'REFRACTORY_RESTART'),
    ('ar', 'SEDIMENT_SETTLING'),
    ('al', 'HYDROSTATIC_PUMP_UP'),
    ('aiin', 'CLOSED_HIGH_PRESSURE_LINE'),
    ('ain', 'OPEN_LOW_PRESSURE_LINE'),
    ('am', 'CONTINUOUS_SEQUENCE_LINK'),
    ('ol', 'BYPASS_FREE_FLOW')
]

FINNISH_LEXICON = {
    'INIT_ACTIVATION': "PÄÄVIRTA KYTKETTY: Linjaston alustus ja kanavien avaaminen.",
    'SYSTEM_REBOOT': "JÄRJESTELMÄN NOLLAUS: Kellojakson salpa ja tahdistuspulssi aktivoitu.",
    'VALVE_CALIBRATION': "VENTTIILIN SÄÄTÖ: Virtausventtiilin dynaaminen kalibrointitila kytketty.",
    'CONTAINMENT_RECEPTACLE': "MATERIAALILATAUS: Pääsyöttöallas online, uusi nestemassa ajettu sisään.",
    'HYDROSTATIC_PUMP_UP': "HYDROSTAATTINEN PUMPPAUS: Paine kytketty, neste pakotettu nousemaan ylöspäin.",
    'PRESSURE_BOOST_THROTTLE': "PAINEEN KURISTUS: Linjavastus kytketty, maksimi dynaaminen paine väylässä.",
    'PRESSURIZED_CALIBRATION': "PAINEKALIBROINTI: Paineellinen hienosäätövaihe kytketty linjaan.",
    'THERMAL_INFUSION': "TERMISTEN KÄSITTELY: Lämpöenergia kytketty (Uutto/Tislausvaihe aktiivinen).",
    'OPEN_LOW_PRESSURE_LINE': "YLIVUOTO AVATTU: Matalapainelinja auki, aines siirtyy vapaasti eteenpäin.",
    'CLOSED_HIGH_PRESSURE_LINE': "KORKEAPAINE LUKITTU: Korkeatehoinen ja tiivis reaktiotila kytketty.",
    'FORCED_OPEN_CHANNEL_FLUSH': "TEHOSTETTU HUUHTELU: Avoimen kanavan pikasyöttö ja puhdistus käynnistetty.",
    'BATCH_SHUTDOWN': "ERÄAJON ALASAJO: Tuotesykli päätetty, linja ajettu tyhjäksi tuotteesta.",
    'COMPLETED_LOCK_HALT': "PROSESSILUKKO: Venttiilit suljettu hallitusti, kammio eristetty hautumista varten.",
    'CHECK_VALVE_ISOLATION': "TAKAIskuVENTTIILI: Mekaaninen sulku paluuvirtauksen estämiseksi.",
    'BYPASS_FREE_FLOW': "OHIPUTKI KYTKETTY: Paineentasaus ja vapaavalunta aktivoitu ilman ulkoista painetta.",
    'REFRACTORY_RESTART': "JÄÄHTYMISVAIHE: Linjan kiertoreititys ja cooldown-jakso käynnistetty.",
    'CONTINUOUS_SEQUENCE_LINK': "SARJAKYTKENTÄ: Suora väylälinkki seuraavaan moduuliin ilman latenssia.",
    'JET_FLOW_DISCHARGE': "SUIHKUTUS: Korkeapaineinen purku kapeasta suuttimesta käynnistetty.",
    'SEDIMENT_SETTLING': "SAKKAUS: Raskaan pohjasakan passiivinen laskeuttaminen käynnistetty astiassa.",
    'FLUID_STABILIZATION': "NESTEEN TASAUS: Virtausnopeuden pudotus ja linjapuskurointi aktivoitu.",
    'HIGH_PRESSURE_OVERRIDE': "PAINEPAKOTE: Ulkoinen mekaaninen pakko-ohjaus kytketty väylään.",
    'STABILIZATION_HOLD': "STABILOINTILUKITUS: Linjan staattinen tasaus ja painepatjan pito paikoillaan.",
    'SYSTEM_CHRONO': "AIKAVALVONTA: Järjestelmän sisäinen käyntiaika- ja sekvenssimittari kytketty."
}

# --- KALIBROINTIVAKIOT ---
MAX_HIGH_PRESSURE_DURATION = 4   
MAX_IDLE_STREAK = 4              

def clean_and_extract_tokens(raw_line):
    """ Siivoaa raa'asta komentorivistä Landinin/EVA-koodit, kommentit ja palauttaa puhtaat sanat """
    line_str = raw_line.strip()
    if not line_str or line_str.startswith('#'): 
        return []
    
    match = re.search(r'<(?:f\d+[rv]\.\d+,[^>]+>)?\s*([^<\n]+)', line_str)
    if not match:
        clean_text = re.sub(r'<[^>]+>', '', line_str).strip()
    else:
        clean_text = match.group(1).strip()
        
    clean_text = re.sub(r'[{}\[\]!@%<>]', '', clean_text)
    tokens = [t.strip() for t in re.split(r'[\s.]+', clean_text) if t]
    return tokens

def parse_token(token):
    cleaned = token.lower()
    if cleaned == "oror": return 'FINAL_SYSTEM_EVACUATION'
    for key, tag in MATRIX_MAP_ORDERED:
        if key in cleaned:
            return tag
    return "UNKNOWN"
def compile_voynich_stream(tokens_list, is_circular_chart=False):
    """ Ajaa puhdistetun datan tiukan tilakoneen läpi ja generoi raportin """
    system_initialized = is_circular_chart  # Pyöreässä kaaviossa linja on valmiiksi kytketty ja esiladattu
    vessel_fluid_units = 3 if is_circular_chart else 0 
    pressure_state = "LOW_PRESSURE" if is_circular_chart else "IDLE"
    logical_contradictions = 0
    step = 0
    
    high_pressure_duration = 0   
    idle_streak = 0              
    
    report_lines = []
    
    for token in tokens_list:
        tag = parse_token(token)
        step += 1
        
        if tag == "UNKNOWN":
            report_lines.append(f"Askel {step:02d} | {token:<15} | {'UNKNOWN':<26} | {'-':<6} | {'-':<15} | Varoitus: Tuntematon komponentti.")
            continue

        # --- v8.2 CRITICAL HARDWARE CHECKS ---
        if token.lower() in ["tsheos", "potchokor", "osar", "daiin"]:
            system_initialized = True
            vessel_fluid_units = 4 
            pressure_state = "LOW_PRESSURE" if pressure_state == "IDLE" else pressure_state
            high_pressure_duration = 0
            idle_streak = 0
            suomi_ohje = "ERÄAJON ALUSTUS: Puskurilataus esiladattu linjaan, järjestelmä valvonnassa."
            report_lines.append(f"Askel {step:02d} | {token:<15} | {tag:<26} | {vessel_fluid_units:<6} | {pressure_state:<15} | {suomi_ohje}")
            continue

        if not system_initialized:
            if tag != 'INIT_ACTIVATION' and tag != 'SYSTEM_REBOOT':
                logical_contradictions += 1
                report_lines.append(f"Askel {step:02d} | {token:<15} | {tag:<26} | {'-':<6} | {pressure_state:<15} | RISTIRIITA: Komento ajettu ennen päävirtaa!")
                continue

        if tag in ['INIT_ACTIVATION', 'SYSTEM_REBOOT', 'VALVE_CALIBRATION', 'SEDIMENT_SETTLING', 'STABILIZATION_HOLD', 'SYSTEM_CHRONO']:
            system_initialized = True
            if pressure_state == "IDLE": pressure_state = "LOW_PRESSURE"
            if tag in ['SYSTEM_REBOOT', 'SEDIMENT_SETTLING']:
                idle_streak += 1
                if idle_streak > MAX_IDLE_STREAK: 
                    logical_contradictions += 1
                    report_lines.append(f"Askel {step:02d} | {token:<15} | {tag:<26} | {vessel_fluid_units:<6} | {pressure_state:<15} | RISTIRIITA: Joutokäyntiviive ylittynyt!")
                    continue
            else:
                idle_streak = 0
            
        elif tag == 'CONTAINMENT_RECEPTACLE':
            vessel_fluid_units += 2
            idle_streak = 0
            
        elif tag in ['HYDROSTATIC_PUMP_UP', 'PRESSURE_BOOST_THROTTLE', 'PRESSURIZED_CALIBRATION', 'CLOSED_HIGH_PRESSURE_LINE', 'HIGH_PRESSURE_OVERRIDE']:
            if vessel_fluid_units <= 0:
                logical_contradictions += 1
                report_lines.append(f"Askel {step:02d} | {token:<15} | {tag:<26} | {vessel_fluid_units:<6} | {pressure_state:<15} | RISTIRIITA: Kuivapumppaus ilman nestesyöttöä!")
                continue
            pressure_state = "HIGH_PRESSURE"
            vessel_fluid_units = max(0, vessel_fluid_units - 1)
            idle_streak = 0
            
            high_pressure_duration += 1
            if high_pressure_duration > MAX_HIGH_PRESSURE_DURATION: 
                logical_contradictions += 1
                report_lines.append(f"Askel {step:02d} | {token:<15} | {tag:<26} | {vessel_fluid_units:<6} | {pressure_state:<15} | RISTIRIITA: Ylipainerasitus ylittynyt!")
                continue
            
        elif tag == 'THERMAL_INFUSION':
            if vessel_fluid_units <= 0 and pressure_state == "HIGH_PRESSURE":
                logical_contradictions += 1
                report_lines.append(f"Askel {step:02d} | {token:<15} | {tag:<26} | {vessel_fluid_units:<6} | {pressure_state:<15} | RISTIRIITA: Tyhjän reaktorin kuivakeitto!")
                continue
            pressure_state = "THERMAL_VAPOR"
            vessel_fluid_units = max(0, vessel_fluid_units - 1)
            idle_streak = 0
            high_pressure_duration = 0 
            
        elif tag == 'OPEN_LOW_PRESSURE_LINE':
            pressure_state = "LOW_PRESSURE"
            vessel_fluid_units = max(0, vessel_fluid_units - 1)
            high_pressure_duration = 0 
            idle_streak = 0
            
        elif tag in ['BATCH_SHUTDOWN', 'COMPLETED_LOCK_HALT', 'FINAL_SYSTEM_EVACUATION']:
            high_pressure_duration = 0
            idle_streak = 0
            if tag == 'COMPLETED_LOCK_HALT':
                pressure_state = "PRESSURE_LOCK"
            else:
                vessel_fluid_units = 0
                pressure_state = "IDLE"
                if tag == 'FINAL_SYSTEM_EVACUATION': system_initialized = False

        suomi_ohje = FINNISH_LEXICON.get(tag, "Rekisterivaste OK.")
        report_lines.append(f"Askel {step:02d} | {token:<15} | {tag:<26} | {vessel_fluid_units:<6} | {pressure_state:<15} | {suomi_ohje}")

    print("="*115)
    print(" THE VFSF COMPILER v1.2 — AUTOMAATTINEN PROSESSI- JA TEHDASRAPORTTI")
    print("="*115)
    print(f"{'ASKELE':<7} | {'VMS TOKEN':<15} | {'LAITETAGI':<26} | {'NESTE':<6} | {'PAINE':<15} | {'SUOMENKIELINEN OHJAUSKOMENTO / STATUS'}")
    print("-" * 115)
    for line in report_lines:
        print(line)
    print("-" * 115)
    compliance = ((step - logical_contradictions) / step * 100) if step > 0 else 0
    print(f" KÄÄNNÖS VALMIS. Askeleita ajettu: {step} | Havaitut ristiriidat: {logical_contradictions} | Yhteensopivuus: {compliance:.2f}%")
    print("="*115)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        if not os.path.exists(file_path):
            print(f"Virhe: Tiedostoa '{file_path}' ei löydy.")
            sys.exit(1)
            
        print(f"Ladataan ja puhdistetaan tiedostoa: {file_path}...\n")
        all_tokens = []
        is_circular = False
        
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if any(x in line.lower() for x in ["f68r", "fros", "star", "circular"]):
                    is_circular = True
                extracted = clean_and_extract_tokens(line)
                all_tokens.extend(extracted)
                
        if not all_tokens:
            print("Virhe: Tiedostosta ei uutettu yhtään kelvollista prosessisanaa.")
            sys.exit(1)
            
        print(f"Uutettu yhteensä {len(all_tokens)} genuine-sanaa. Käynnistetään kääntäjä...")
        compile_voynich_stream(all_tokens, is_circular_chart=is_circular)
        
    else:
        print("Käynnistetään The VFSF Compiler v1.2 — Oletusarvoinen diagnostiikka-ajo...")
        print("(Vihje: Voit ajaa ulkoisen tiedoston komentoriviltä: python vfsf_compiler.py tiedosto.txt)\n")
        test_stream = ["ar", "chly", "sheteal", "aram", "dair", "shedy", "okor", "dain", "cthy"]
        compile_voynich_stream(test_stream, is_circular_chart=False)
