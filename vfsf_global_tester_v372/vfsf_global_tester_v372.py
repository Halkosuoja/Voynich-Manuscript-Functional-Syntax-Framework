#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===================================================================================
THE VFSF GLOBAL STRESS TESTER v3.7.2 (Deeply Commented Production Edition)
===================================================================================
Tekijä: Juho Olavi Laakso (Paimio, Finland)
Konteksti: Voynich Manuscript Functional Syntax Framework (VFSF)
Lisenssi: MIT License (Copyright (c) 2026 Juho Olavi Laakso)
GitHub: Voynich-Manuscript-Functional-Syntax-Framework
===================================================================================
"""
import re
import sys
import os
import random

# =================================================================================
# GLOBAALI HARDWARE-REKISTERI JA ABSTRAKTI OPERAATTORIMATRIISI
# =================================================================================
# Järjestys on dynaamisesti kriittinen: pisimmät osamerkkijonot (Longest Match) 
# sijoitetaan listan ylälaitaan, jotta haku ei pirsto hitsattuja ligatuureja.
MATRIX_MAP_ORDERED = [
    # 1. Monimutkaiset korkeapainelohkot ja pakko-ohjatut hätäevakuoinnit
    ('qokch', 'PRESSURIZED_CALIBRATION'),     # Paineistettu kalibrointiajo linjassa
    ('qokain', 'FORCED_OPEN_CHANNEL_FLUSH'),   # Pakotettu avoimen kanavan huuhtelusykli
    ('qotal', 'PRESSURE_BOOST_THROTTLE'),      # Linjavastuksen dynaaminen kuristus paineella
    ('qokor', 'FORCED_EVACUATION_CYCLE'),      # Pakko-evakuointi hätätilassa
    
    # 2. Järjestelmän alustus- ja hallitut alasajokomennot
    ('pched', 'INIT_ACTIVATION'),              # Ensimmäinen mekaaninen käynnistyspulssi
    ('oteog', 'BATCH_SHUTDOWN'),               # Tuotantoerän (batch) hallittu alasajo
    ('daiin', 'COMPLETED_LOCK_HALT'),          # Linjaportti suljettu, sykli valmis
    ('ckhhey', 'CHECK_VALVE_ISOLATION'),       # Mekaaninen takaiskuventtiilin sulku
    ('chcthy', 'VALVE_CALIBRATION'),           # Venttiilivälyksen dynaaminen hienosäätö
    ('cholchiky', 'VALVE_CALIBRATION'),        # Vaihtoehtoinen hienosäätökomento
    
    # 3. Materiaalin syöttöastiat ja säiliöt (Nostavat nestetasoa muuttujarekisterissä REG V)
    ('dair', 'CONTAINMENT_RECEPTACLE'),        # Eristetty reaktiosäiliö / allas
    ('dar', 'CONTAINMENT_RECEPTACLE'),         # Pääsyöttöallas / keräyssäiliö
    
    # 4. Aktiiviset ja passiiviset siirtovektorit (Kuluttavat nestetasoa paineella ainetaseessa)
    ('dal', 'ACTIVE_UPWARD_VECTOR'),           # Paineistettu nousuputki / pumppaus ylös
    ('dol', 'GRAVITY_DRAIN_DOWN'),             # Paineeton valumaputki / valuma alas
    ('cfh', 'JET_FLOW_DISCHARGE'),             # Suoraruiskutussuutin / purkaus
    ('cph', 'PASSIVE_CROSS_FLOW'),             # Passiivinen poikittaisvirtaus linjastossa
    ('cthy', 'THERMAL_INFUSION'),              # Terminen uuttovaihe / lämmitys reaktorissa
    ('ched', 'FLUID_STABILIZATION'),           # Nesteen dynaaminen stabilointi / puskurivaippa
    ('chey', 'FLUID_STABILIZATION'),           # Puskurivaipan rinnakkaiskomento
    
    # 5. Järjestelmäresethit ja matalapaineiset linja-avaukset
    ('sheteal', 'SYSTEM_REBOOT'),              # Kokonaisvaltainen laiteohjelmiston reseth
    ('shdy', 'SYSTEM_REBOOT'),                 # Paikallinen osalohkon uudelleenkäynnistys
    ('shedy', 'SYSTEM_REBOOT'),                # Lohkoresethin variaatio
    ('shol', 'SYSTEM_REBOOT'),                 # Kanavan nollauspulssi
    ('shekey', 'SYSTEM_REBOOT'),               # Ohjausrekisterin nollaus
    ('dain', 'OPEN_LOW_PRESSURE_LINE'),        # Matalapaineväylän mekaaninen avaus
    ('chly', 'VALVE_CALIBRATION'),             # Kalibrointiajo linjassa
    ('chal', 'VALVE_CALIBRATION'),             # Kalibrointiajon variaatio
    ('okor', 'REFRACTORY_RESTART'),            # Jäähdytysvaiheen uudelleenkäynnistys
    ('oror', 'FINAL_SYSTEM_EVACUATION'),       # Järjestelmän lopullinen tyhjennysajo
    ('pd', 'INIT_ACTIVATION'),                 # Alkupään alustusbitit
    ('p', 'INIT_ACTIVATION'),                  # Yksittäinen avauspalkki
    ('s', 'SYSTEM_REBOOT'),                    # Tahdistus / synkronointipulssi
    ('r', 'REFRACTORY_RESTART'),               # Refraktorinen jäähdytyskierto
    ('qok', 'HIGH_PRESSURE_OVERRIDE'),         # Korkeapaineen pakko-ohjaus
    ('or', 'REFRACTORY_RESTART'),              # Jäähdytyskierron juurimerkki
    ('ar', 'SEDIMENT_SETTLING'),               # Sakan laskeutusvaihe mekaanisessa kourussa
    ('al', 'ACTIVE_UPWARD_VECTOR'),            # Pystynousun juurivektori
    ('aiin', 'CLOSED_HIGH_PRESSURE_LINE'),     # Korkeapainerengas lukittu tiiviiksi
    ('ain', 'OPEN_LOW_PRESSURE_LINE'),         # Matalapaineväylän avauksen juurimerkki
    ('am', 'CONTINUOUS_SEQUENCE_LINK'),        # Katkeamaton väylälinkki ilman latenssia
    ('ol', 'BYPASS_FREE_FLOW'),                # Paineeton ohiputki / vapaa virtaus linjassa
    
    # 6. Atomiset linja-osoitteet ja visuaaliset nollasaranat (Kuvatason murtomatchit)
    ('y', 'CHANNEL_ADDRESS_HOLD'),             # Passiivinen kanavaosoitteen pito rekisterissä
    ('d', 'PHASE_CONVERSION_HOLD'),            # Olomuodon muutoksen / lauhteen passiivipito
    ('o', 'GRAVITY_FEED_HOLD'),                # Paineettoman vapaan syötön passiivipito
    ('an', 'BUS_CHANNEL_SELECT'),              # Väyläkanavan valintabitti telemetriassa
    ('on', 'BUS_CHANNEL_SELECT'),              # Väyläkanavan valintabitin variaatio
    ('n', 'TERMINAL_RESTRICTOR'),              # Supistusliitin / uoman mekaaninen päätytulppa
    ('cha', 'PASSIVE_JUNCTION_HOLD'),          # Passiivinen haaroituspisteen odotustila
    ('iiin', 'LOW_PRESSURE_VALVE_LOCK'),       # Matalapaineväylän lukitusventtiili
    ('g', 'INERT_WASTE_FLAG'),                 # Kuivan kiintoainesakan tyhjennyslippu
	('l', 'OPEN_OUTLET_DRAIN'),                # Paineeton paluulinja / vapaa poistoväylä
    ('vor', 'REFRACTORY_RESTART'),             # Jäähdytysvaiheen sumea muoto lokissa
    ('olb', 'BYPASS_FREE_FLOW'),               # Kouruliukuman dynaaminen ohiputkivirtaus
    ('ckh', 'CHECK_VALVE_ISOLATION')           # Kuluneen kynänjäljen tuottama takaiskusulku
]

# Tunnistetaan itsenäiset peruskomponentit pitkien kaskadiuomien halkaisua varten
SPLITTABLE_STEMS = ['cthy', 'daiin', 'dain', 'chol', 'shol', 'dal', 'dol', 'dar', 'oror', 'ckhy', 'cho']


# Järjestelmän dynaamiset mekaaniset suoritusrajat (Fysiikan sietorajat)
MAX_HIGH_PRESSURE_DURATION = 4  # Maksimaalinen sallittu yhtäjaksoinen ylipainerasitus askelina
MAX_IDLE_STREAK = 15            # Optimoitu joutokäyntikynnys pitkien uomaliukumien sallimiseksi
# =================================================================================
# SYÖTEDATAN PUHDISTUS JA BITTIJÄSENNYS (THE GENUINE TOKEN PURIFIER)
# =================================================================================

def clean_and_extract_tokens(raw_line):
    """
    Suorittaa raakadatalle tiukan mekaanisen esipuhdistuksen (The Genuine Token Purifier).
    Pyyhkii pois Landinin transkription kommentit, erikoiskoodit ja optiset häiriöt,
    jotka muuten pätkisivät aidon Voynich-musteen mekaanisesti rikkinäisiksi paloiksi.
    """
    # Pyyhitään rivin alun ja lopun tyhjät välit pois muistista lennosta
    line_str = raw_line.strip()
    if not line_str or line_str.startswith('#'): return [], None
    
    # --- LOCUS-TUNNISTUS SIVUNVAIHDON LOHKORESETOINTIA VARTEN ---
    # Etsitään RegExillä sivunumeromerkinnät (kuten <f1r>, <f2v.1>) lennosta.
    # Tämä varmistaa, ettei edellisen sivun painekuorma valu pilaamaan uuden sivun tiloja.
    locus_match = re.search(r'<f(\d+[rv])', line_str.lower())
    current_folio = locus_match.group(1) if locus_match else None
    
    # --- TRANSKRIPTIOHÄIRIÖIDEN SUORAPUHDISTUS ---
    clean_text = re.sub(r'<[^>]+>', '', line_str)       # Pyyhitään loogiset paikkakehykset < >
    clean_text = re.sub(r'\{[^}]+\}', '', clean_text)   # Pyyhitään EVA-transkription arvaussulkeet { }
    clean_text = re.sub(r'\[[^\]]+\]', '', clean_text)   # Pyyhitään Landinin tekstinkorjaushakasulkeet [ ]
    clean_text = re.sub(r'@[0-9;]+', '', clean_text)    # Pyyhitään optiset välikoodit (kuten @192; ja @130;)
    
    # --- OPTINEN SUMEUTUSOHJAIN (FUZZY LOGIC) ---
    # Pyyhitään heittomerkit ja katkoviivat, jotta kulunut musteviiva yhdistyy ehjäksi tagiksi.
    # Esimerkki: "qo'ky" sumennetaan ja korjataan suoraan muotoon "qoky" (HIGH_PRESSURE_OVERRIDE).
    clean_text = clean_text.replace("'", "").replace("’", "")
    clean_text = re.sub(r'[{}\[\]!@%<>?:*#$,=+\-]', ' ', clean_text)
    
    # Paloitellaan puhdistettu tekstivirta tyhjien välien ja pisteiden perusteella tokeneiksi
    raw_tokens = [t.strip().lower() for t in re.split(r'[\s.]+', clean_text) if t]
    
    # Varmistetaan, ettei koodivirtaan pääse vuotamaan puhtaita sivunumerotunnisteita (esim. 'f1r')
    # laitteistotagoiksi (kuten f1r -> r -> REFRACTORY_RESTART), mikä loisi keinotekoisia herätysvirheitä.
    filtered_tokens = [t for t in raw_tokens if not re.match(r'^f\d+[rv]$', t)]
    return filtered_tokens, current_folio

def parse_token(token):
    """ Vertaa puhdistettua sanaa komentomatriisiin ja palauttaa sen arkkitehtorisen laitetagin """
    if token == "oror": return 'FINAL_SYSTEM_EVACUATION'
    if token == "qokey": return 'HIGH_PRESSURE_OVERRIDE'
    for key, tag in MATRIX_MAP_ORDERED:
        if key == token or key in token: return tag
    return "UNKNOWN"
def tokenize_and_split_with_multiplier(token):
    """
    Kääntäjän dynaaminen esikäsittelijä (The Sequence Multiplier Engine).
    Erottaa sanan sisältä ne toisen tekoälymallin auditoinnissa paljastuneet
    kestoinfiksit (-ee- ja -eee-) ja purkaa pitkät agglutinoituneet kaskadiuomat.
    """
    cleaned = token.lower()
    multiplier = 1 # Perusoletus: 1x kellojakson viive
    
    # --- INFIX MULTIPLIER: AIKARAJAKIERTOJEN JA PIDON MITTAUS ---
    # Koodi ei enää tuhoa tai hylkää näitä merkkejä, vaan mittaa niistä todellisen aikaviiveen.
    if 'eee' in cleaned:
        multiplier = 3  # Kolminkertainen maksimaalinen pito- ja viiveajon lukitus
        cleaned = cleaned.replace('eee', '', 1)
    elif 'ee' in cleaned:
        multiplier = 2  # Kaksikertainen dynaaminen puskuritila
        cleaned = cleaned.replace('ee', '', 1)
        
    # Jos puhdistettu sana löytyy sellaisenaan matriisista, palautetaan se suoraan kertoimen kanssa
    if parse_token(cleaned) != "UNKNOWN":
        return [(cleaned, multiplier)]
        
    # --- KASKADIUOMAN PURKU (SPLIT-AND-PARSE) ---
    # Jos kyseessä on pitkä yhdyssana (esim. ctheyykol), se halkaistaan itsenäisiksi makrokäskyiksi.
    for stem in SPLITTABLE_STEMS:
        if stem in cleaned and len(cleaned) > len(stem):
            idx = cleaned.find(stem)
            part1, part2 = cleaned[:idx], cleaned[idx:]
            sub_tokens = []
            
            # Ajetaan ensimmäinen uomavaihe 1x perustilassa
            if part1 and parse_token(part1) != "UNKNOWN": 
                sub_tokens.append((part1, 1))
            # Siirretään dynaaminen aikarajakerroin vaikuttamaan loppuvaiheen uomaan
            if part2 and parse_token(part2) != "UNKNOWN": 
                sub_tokens.append((part2, multiplier))
                
            if sub_tokens: return sub_tokens
            
    return [(cleaned, multiplier)]
# =================================================================================
# AIDON TEKSTIVIRRAN GLOBAALI PROSESSI- JA FYSIIKKASIMULAATTORI
# =================================================================================

def run_simulation_with_logging(tokens_with_locus):
    """
    Ajaa puhdistetun tekstivirran dynaamisen osatila-automaatin (Strict v8.2) läpi.
    Valvoo reaaliaikaisesti ainetaseita, ylipainerasituksia ja latensseja askel askeleelta.
    Tuottaa täydellisen sarakemuotoisen telemetrialokin virhe-erittelyineen.
    """
    # --- AJONAIKAISET HARDWARE-MUUTTUJAREKISTERIT ---
    system_initialized = False   # Boolean-salpa kylmäkäynnistyksen ja herätyksen valvontaan
    vessel_fluid_units = 0        # Nestemassan pääpuskurirekisteri (Muuttujatase REG V)
    pressure_state = "IDLE"       # Putkiston senhetkinen painetila (IDLE/LOW/HIGH/THERMAL/LOCK)
    logical_contradictions = 0    # Havaittujen loogisten fysiikkaristiriitojen kokonaislaskuri
    step = 0                      # Askeleellinen juokseva kokonaislaskuri halkaisujen jälkeen
    high_pressure_duration = 0    # Yhtäjaksoisen teollisen ylipaineen aikajaksojen aikalaskuri
    idle_streak = 0               # Avointen uomien passiivisen linjapidon latenssiputki
    log_lines = []                # Raporttitiedostoon kirjoitettava visualisoitu suoritusloki
    last_folio = None             # Edellisen käsitellyn sivun (Folio Locus) seurantamuuttuja
    
    # Käynnistetään pääsekvenssilooppi genuine-tokeneille
    for raw_token, folio in tokens_with_locus:
        # Puretaan agglutinoituneet sanat kaskadiuomiksi ja mitataan latenssikertoimet
        sub_tokens = tokenize_and_split_with_multiplier(raw_token)
        
        for token, multiplier in sub_tokens:
            step += 1
            
            # --- LOHKORESETOINTI SIVUN VAIHTUESSA (BLOCK RESET ON FOLIO SWITCH) ---
            # Jos havaitaan, että datavirrassa sivu vaihtuu (esim. <f1r> -> <f1v>), suoritetaan
            # rekistereille täysi nollaus. Tämä kuvaa sitä, että uusi sivu on itsenäinen laitelohko.
            if folio and last_folio and folio != last_folio:
                system_initialized, vessel_fluid_units, pressure_state, high_pressure_duration, idle_streak = False, 0, "IDLE", 0, 0
                log_lines.append(f"Askel {step:05d} | {'[FOLIO_SWITCH]':<15} | {'BLOCK_RESET':<26} | {'0':<4} | {'IDLE':<12} | INFO: Sivu vaihtunut <f{folio}>. Rekisterit nollattu.")
                
            if folio: 
                last_folio = folio
                
            # Haetaan sanalle sen arkkitehtorinen toimilaitetagi hardware-matriisista
            tag = parse_token(token)
            
            # --- TUNTEMATTOMIEN OPERAATTORIEN SEURANTA JA HANKINTA ---
            if tag == "UNKNOWN":
                log_lines.append(f"Askel {step:05d} | {token:<15} | {'UNKNOWN':<26} | {'-':<4} | {'-':<12} | Varoitus: Tuntematon operaattori.")
                continue
                
            error_msg = ""
            is_error_step = False # Lippu, joka kytkeytyy päälle jos fysiikkalaki rikkoutuu
            
            # --- ALUSTUS- JA SYSTEM RESETH -PULSSIT (INITIALIZATION PROTOCOL) ---
            # Tunnistetaan ne neljä ydinjuurta, jotka laukaisevat linjaan materiaalisyötön.
            # Alustus herättää koneen ja lataa puskuriin (REG V) kiinteän nestemassan V=4.
            if token in ["tsheos", "potchokor", "osar", "daiin"]:
                system_initialized, vessel_fluid_units, high_pressure_duration, idle_streak = True, 4, 0, 0
                pressure_state = "LOW_PRESSURE" if pressure_state == "IDLE" else pressure_state
                log_lines.append(f"Askel {step:05d} | {token:<15} | {tag:<26} | {vessel_fluid_units:<4} | {pressure_state:<12} | REKISTERIN ALUSTUS: Puskuri V=4.")
                continue

            # --- COLD START: KYLMÄKÄYNNISTYKSEN VALVONTASÄÄNTÖ ---
            # Jos järjestelmää ei ole herätetty, mikään dynaaminen paine- tai pumppausoperaatio
            # ei ole loogisesti sallittu. Sääntö sallii vain passiiviset väylä- ja osoitevalinnat ennen virtaa.
            if not system_initialized:
                if tag not in ['INIT_ACTIVATION', 'SYSTEM_REBOOT', 'CHANNEL_ADDRESS_HOLD', 'PHASE_CONVERSION_HOLD', 'GRAVITY_FEED_HOLD', 'BUS_CHANNEL_SELECT', 'TERMINAL_RESTRICTOR', 'PASSIVE_JUNCTION_HOLD', 'LOW_PRESSURE_VALVE_LOCK', 'INERT_WASTE_FLAG']:
                    logical_contradictions += 1
                    log_lines.append(f"Askel {step:05d} | {token:<15} | {tag:<26} | {'-':<4} | {pressure_state:<12} | RISTIRIITA: Komento ennen herätystä!")
                    continue
            # Kytketään infiksistä uutetun aikarajakertoimen reaaliluku latenssia varten
            current_hold_latency = multiplier
            
            # --- LAITTEISTOTILOJEN DYNAAMISET SIIRTYMÄSÄÄNNÖT JA REKISTERIMUUTOKSET ---
            if tag in ['INIT_ACTIVATION', 'SYSTEM_REBOOT', 'VALVE_CALIBRATION', 'SEDIMENT_SETTLING']:
                system_initialized = True
                if pressure_state == "IDLE": 
                    pressure_state = "LOW_PRESSURE"
                if tag in ['SYSTEM_REBOOT', 'SEDIMENT_SETTLING']:
                    # Joutokäyntiviive kasvaa dynaamisesti aikarajakertoimen (multiplier) verran
                    idle_streak += current_hold_latency
                    if idle_streak > MAX_IDLE_STREAK: 
                        logical_contradictions, error_msg, is_error_step = logical_contradictions + 1, " [Joutokäyntiviive ylittynyt!]", True
                else: 
                    idle_streak = 0
                
            elif tag in ['CHANNEL_ADDRESS_HOLD', 'PHASE_CONVERSION_HOLD', 'GRAVITY_FEED_HOLD', 'BUS_CHANNEL_SELECT', 'TERMINAL_RESTRICTOR', 'PASSIVE_JUNCTION_HOLD', 'LOW_PRESSURE_VALVE_LOCK']:
                # Atomiset linja-osoitteet ja passiiviset pääterajoittimet kytkevät linjaan passiivisen pidon.
                # Ne sallivat laitteen virtaustilan säilymisen ilman mekaanisen nestemassan kulutusta.
                if pressure_state == "IDLE": 
                    pressure_state = "LOW_PRESSURE"
                idle_streak += current_hold_latency
                if idle_streak > MAX_IDLE_STREAK:
                    logical_contradictions, error_msg, is_error_step = logical_contradictions + 1, " [Joutokäyntiviive ylittynyt!]", True
                
            elif tag == 'CONTAINMENT_RECEPTACLE': 
                # Altaan syöttö ja massan lataus: puskurirekisteri kasvaa +2 yksikköä per aikarajakerroin
                vessel_fluid_units, idle_streak = vessel_fluid_units + (2 * current_hold_latency), 0
                
            elif tag in ['HYDROSTATIC_PUMP_UP', 'PRESSURE_BOOST_THROTTLE', 'PRESSURIZED_CALIBRATION', 'CLOSED_HIGH_PRESSURE_LINE', 'HIGH_PRESSURE_OVERRIDE', 'ACTIVE_UPWARD_VECTOR', 'CHECK_VALVE_ISOLATION']:
                # --- ALIVUOTOVALVONTA (UNDERFLOW PROTOCOL) ---
                # Jos yritetään dynaamista korkeapainepumppausta ilman nestettä, laukaistaan kuivapumppausvirhe.
                if vessel_fluid_units <= 0: 
                    logical_contradictions, error_msg, is_error_step = logical_contradictions + 1, " [Kuivapumppaus ilman nestesyöttöä!]", True
                pressure_state = "HIGH_PRESSURE"
                # Kulutetaan nestemassaa dynaamisen aikarajakertoimen (multiplier) yksiköiden suhteessa
                vessel_fluid_units = max(0, vessel_fluid_units - current_hold_latency)
                idle_streak = 0
                
                # --- KYLLÄSTYMISVALVONTA (OVERPRESSURE PROTOCOL) ---
                # Korkeapaineen aikajakso kasvaa. Jos sietoraja ylittyy, laukaistaan ylipainevirhe.
                high_pressure_duration += current_hold_latency
                if high_pressure_duration > MAX_HIGH_PRESSURE_DURATION: 
                    logical_contradictions, error_msg, is_error_step = logical_contradictions + 1, error_msg + " [Putkiston ylipainerasitus!]", True
                    
            elif tag == 'THERMAL_INFUSION':
                # Valvotaan, ettei tyhjää reaktoria kuumenneta kuivaksi yhtäjaksoisessa korkeapainetilassa
                if vessel_fluid_units <= 0 and pressure_state == "HIGH_PRESSURE": 
                    logical_contradictions, error_msg, is_error_step = logical_contradictions + 1, " [Tyhjän reaktorin kuivakeitto!]", True
                pressure_state = "THERMAL_VAPOR"
                vessel_fluid_units = max(0, vessel_fluid_units - current_hold_latency)
                idle_streak = 0
                high_pressure_duration = 0
                
            elif tag == 'OPEN_LOW_PRESSURE_LINE': 
                # Avaus matalapaineväylälle nollaa yhtäjaksoisen ylipainerasituksen ja purkaa latenssin
                pressure_state = "LOW_PRESSURE"
                vessel_fluid_units = max(0, vessel_fluid_units - current_hold_latency)
                high_pressure_duration = 0
                idle_streak = 0
                
            elif tag in ['BATCH_SHUTDOWN', 'COMPLETED_LOCK_HALT', 'FINAL_SYSTEM_EVACUATION', 'INERT_WASTE_FLAG']:
                # Hallitut alasajot nollaavat dynaamiset aikajaksot ja painerekisterit perustilaan
                high_pressure_duration = idle_streak = 0
                if tag == 'COMPLETED_LOCK_HALT': 
                    pressure_state = "PRESSURE_LOCK"
                else:
                    vessel_fluid_units, pressure_state = 0, "IDLE"
                    if tag == 'FINAL_SYSTEM_EVACUATION': 
                        system_initialized = False
                    
            duration_txt = f"{current_hold_latency}x Viive"
            status_text = "RISTIRIITA:" + error_msg if is_error_step else "Mekaaninen vaihe OK."
            log_lines.append(f"Askel {step:05d} | {token:<15} | {tag:<26} | {vessel_fluid_units:<4} | {pressure_state:<12} | {status_text} ({duration_txt})")
            
    return logical_contradictions, log_lines
# =================================================================================
# MONTE CARLO -TAUSTASIMULAATTORI JA FILERAPORTOINTI
# =================================================================================

def run_silent_simulation(tokens_with_locus):
    """
    Kevyt taustasimulaatioversio satunnaisdatan mittaukseen ilman muistivuotoja.
    Ohjelmoitu rullaamaan ilman I/O-kirjoitusta prosessointinopeuden maksimoimiseksi.
    """
    system_initialized = False   # Kylmäkäynnistyksen boolean-salpa taustasimulaatiolle
    vessel_fluid_units = 0        # Nestemassan puskurirekisteri (REG V)
    pressure_state = "IDLE"       # Putkiston senhetkinen painetila
    logical_contradictions = 0    # Havaittujen loogisten fysiikkaristiriitojen laskuri
    high_pressure_duration = 0    # Yhtäjaksoisen ylipaineen aikajaksojen aikalaskuri
    idle_streak = 0               # Joutokäynnin / passiivisen linjapidon latenssiputki
    last_folio = None             # Edellisen käsitellyn sivun seuranta
    
    for raw_token, folio in tokens_with_locus:
        # Paloitellaan agglutinaatiot ja mitataan latenssikertoimet
        sub_tokens = tokenize_and_split_with_multiplier(raw_token)
        for token, multiplier in sub_tokens:
            
            # --- LOHKORESETOINTI SIVUN VAIHTUESSA ---
            if folio and last_folio and folio != last_folio:
                system_initialized, vessel_fluid_units, pressure_state, high_pressure_duration, idle_streak = False, 0, "IDLE", 0, 0
            if folio: last_folio = folio
            
            tag = parse_token(token)
            if tag == "UNKNOWN": continue
            
            # --- ALUSTUS- JA SYSTEM RESETH -PULSSIT ---
            if token in ["tsheos", "potchokor", "osar", "daiin"]:
                system_initialized, vessel_fluid_units, pressure_state, high_pressure_duration, idle_streak = True, 4, "LOW_PRESSURE", 0, 0
                continue
                
            # --- COLD START PROTOCOLLA ---
            if not system_initialized:
                if tag not in ['INIT_ACTIVATION', 'SYSTEM_REBOOT', 'CHANNEL_ADDRESS_HOLD', 'PHASE_CONVERSION_HOLD', 'GRAVITY_FEED_HOLD', 'BUS_CHANNEL_SELECT', 'TERMINAL_RESTRICTOR', 'PASSIVE_JUNCTION_HOLD', 'LOW_PRESSURE_VALVE_LOCK', 'INERT_WASTE_FLAG']:
                    logical_contradictions += 1
                    continue
            
            current_hold_latency = multiplier
            
            # --- FYSIIKKAMOOTTORIN TAUSTALASKENTA ---
            if tag in ['INIT_ACTIVATION', 'SYSTEM_REBOOT', 'VALVE_CALIBRATION', 'SEDIMENT_SETTLING']:
                system_initialized = True
                if pressure_state == "IDLE": pressure_state = "LOW_PRESSURE"
                if tag in ['SYSTEM_REBOOT', 'SEDIMENT_SETTLING']:
                    idle_streak += current_hold_latency
                    if idle_streak > MAX_IDLE_STREAK: logical_contradictions += 1
                else: idle_streak = 0
            elif tag in ['CHANNEL_ADDRESS_HOLD', 'PHASE_CONVERSION_HOLD', 'GRAVITY_FEED_HOLD', 'BUS_CHANNEL_SELECT', 'TERMINAL_RESTRICTOR', 'PASSIVE_JUNCTION_HOLD', 'LOW_PRESSURE_VALVE_LOCK']:
                if pressure_state == "IDLE": pressure_state = "LOW_PRESSURE"
                idle_streak += current_hold_latency
                if idle_streak > MAX_IDLE_STREAK: logical_contradictions += 1
            elif tag == 'CONTAINMENT_RECEPTACLE': 
                vessel_fluid_units = vessel_fluid_units + (2 * current_hold_latency)
                idle_streak = 0
            elif tag in ['HYDROSTATIC_PUMP_UP', 'PRESSURE_BOOST_THROTTLE', 'PRESSURIZED_CALIBRATION', 'CLOSED_HIGH_PRESSURE_LINE', 'HIGH_PRESSURE_OVERRIDE', 'ACTIVE_UPWARD_VECTOR', 'CHECK_VALVE_ISOLATION']:
                if vessel_fluid_units <= 0: logical_contradictions += 1
                pressure_state = "HIGH_PRESSURE"
                vessel_fluid_units = max(0, vessel_fluid_units - current_hold_latency)
                idle_streak = 0
                high_pressure_duration += current_hold_latency
                if high_pressure_duration > MAX_HIGH_PRESSURE_DURATION: logical_contradictions += 1
            elif tag == 'THERMAL_INFUSION':
                if vessel_fluid_units <= 0 and pressure_state == "HIGH_PRESSURE": logical_contradictions += 1
                pressure_state = "THERMAL_VAPOR"
                vessel_fluid_units = max(0, vessel_fluid_units - current_hold_latency)
                idle_streak = 0
                high_pressure_duration = 0
            elif tag == 'OPEN_LOW_PRESSURE_LINE': 
                pressure_state, vessel_fluid_units, high_pressure_duration, idle_streak = "LOW_PRESSURE", max(0, vessel_fluid_units - current_hold_latency), 0, 0
            elif tag in ['BATCH_SHUTDOWN', 'COMPLETED_LOCK_HALT', 'FINAL_SYSTEM_EVACUATION', 'INERT_WASTE_FLAG']:
                high_pressure_duration = idle_streak = 0
                if tag == 'COMPLETED_LOCK_HALT': pressure_state = "PRESSURE_LOCK"
                else:
                    vessel_fluid_units, pressure_state = 0, "IDLE"
                    if tag == 'FINAL_SYSTEM_EVACUATION': system_initialized = False
    return logical_contradictions

def process_stress_test(filepath):
    """
    Lataa kohde-korpuksen, tyhjentää muistin, ajaa aidon aineiston sekvenssin
    sekä suorittaa 1 000 sokeaa Monte Carlo -ajoa tilastolliselle alahännälle.
    """
    if not os.path.exists(filepath): return
    print(f"Ladataan kohde-korpusta: '{filepath}'...")
    
    # MATEMAATTINEN TÄYDELLINEN MUISTIPUHDISTUS ALUSSA
    tokens_with_locus = []
    current_locus_folio = None
    
    # Puretaan tiedosto muistiin
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            tokens, folio = clean_and_extract_tokens(line)
            if folio: current_locus_folio = folio
            for t in tokens: tokens_with_locus.append((t, current_locus_folio))
            
    total_words = len(tokens_with_locus)
    if total_words == 0: return
    print(f"Puhdistus valmis. Käsitellään {total_words:,} genuine-tokenia...")
    
    # 1. Ajetaan aito teksti dynaamisen fysiikka- ja latenssimoottorin läpi
    orig_errors, visual_logs = run_simulation_with_logging(tokens_with_locus)
    actual_steps = len(visual_logs)
    orig_compliance = ((actual_steps - orig_errors) / actual_steps * 100) if actual_steps > 0 else 0
    
    # 2. Käynnistetään vankka Monte Carlo -kontrollitestaus sokeille permutaatioille
    iterations = 1000
    print(f"Käynnistetään {iterations:,} iteraation sokea sekoitusajo kontrolliryhmälle...")
    shuffled_errors = []
    rng = random.Random(1337) # Lukitaan siemen matemaattisen toistettavuuden takeeksi
    
    for idx in range(iterations):
        shuffled_list = tokens_with_locus.copy()
        rng.shuffle(shuffled_list)
        errors = run_silent_simulation(shuffled_list)
        shuffled_errors.append(errors)
        
    avg_shuffled_errors, min_shuffled, max_shuffled = sum(shuffled_errors) / iterations, min(shuffled_errors), max(shuffled_errors)
    p_value = (sum(x <= orig_errors for x in shuffled_errors) + 1) / (iterations + 1)
    
    # --- TALLENNETAAN TÄYDELLINEN SIISTI AKATEEMINEN RAPORTTI LEVYLLE ---
    output_report_name = "vfsf_stress_test_report.txt"
    with open(output_report_name, 'w', encoding='utf-8') as out_f:
        out_f.write("="*125 + "\n")
        out_f.write(" VFSF GLOBAL STRESS TESTER v3.7.2 — MATEMAATTINEN TELEMETRIALOKI JA TILASTORAPORTTI\n")
        out_f.write(" Tekijäoikeus (C) 2026 Juho Olavi Laakso (Paimio, Finland) | MIT License\n")
        out_f.write("="*125 + "\n")
        out_f.write(f" Käsitelty syötetiedosto:                  {filepath}\n")
        out_f.write(f" Käsittelymassa yhteensä (Tokens):         {total_words:,} kpl\n")
        out_f.write(f" Prosessivaiheita halkaisujen jälkeen:     {actual_steps:,} kpl\n")
        out_f.write("="*125 + "\n")
        out_f.write(" SEURAAVA ON AIDON TEKSTIN TILA-AJO SEKVENSSI SIVUKOHTAISELLA LOHKORESETOINNILLA:\n")
        out_f.write("-" * 125 + "\n")
        out_f.write(f"{'ASKEL':<11} | {'TOKEN':<15} | {'LAITETAGI / OPERAATTORI':<26} | {'REG':<4} | {'PAINETILA':<12} | {'SUORITUSLOKI / STATUS'}\n")
        out_f.write("-" * 125 + "\n")
        for line in visual_logs: out_f.write(line + "\n")
        out_f.write("-" * 125 + "\n\n")
        
        out_f.write("="*85 + "\n")
        out_f.write(" MONTE CARLO STRESSITESTIN LOPPUTIIVISTELMÄ\n")
        out_f.write("="*85 + "\n")
        out_f.write(f" AITO KÄSIKIRJOITUKSEN JÄRJESTYS:\n")
        out_f.write(f"  - Havaitut loogiset ristiriidat:         {orig_errors:,} kpl\n")
        out_f.write(f"  - Rakennekonvergenssi (Yhteensopivuus):  {orig_compliance:.2f} %\n")
        out_f.write("-" * 85 + "\n")
        out_f.write(f" SEKOITETTU KONTROLLIRYHMÄ ({iterations:,} puhdistettua parisekoitusta):\n")
        out_f.write(f"  - Keskimääräinen virhemäärä kohinassa:    {avg_shuffled_errors:.2f} kpl per ajo\n")
        out_f.write(f"  - Minimivirhe satunnaisuudessa:          {min_shuffled:,} kpl\n")
        out_f.write(f"  - Maksimivirhe satunnaisuudessa:          {max_shuffled:,} kpl\n")
        out_f.write("-" * 85 + "\n")
        out_f.write(f" YKSISUUNTAISEN TESTAUKSEN p-ARVO (Empirical p-value): {p_value:.6f}\n")
        out_f.write(f" -> TULOS: ")
        if p_value < 0.05:
            out_f.write("ERITTÄIN MERKITSEVÄ (Highly Significant). Sattumateoria globaalisti kumottu.\n")
        else:
            out_f.write("EI TILASTOLLISESTI MERKITSEVÄ GLOBAALISSA PUTKESSA. Vaatii lohkosäätöä.\n")
        out_f.write("="*85 + "\n")
        
    print(f"\n[VALMIS v3.7.2]: Täydellinen master-raportti kommentoituna tallennettu tiedostoon '{output_report_name}'")

if __name__ == "__main__":
    if len(sys.argv) > 1: 
        process_stress_test(sys.argv[1])
    else:
        print("Käyttö: python vfsf_global_tester_v372.py <tiedostonnimi.txt>")
