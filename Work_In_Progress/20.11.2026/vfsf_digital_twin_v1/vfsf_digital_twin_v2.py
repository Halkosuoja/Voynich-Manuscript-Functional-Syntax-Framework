#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2026 Juho Olavi Laakso
# SPDX-License-Identifier: MIT
"""
VFSF Virtual Reactor Simulator (Digital Twin) v2.0
Eriytetyt lämpötila-alueet (reaktori vs. lauhdutin) + Monte Carlo -kontrollitesti.
"""
import re
import sys
import os
import random
from collections import defaultdict

# Järjestetty pisimmästä avaimesta lyhyimpään, kuten v3.8.2-testissä
OPERATOR_MAP = [
    ('qokch', 'PRESSURE_CALIBRATE'),
    ('qokain', 'FLUSH_SYSTEM'),
    ('qotal', 'THROTTLE_PRESSURE'),
    ('qokor', 'EMERGENCY_VENT'),
    ('pched', 'OPEN_INTAKE'),
    ('ckhhey', 'CLOSE_CHECK_VALVE'),
    ('chcthy', 'ADJUST_VALVES'),
    ('daiin', 'LOCK_SYSTEM'),
    ('dair', 'FILL_FEED_BASIN'),
    ('dar', 'FILL_FEED_BASIN'),
    ('dal', 'PUMP_UP_TO_REACTOR'),
    ('dol', 'GRAVITY_DRAIN_TO_RECEIVER'),
    ('cfh', 'JET_INJECT'),
    ('cph', 'CROSS_FLOW_BALANCE'),
    ('cthey', 'HEAT_REACTOR'),
    ('cthy', 'HEAT_REACTOR'),
    ('cth', 'HEAT_REACTOR'),
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
    def __init__(self):
        self.feed_basin = 20.0
        self.reactor_fluid = 0.0
        self.condenser_vapor = 0.0
        self.product_yield = 0.0

        self.reactor_temp_c = 20.0
        self.condenser_temp_c = 20.0
        self.pressure_bar = 1.0
        self.max_pressure_bar = 1.0
        self.valves_locked = False

        self.safety_alerts = 0
        self.burst_risk = False
        self.dry_boil_risk = False

    def apply_physics_tick(self, multiplier):
        for _ in range(multiplier):
            # Reaktori ja lauhdutin jäähtyvät hitaasti kohti ympäristön lämpöä
            if self.reactor_temp_c > 20.0:
                self.reactor_temp_c = max(20.0, self.reactor_temp_c - 1.5)
            if self.condenser_temp_c > 20.0:
                self.condenser_temp_c = max(20.0, self.condenser_temp_c - 2.0)

            # Avoimet venttiilit tasaavat painetta luonnollisesti
            if not self.valves_locked and self.pressure_bar > 1.0:
                self.pressure_bar = max(1.0, self.pressure_bar - 0.25)

            # Höyrystyminen tapahtuu reaktorin lämpötilan mukaan
            if self.reactor_fluid > 0 and self.reactor_temp_c >= 75.0:
                evaporated = min(self.reactor_fluid, 1.5)
                self.reactor_fluid -= evaporated
                self.condenser_vapor += evaporated
                self.pressure_bar += 0.20

            # Tiivistyminen tapahtuu erillisen lauhduttimen lämpötilan mukaan
            if self.condenser_vapor > 0 and self.condenser_temp_c < 65.0:
                condensed = min(self.condenser_vapor, 1.2)
                self.condenser_vapor -= condensed
                self.product_yield += condensed
                self.pressure_bar = max(1.0, self.pressure_bar - 0.10 * condensed)

            self.max_pressure_bar = max(self.max_pressure_bar, self.pressure_bar)

            if self.pressure_bar > 4.5:
                self.burst_risk = True
                self.safety_alerts += 1
            if self.reactor_fluid <= 0.1 and self.reactor_temp_c > 85.0:
                self.dry_boil_risk = True
                self.safety_alerts += 1

    def execute_command(self, action, multiplier):
        note = "OK"

        if action == 'FILL_FEED_BASIN':
            self.feed_basin = min(100.0, self.feed_basin + 5.0 * multiplier)
            note = "Syöttöallasta täytetty"

        elif action in ('PUMP_UP_TO_REACTOR', 'OPEN_INTAKE', 'JET_INJECT'):
            self.valves_locked = False
            transfer = min(self.feed_basin, 3.0 * multiplier)
            if transfer > 0:
                self.feed_basin -= transfer
                self.reactor_fluid = min(50.0, self.reactor_fluid + transfer)
                self.pressure_bar += 0.15 * multiplier
                note = f"Siirretty {transfer:.1f} yks. reaktoriin"
            else:
                note = "VAROITUS: Syöttöallas tyhjä"

        elif action == 'GRAVITY_FEED':
            if not self.valves_locked:
                transfer = min(self.feed_basin, 1.0 * multiplier)
                self.feed_basin -= transfer
                self.reactor_fluid = min(50.0, self.reactor_fluid + transfer)
                note = "Painovoimainen syöttö"
            else:
                note = "Syöttö estetty (venttiilit lukossa)"

        elif action == 'HEAT_REACTOR':
            self.reactor_temp_c = min(120.0, self.reactor_temp_c + 18.0 * multiplier)
            self.pressure_bar += 0.25 * multiplier
            note = "Reaktoria lämmitetty"

        elif action == 'COOL_CONDENSER':
            self.condenser_temp_c = max(15.0, self.condenser_temp_c - 15.0 * multiplier)
            self.pressure_bar = max(1.0, self.pressure_bar - 0.20 * multiplier)
            if self.condenser_vapor > 0:
                condensed = min(self.condenser_vapor, 2.5 * multiplier)
                self.condenser_vapor -= condensed
                self.product_yield += condensed
            note = "Lauhdutinta jäähdytetty"

        elif action in ('BOOST_PRESSURE', 'SEAL_HIGH_PRESSURE', 'CLOSE_CHECK_VALVE'):
            self.valves_locked = True
            self.pressure_bar += 0.40 * multiplier
            note = "Korkeapaine lukittu"

        elif action in ('THROTTLE_PRESSURE', 'ADJUST_VALVES', 'PRESSURE_CALIBRATE'):
            self.pressure_bar = max(1.0, self.pressure_bar - 0.15 * multiplier)
            note = "Painetta kuristettu/säädetty"

        elif action in ('RESET_VALVES', 'BYPASS_FLOW', 'CROSS_FLOW_BALANCE'):
            self.valves_locked = False
            self.pressure_bar = max(1.0, self.pressure_bar - 0.35 * multiplier)
            note = "Ohivirtaus / venttiilit avattu"

        elif action in ('OPEN_LOW_PRESSURE', 'EMERGENCY_VENT', 'OPEN_DRAIN', 'FLUSH_SYSTEM'):
            self.valves_locked = False
            self.pressure_bar = max(1.0, self.pressure_bar - 0.80 * multiplier)
            note = "Paine vapautettu"

        elif action == 'GRAVITY_DRAIN_TO_RECEIVER':
            self.valves_locked = False
            if self.condenser_vapor > 0:
                drained = min(self.condenser_vapor, 2.0 * multiplier)
                self.condenser_vapor -= drained
                self.product_yield += drained
            note = "Painovoimainen valuma keräysastiaan"

        elif action == 'LOCK_SYSTEM':
            self.valves_locked = True
            self.feed_basin = max(self.feed_basin, 15.0)
            note = "Järjestelmä lukittu sykliin"

        self.apply_physics_tick(multiplier)

        if self.pressure_bar > 4.5:
            note = "HÄLYTYS: Ylipaineriski (>4.5 bar)!"
        elif self.reactor_fluid <= 0.1 and self.reactor_temp_c > 85.0:
            note = "HÄLYTYS: Reaktorin kuivakeitto!"

        return note


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
            if cleaned == key:
                return action, mult
        else:
            if key in cleaned:
                return action, mult
    return 'HOLD_STATE', mult


def load_tokens_with_locus(filepath):
    tokens_with_locus = []
    current_folio = "default"
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            raw = line.strip()
            if not raw or raw.startswith('#'):
                continue
            locus_match = re.search(r'<f(\d+[rv]\d*)', raw.lower())
            if locus_match:
                current_folio = locus_match.group(1)
            clean = re.sub(r'<[^>]+>|\{[^}]+\}|\[[^\]]+\]|@[0-9;]+', '', raw)
            clean = re.sub(r'[{}\[\]!@%<>?:*#$,=+\-\'’]', ' ', clean)
            words = [w.strip() for w in re.split(r'[\s.]+', clean)
                     if w and not re.match(r'^f\d+[rv]\d*$', w.lower())]
            for w in words:
                tokens_with_locus.append((w, current_folio))
    return tokens_with_locus


def simulate_sequence(tokens_with_locus, print_log=False):
    rig = VirtualDistillationRig()
    last_folio = None

    if print_log:
        print("-" * 122)
        print(f"{'ASKEL':<6} | {'SANA':<12} | {'TOIMENPIDE':<25} | {'ALLAS':<5} | {'REAKT':<5} | {'R.LÄMPÖ':<7} | {'L.LÄMPÖ':<7} | {'PAINE':<7} | {'TUOTTO':<6} | {'TILA'}")
        print("-" * 122)

    for step, (word, folio) in enumerate(tokens_with_locus, 1):
        if last_folio is not None and folio != last_folio:
            rig.valves_locked = False
            rig.pressure_bar = 1.0
        last_folio = folio

        action, mult = parse_word(word)
        note = rig.execute_command(action, mult)

        if print_log:
            print(f"{step:05d}  | {word:<12} | {action:<25} | {rig.feed_basin:5.1f} | {rig.reactor_fluid:5.1f} | "
                  f"{rig.reactor_temp_c:5.1f}°C | {rig.condenser_temp_c:5.1f}°C | {rig.pressure_bar:4.2f}bar | "
                  f"{rig.product_yield:6.1f} | {note}")

    if print_log:
        print("-" * 122)
    return rig


def shuffle_within_folios(tokens_with_locus, rng):
    groups = defaultdict(list)
    order = []
    for word, folio in tokens_with_locus:
        if folio not in groups:
            order.append(folio)
        groups[folio].append(word)

    shuffled = []
    for folio in order:
        words = groups[folio].copy()
        rng.shuffle(words)
        for w in words:
            shuffled.append((w, folio))
    return shuffled


def main(filepath, iterations=1000):
    if not os.path.exists(filepath):
        print(f"Virhe: Tiedostoa '{filepath}' ei löydy.")
        return

    tokens_with_locus = load_tokens_with_locus(filepath)
    if not tokens_with_locus:
        print("Virhe: Tiedostosta ei löytynyt luettavia tokeneita.")
        return

    print(f"\nAjetaan Digital Twin v2.0 tiedostolle '{filepath}' ({len(tokens_with_locus)} käskyä)...")
    real_rig = simulate_sequence(tokens_with_locus, print_log=True)

    rng = random.Random(1337)
    mc_alerts, mc_max_p, mc_yields = [], [], []

    for _ in range(iterations):
        shuf = shuffle_within_folios(tokens_with_locus, rng)
        r = simulate_sequence(shuf, print_log=False)
        mc_alerts.append(r.safety_alerts)
        mc_max_p.append(r.max_pressure_bar)
        mc_yields.append(r.product_yield)

    p_alerts = (sum(x <= real_rig.safety_alerts for x in mc_alerts) + 1) / (iterations + 1)
    p_pressure = (sum(x <= real_rig.max_pressure_bar for x in mc_max_p) + 1) / (iterations + 1)
    p_yield = (sum(x >= real_rig.product_yield for x in mc_yields) + 1) / (iterations + 1)

    print("\n" + "=" * 76)
    print(" DIGITAL TWIN v2.0 + MONTE CARLO -YHTEENVETO")
    print("=" * 76)
    print(f" AITO JÄRJESTYS:")
    print(f"  - Valmis tuotto (yield):        {real_rig.product_yield:.2f} yksikköä")
    print(f"  - Huippupaine / Loppupaine:     {real_rig.max_pressure_bar:.2f} / {real_rig.pressure_bar:.2f} bar")
    print(f"  - Turvallisuushälytykset:       {real_rig.safety_alerts} kpl")
    print("-" * 76)
    print(f" MONTE CARLO ({iterations} sivunsisäistä sekoitusta):")
    print(f"  - Hälytysten ka. (min-max):     {sum(mc_alerts)/iterations:.2f} ({min(mc_alerts)}-{max(mc_alerts)}) | p = {p_alerts:.4f}")
    print(f"  - Huippupaineen ka. (min-max):  {sum(mc_max_p)/iterations:.2f} ({min(mc_max_p):.2f}-{max(mc_max_p):.2f}) | p = {p_pressure:.4f}")
    print(f"  - Tuoton ka. (min-max):         {sum(mc_yields)/iterations:.2f} ({min(mc_yields):.2f}-{max(mc_yields):.2f}) | p = {p_yield:.4f}")
    print("=" * 76)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Käyttö: python vfsf_digital_twin_v2.py <tiedostonnimi.txt>")