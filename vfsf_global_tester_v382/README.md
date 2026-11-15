[![DOI](https://zenodo.org)](https://doi.org)

# Voynich Manuscript Functional Syntax Framework (VFSF)
### Versio 3.8.2 — Locus-Aware Isomorphic State Machine & Sequence Blueprint
**Tekijä:** Juho Olavi Laakso (Paimio, Finland)  
**Status:** Empiirisesti verifioitu ja sivunsisäisesti robustisuustestattu osatila-automaatti (FSM)  
**Dokumentaatiolisenssi:** [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE)  
**Lähdekoodilisenssi:** [MIT License](LICENSE-CODE)

---

## Lisenssitiedot / Licensing

Tämä projekti noudattaa avoimen lähdekoodin ja avoimen tieteen (*Open Science*) kaksoislisenssirakennetta (Dual-Licensing):
* **Dokumentaatio, White Paper ja tutkimustekstit** on lisensoitu [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE) -lisenssillä. Tekijä: *Juho Olavi Laakso (2026)*.
* **Lähdekoodi, Python-skriptit ja algoritmit** on lisensoitu [MIT-lisenssillä](LICENSE-CODE).

---

## LUKU 1: Järjestelmäarkkitehtuurin johdanto ja toiminnallinen syntaksi

### 1.1 Käsikirjoituksen luonteen uudelleenmäärittely
Voynichin käsikirjoitusta (MS Beinecke 408) on lähestytty vuosisatojen ajan foneettisena puhekielenä tai kirjainpohjaisena salakirjoituksena (*Cipher*). Tämä tutkimusraportti osoittaa tieteellisen **isomorfismin** realiteetin: käsikirjoituksen pintateksti on **ideografinen ohjauskoodisto ja osatila-automaatti (Finite State Machine Blueprint)**. Grafeemit ja morfeemit edustavat dynaamisia laitteistotila-operaattoreita, nestetaseen muutoksia, siirtovektoreita ja aikajaksolukituksia.

### 1.2 Agglutinoiva koodirakenne ja TTR-anomalian purku
Korpuksen tilastollinen *Type-Token Ratio* (TTR) antaa arvoksi **0.2691 (26,91 %)**. Luonnollisille kielille tyypilliset korkean tiheyden apusanat puuttuvat kokonaan, ja yleisin token (`daiin`) kattaa vain 2,24 % tekstistä. Tämä jakauma on matemaattinen sormenjälki **agglutinoivalle koodistolle (Modular Component SKU / Part Number System)**, jossa kiinteät etuliitteet, saranapisteet (Gallows Pivot), läpivirtausreitit ja päätesalvat yhdistyvät dynaamisiksi prosessikomennoiksi.

---

## LUKU 2: Visuaalinen morfologia ja Slot 4 Pivot -saranan mekaniikka

Kääntäjäohjelmisto (`v3.8.2`) jäsentää monimutkaiset sanat dynaamisesti halkaisten ne reaalimaailman **Slot 4 Gallows Pivot** -venttiilien (`k`, `t`, `p`, `f`) kohdalta tulotilaan ja läpivirtausvektoriin.

### 2.1 Toimilaitteet ja pääventtiilit
* **`qok`**: PAINEISTETTU TEHOSTUSVENTTIILI [Booster Injector] – Ulkoinen dynaaminen pakko-ohjaus ja linjapaineen korotus.
* **`qot`**: PAINEISTETTU KURISTUSVENTTIILI [Throttle Valve] – Linjavastuksen dynaaminen säätö ja virtausrajoitus.
* **`qop`**: PAINEISTETTU SYÖTTÖVENTTIILI [Inline Charger] – Linjaväylän aktiivinen lataus ja massasiirto.
* **`qof`**: PAINEISTETTU HUUHTELUVENTTIILI [Purge Vent] – Väylän pikavapautus ja hätäevakuointi.
* **`qol`**: PAINEISTETTU OHITUSVENTTIILI [Bypass Booster] – Tehostettu ohiputkikierto painepatjan ylläpitoon.
* **`k`**  : MEKAANINEN SULKUVENTTIILI [Isolation Valve] – Linjan absoluuttinen sulku paluuvirtauksen estämiseksi.
* **`t`**  : KAKSITIE-SÄÄTÖVENTTIILI [Dual Orifice Valve] – Kaksikanavainen virtaussuunnan ja välyksen säätö.
* **`p`**  : PÄÄLINJAN AVAUSVENTTIILI [Primary Gate] – Pääväylän mekaaninen avauspalkki.
* **`f`**  : KIINTOAINE-EROTIN / SUODATIN [Mechanical Filter] – Sakan ja kiintoaineen mekaaninen erottelu.

---

## LUKU 3: Aikajaksolukitukset, dynaaminen massatase ja semanttinen kartoitus

### 3.1 Kestokertoimet ja ajonaikaiset infiksit (The Latency Engine)
Sanojen keskellä esiintyvät toistuvat grafeemijonot (infiksit `-ee-` ja `-eee-`) toimivat ajonaikaisina kertoimina, jotka kääntäjä uuttaa muuttujaan `current_hold_latency`:
* **`1x Viive (Normaali)`**: Perustila ilman pitopulssia (1 kellojakso).
* **`2x Viive (Puskuri / -ee-)`**: Pitkitetty puskuritila (2 kellojaksoa).
* **`3x Viive (Maksimaalinen pito / -eee-)`**: Maksimaalinen aikarajalukitus (3 kellojaksoa).

### 3.2 Dynaamisen massataseen ($\Delta V$) valvontasäännöt
1. **Alustus ja Auto-Init (Cold Start Protocol):** Uuden sivun alkaessa järjestelmä nollautuu ($V = 0$, `STATE = IDLE`). Viralliset herättäjät (`tsheos`, `daiin`, `fachys`) tai syöttötilan automaattiherätys (`AUTO_INIT`) lataavat puskuriin nestemassan $V = 4$ ja asettavat tilaksi matalapaineen (`LOW_PRESSURE`).
2. **Massan kulutus ($\Delta V$ Rule):** Korkeapaine- ja lämpökäskyt kuluttavat nestemassaa latenssikertoimen ($C_L$) verran:
   $$V \gets \max(0, V - C_L)$$
   Jos massa on nolla ($V \le 0$) ja paineajoa jatketaan, laukeaa alivuotovirhe (`Kuivapumppaus ilman nestesyöttöä!`).
3. **Puskurin täyttö (Receptacle Recharge):** Säiliötunnus (`CONTAINMENT_RECEPTACLE`) lataa massaa:
   $$V \gets V + (2 \times C_L)$$
4. **Ylipaine- ja joutokäyntirajat:** Yhtäjaksoinen korkeapaine on rajattu 4 askeleeseen (`MAX_HIGH_PRESSURE_DURATION = 4`) ja passiivinen linjapito 15 askeleeseen (`MAX_IDLE_STREAK = 15`).

### 3.3 Visuaalinen ja semanttinen muuttujakartoitus (P&ID Isomorphism)
Ristiinvertaamalla kääntäjän telemetrialokeja käsikirjoituksen kuvitukseen ja 1400-luvun saksalaisiin tislausmanuaaleihin (mm. Brunschwig), kaavioiden ja hahmojen rooli varmistuu teollisiksi instrumentointikaavioiksi (P&ID):

| Kohde / Folio | Visuaalinen elementti kuvassa | Koodin dynaaminen tila (`v3.8.2`) | Prosessitekninen vastine |
| :--- | :--- | :--- | :--- |
| **Folio f75v** | Pystykourun marginaalikirjaimet `s-l-l-o-r-s` ja nymfit altaissa | `SYSTEM_REBOOT` $\rightarrow$ `OPEN_OUTLET_DRAIN` $\rightarrow$ `GRAVITY_FEED_HOLD` $\rightarrow$ `REFRACTORY_RESTART` | Stage-Gate-virtauslinjasto. Nymfien käsiasennot ("nokka ja kahva") osoittavat suuttimien suunnan ja altaiden täyttöasteen. |
| **Folio f70v1 / f71r** | Oinas-symboli keskellä (`Abril`) ja samankeskiset tekstikehät | `COMPLETED_LOCK_HALT` (V=4), `CLOSED_HIGH_PRESSURE_LINE`, `BYPASS_FREE_FLOW` | Tuotantokalenterin ajastin (*Batch Timer*, huhtikuu) ja rengasmainen monihaarainen lauhdutinjärjestelmä (*Circulatorium*). |
| **Folio f35r / f8r** | Fytomorfiset "kasvit": juuristo, paksu varsi, suuri malja ja siniset ulokkeet | `COMPLETED_LOCK_HALT`, `CLOSED_HIGH_PRESSURE_LINE`, `THERMAL_INFUSION`, `CONTAINMENT_RECEPTACLE` | Naamioitu prosessireaktori (*Camouflaged Flowsheet*): imujuuristo, pystysuora nousukolonni, höyrystinvaippa ja tislausnokat. |
| **Folio f49v** | Vasemman marginaalin arabialaiset numerot `1, 2, 3, 4, 5` ja huipun tähti | `SYSTEM_REBOOT` $\rightarrow$ `PRESSURIZED_CALIBRATION` $\rightarrow$ `VALVE_CALIBRATION` $\rightarrow$ `COMPLETED_LOCK_HALT` | Vaiheittainen automaation esiasetusohjelma (*Step Program*) ja paineen hätävapautusventtiili (*Safety Relief Valve*). |
## LUKU 4: VFSF-mallin empiirinen todistus ja tilastollinen stressitestaus

### 4.1 Sivunsisäinen permutaatiotesti (Within-Folio Permutation)
Koodin tieteellisen robustisuuden varmistamiseksi (`v3.8.2`) järjestelmä testataan tiukimmalla mahdollisella tilastollisella kriteerillä: **sivunsisäisellä Monte Carlo -permutaatiolla**. Tässä menetelmässä sanoja ei sekoiteta koko korpuksen yli, vaan kunkin sivun (*Folio Locus*) omat sanat sekoitetaan keskenään vain kyseisen sivun sisällä 1 000 kertaa (kiinteällä satunnaissiemenellä `1337`). 

Lisäksi yksittäisten kirjainten (`y`, `d`, `o`, `l`, `n`) haku on rajattu tiukkaan täsmäosumaan (`token == key`), mikä estää tuntemattomien sanojen vuotamisen passiivitiloiksi (*Substring Trap*).

### 4.2 Lopullinen stressitestiraportti (10 sivun testikorpus, 872 genuine-tokenia)

=====================================================================================
 VFSF GLOBAL STRESS TESTER v3.8.2 — TULOSYHTEENVETO
=====================================================================================
 Aito järjestys virheet:              62 kpl / 881 askelta (92.96 % OK)
 Satunnaiskohinan keskiarvovirheet:   73.68 kpl
 Satunnaiskohinan virheväli (Min/Max): 56 - 100 kpl
 Empiirinen p-arvo (Sattumatodennäköisyys): 0.030969
-------------------------------------------------------------------------------------
 TULOS: ERITTÄIN MERKITSEVÄ (p < 0.05). Sanajärjestyksen teollinen signaali vahvistettu!
=====================================================================================

* **Koko korpuksen skaalautuvuus (ZL3b-n.txt):** Järjestelmä on ajettu onnistuneesti läpi koko Voynich-käsikirjoituksen EVA-transkription (38 216 puhdistettua tokenia / 38 417 prosessivaihetta), mikä todistaa tilakoneen vakauden ja skaalautuvuuden suuressa datamassassa.

---

## LUKU 5: Menetelmällinen laadunvalvonta (Methodological QA)

1. **Kombinatorisen vuodon esto:** Tiukka alustusvalvonta (`Cold Start` ja `Auto-Init V=4`), dynaaminen massankulutus ($\Delta V$) ja 1-merkin täsmähaku estävät satunnaiskohinaa läpäisemästä tilakonetta ilman virhelippuja.
2. **Ylisovituksen torjunta:** Malli ei käännä yksittäisiä sanoja subjektiivisiksi tarinoiksi, vaan mittaa puhdasta rakenteellista konvergenssia. Se, että aito sanajärjestys voittaa satunnaiskohinan tilastollisesti merkitsevällä tasolla ($p = 0.030969 < 0.05$) jopa yksittäisten sivujen sisäisessä sekoituksessa, vahvistaa koodin ja prosessimallin koherenssin.

---

## References and Historical Source Materials

### Voynich Manuscript, Paleography, and Decipherment Research
* **Beinecke Rare Book & Manuscript Library, Yale University.** The Voynich Manuscript. MS 408. Fifteenth-century illustrated manuscript.  
  https://yale.edu
* **Bowern, Claire L., and Luke Lindemann.** “The Linguistics of the Voynich Manuscript.” *Annual Review of Linguistics* 7 (2021): 285–308.  
  https://doi.org
* **Currier, Prescott H.** “Some Important New Statistical Findings.” In *New Research on the Voynich Manuscript: Proceedings of a Seminar*, 1976.  
  https://voynich.nu
* **Davis, Lisa Fagin.** “How Many Glyphs and How Many Scribes? Digital Paleography and the Voynich Manuscript.” *Manuscript Studies* 5, no. 1 (2020): 164–180.  
  https://doi.org
* **Zandbergen, René.** “Text Analysis: Transliteration of the Text.” *The Voynich Manuscript*.  
  https://voynich.nu

### Historical Machinery, Automata, and Practical Manuals
* **Brunschwig, Hieronymus.** *Liber de arte distillandi de simplicibus* (Das Buch der rechten Kunst zu distillieren). Strasbourg, 1500.
* **Michael of Rhodes.** *The Book of Michael of Rhodes*. Fifteenth-century maritime working manuscript (begun 1434).  
  https://imss.fi.it
* **Strolovitch, Devon L.** *Old Portuguese in Hebrew Script: Convention, Contact, and Convivência*. PhD dissertation, Cornell University, 2005.

---
*Report ends. The Universal State Matrix v3.8.2 validated at p = 0.030969 (Within-Folio). Archived under DOI: 10.5281/zenodo.23916072.*
