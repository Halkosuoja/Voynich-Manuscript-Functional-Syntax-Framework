#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===================================================================================
THE VFSF VIRTUAL REACTOR SIMULATOR (DIGITAL TWIN) v1.0
===================================================================================
Tekijä: Juho Olavi Laakso (Paimio, Finland)
Konteksti: Voynich Manuscript Functional Syntax Framework (VFSF)
Lisenssi: MIT License (Copyright (c) 2026 Juho Olavi Laakso)
Kuvaus:
    Simuloi 1400-luvun monivaiheista tislaus- ja uuttolaitteistoa.
    Kääntää Voynich-käsikirjoituksen EVA-transkription fyysisiksi venttiili-,
    paine- ja lämpötilakäskyiksi ja mittaa valmiin tisleen tuottoa sekä
    laitteiston turvallisuutta (ylipaine ja kuivakeitto).
===================================================================================
"""
import re
import sys
import os

# Ydinoperaattorien yhdistäminen virtuaalilaitteiston toimilaitteisiin
OPERATOR_MAP = [
    ('qokch', 'PRESSURE_CALIBRATE'),
    ('qokain', 'FLUSH_SYSTEM'),
    ('qotal', 'THROTTLE_PRESSURE'),
    ('qokor', 'EMERGENCY_VENT'),
    ('pched', 'OPEN_INTAKE'),
    ('daiin', 'LOCK_SYSTEM'),
    ('ckhhey', 'CLOSE_CHECK_VALVE'),
    ('chcthy', 'ADJUST_VALVES'),
    ('dair', 'FILL_FEED_BASIN'),
    ('dar', 'FILL_FEED_BASIN'),
    ('dal', 'PUMP_UP_TO_REACTOR'),
    ('dol', 'GRAVITY_DRAIN_TO_RECEIVER'),
    ('cfh', 'JET_INJECT'),
    ('cph', 'CROSS_FLOW_BALANCE'),
    ('cthy', 'HEAT_REACTOR'),
    ('ched', 'COOL_CONDENSER'),
    ('chey', 'COOL_CONDENSER'),
    ('shol', 'RESET_VALVES'),
    ('shey', 'RESET_VALVES'),
    ('shdy', 'RESET_VALVES'),
    ('dain', 'OPEN_LOW_PRESSURE'),
    ('qok', 'BOOST_PRESSURE'),
    ('qot', 'THROTTLE_PRESSURE'),
    ('or', 'COOL_CONDENSER'),
    ('ar', 'SETTLE_SEDIMENT'),
    ('al', 'PUMP_UP_TO_REACTOR'),
    ('aiin', 'SEAL_HIGH_PRESSURE'),
    ('ol', 'BYPASS_FLOW'),
    ('ch', 'HOLD_STATE'),
    ('sh', 'RESET_VALVES'),
    ('ot', 'GRAVITY_FEED'),
    ('ok', 'HOLD_STATE'),
    ('y', 'HOLD_STATE'),
    ('d', 'HOLD_STATE'),
    ('o', 'GRAVITY_FEED'),
    ('l', 'OPEN_DRAIN')
]

class VirtualDistillationRig:
    """ Virtuaalinen 1400-luvun tislaus- ja uuttolaitteisto fysiikkalakeineen """
    def __init__(self):
        self.feed_basin = 20.0      # Syöttöaltaan nestemäärä (yksikköä)
        self.reactor_fluid = 0.0    # Pääreaktorin nestemäärä (yksikköä)
        self.condenser_vapor = 0.0  # Lauhduttimessa oleva höyry (yksikköä)
        self.product_yield = 0.0    # Valmis kerätty tisle / uute (yksikköä)
        
        self.temp_c = 20.0          # Reaktorin lämpötila (°C)
        self.pressure_bar = 1.0     # Järjestelmän paine (bar)
        self.valves_locked = False  # Pääsulkuventtiilin tila
        
        self.safety_alerts = 0      # Kriittisten vaaratilanteiden laskuri
        self.burst_risk = False     # Lasiastian halkeamisriski (paine > 4.5 bar)
        self.dry_boil_risk = False  # Kuivakeittoriski (lämpö > 90 °C ilman nestettä)

    def apply_physics_tick(self, multiplier):
        """ Laskee luonnollisen fysiikan (jäähtyminen, tiivistyminen) joka askeleella """
        for _ in range(multiplier):
            # Luonnollinen jäähtyminen kohti huoneenlämpöä (20 °C)
            if self.temp_c > 20.0:
                self.temp_c = max(20.0, self.temp_c - 2.5)
            
            # Paineen tasaantuminen, jos venttiilit eivät ole täysin lukittuina
            if not self.valves_locked and self.pressure_bar > 1.0:
                self.pressure_bar = max(1.0, self.pressure_bar - 0.15)
                
            # Höyrystyminen, jos reaktorissa on nestettä ja lämpö yli 75 °C
            if self.reactor_fluid > 0 and self.temp_c >= 75.0:
                evaporated = min(self.reactor_fluid, 1.5)
                self.reactor_fluid -= evaporated
                self.condenser_vapor += evaporated
                self.pressure_bar += 0.25

            # Lauhtuminen nesteeksi, jos lauhduttimessa on höyryä ja lämpö alle 65 °C
            if self.condenser_vapor > 0 and self.temp_c < 65.0:
                condensed = min(self.condenser_vapor, 1.2)
                self.condenser_vapor -= condensed
                self.product_yield += condensed

            # Turvallisuusrajat
            if self.pressure_bar > 4.5:
                self.burst_risk = True
                self.safety_alerts += 1
            if self.reactor_fluid <= 0.1 and self.temp_c > 85.0:
                self.dry_boil_risk = True
                self.safety_alerts += 1
    def execute_command(self, action, multiplier):
        """ Suorittaa Voynich-tekstistä käännetyn fyysisen toimenpiteen """
        status_note = "OK"
        
        if action == 'FILL_FEED_BASIN':
            self.feed_basin = min(100.0, self.feed_basin + (5.0 * multiplier))
            status_note = "Syöttöallasta täytetty"
            
        elif action == 'PUMP_UP_TO_REACTOR':
            self.valves_locked = False
            transfer = min(self.feed_basin, 3.0 * multiplier)
            if transfer > 0:
                self.feed_basin -= transfer
                self.reactor_fluid = min(50.0, self.reactor_fluid + transfer)
                self.pressure_bar += 0.2 * multiplier
                status_note = f"Siirretty {transfer:.1f} yks. reaktoriin"
            else:
                status_note = "VAROITUS: Syöttöallas tyhjä!"
                
        elif action == 'HEAT_REACTOR':
            self.temp_c = min(120.0, self.temp_c + (15.0 * multiplier))
            self.pressure_bar += 0.3 * multiplier
            status_note = "Reaktoria lämmitetty"
            
        elif action == 'COOL_CONDENSER':
            self.temp_c = max(20.0, self.temp_c - (18.0 * multiplier))
            self.pressure_bar = max(1.0, self.pressure_bar - 0.3 * multiplier)
            # Kylmä lauhdutin tiivistää höyryä tehokkaasti
            if self.condenser_vapor > 0:
                condensed = min(self.condenser_vapor, 2.5 * multiplier)
                self.condenser_vapor -= condensed
                self.product_yield += condensed
            status_note = "Lauhdutinta jäähdytetty"
            
        elif action == 'BOOST_PRESSURE' or action == 'SEAL_HIGH_PRESSURE':
            self.valves_locked = True
            self.pressure_bar += 0.45 * multiplier
            status_note = "Korkeapaine lukittu"
            
        elif action == 'OPEN_LOW_PRESSURE' or action == 'EMERGENCY_VENT' or action == 'OPEN_DRAIN':
            self.valves_locked = False
            self.pressure_bar = max(1.0, self.pressure_bar - 0.8 * multiplier)
            status_note = "Paine vapautettu"
            
        elif action == 'GRAVITY_DRAIN_TO_RECEIVER':
            self.valves_locked = False
            if self.condenser_vapor > 0:
                drained = min(self.condenser_vapor, 2.0 * multiplier)
                self.condenser_vapor -= drained
                self.product_yield += drained
            status_note = "Painovoimainen valuma keräysastiaan"
            
        elif action == 'LOCK_SYSTEM':
            self.valves_locked = True
            self.feed_basin = max(self.feed_basin, 15.0) # Varmistaa perussyötön
            status_note = "Järjestelmä lukittu sykliin"

        # Ajetaan fysiikkamoottori askeleen lopuksi
        self.apply_physics_tick(multiplier)
        
        if self.pressure_bar > 4.5:
            status_note = "HÄLYTYS: Ylipaineriski (>4.5 bar)!"
        elif self.reactor_fluid <= 0.1 and self.temp_c > 85.0:
            status_note = "HÄLYTYS: Reaktorin kuivakeitto!"
            
        return status_note

def parse_word(word):
    cleaned = word.lower()
    mult = 1
    if 'eee' in cleaned:
        mult = 3
        cleaned = cleaned.replace('eee', '', 1)
    elif 'ee' in cleaned:
        mult = 2
        cleaned = cleaned.replace('ee', '', 1)
        
    for key, action in OPERATOR_MAP:
        if len(key) == 1:
            if cleaned == key: return action, mult
        else:
            if key in cleaned: return action, mult
    return 'HOLD_STATE', mult

def run_virtual_rig(filepath):
    if not os.path.exists(filepath):
        print(f"Virhe: Tiedostoa '{filepath}' ei löydy.")
        return

    rig = VirtualDistillationRig()
    tokens = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            clean = re.sub(r'<[^>]+>|\{[^}]+\}|\[[^\]]+\]|@[0-9;]+', '', line)
            clean = re.sub(r'[{}\[\]!@%<>?:*#$,=+\-\'’]', ' ', clean)
            words = [w.strip() for w in re.split(r'[\s.]+', clean) if w and not re.match(r'^f\d+[rv]$', w.lower())]
            tokens.extend(words)

    print(f"\nKäynnistetään virtuaalilaitteiston ajo: '{filepath}' ({len(tokens)} käskyä)...")
    print("-" * 115)
    print(f"{'ASKEL':<7} | {'SANA':<12} | {'TOIMENPIDE':<25} | {'ALLAS':<6} | {'REAKT.':<6} | {'LÄMPÖ':<7} | {'PAINE':<7} | {'TUOTTO':<6} | {'TILA'}")
    print("-" * 115)

    for step, word in enumerate(tokens, 1):
        action, mult = parse_word(word)
        note = rig.execute_command(action, mult)
        print(f"{step:05d}   | {word:<12} | {action:<25} | {rig.feed_basin:5.1f}  | {rig.reactor_fluid:5.1f}  | {rig.temp_c:5.1f}°C | {rig.pressure_bar:4.2f}bar | {rig.product_yield:5.1f}  | {note}")

    print("-" * 115)
    print("\n" + "="*70)
    print(" VIRTUAALILAITTEISTON LOPPURAPORTTI (DIGITAL TWIN SUMMARY)")
    print("="*70)
    print(f" Valmiin tisleen / uutteen kokonaistuotto:  {rig.product_yield:.2f} yksikköä")
    print(f" Reaktorin loppulämpötila ja -paine:        {rig.temp_c:.1f} °C / {rig.pressure_bar:.2f} bar")
    print(f" Turvallisuushälytykset ajon aikana:        {rig.safety_alerts} kpl")
    print(f" Lasiastian halkeamisriski (Ylipaine):      {'KYLLÄ (Kriittinen)' if rig.burst_risk else 'EI (Turvallinen)'}")
    print(f" Kuivakeittoriski (Tyhjä reaktori):         {'KYLLÄ (Kriittinen)' if rig.dry_boil_risk else 'EI (Turvallinen)'}")
    print("="*70)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_virtual_rig(sys.argv[1])
    else:
        print("Käyttö: python vfsf_digital_twin_v1.py <tiedostonnimi.txt>")
