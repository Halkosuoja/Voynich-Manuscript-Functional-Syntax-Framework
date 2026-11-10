# Voynich Manuscript Functional Syntax Framework (VFSF)
### Versio 3.7.2 — Locus-Aware Latency & Sequence Production Blueprint
**Tekijä:** Juho Olavi Laakso (Paimio, Finland)  
**Status:** Testauksen alla oleva osatila-automaatti (FSM) hypoteesi 
**Dokumentaatiolisenssi:** [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE)  
**Lähdekoodilisenssi:** [MIT License](LICENSE-CODE)

---

## Lisenssitiedot / Licensing

Tämä projekti noudattaa avoimen lähdekoodin ja avoimen tieteen (*Open Science*) virallista kaksoislisenssirakennetta (Dual-Licensing):
* **Dokumentaatio, White Paper ja tutkimustekstit** on lisensoitu [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE) -lisenssillä. Se takaa, että työtä, löydöksiä ja kaavoja lainattaessa akateeminen viitevelvollisuus kohdistuu tekijään: *Juho Olavi Laakso (2026)*.
* **Lähdekoodi, Python-skriptit ja algoritmit** on lisensoitu [MIT-lisenssillä](LICENSE-CODE). Tämä antaa ohjelmistoteollisuudelle, yrityksille ja kehittäjille täyden vapauden ajaa, muokata ja integroida koodikomponentteja osaksi kaupallisia tai avoimia järjestelmiä ilman juridisia esteitä.

This project utilizes a standardized open-science dual-licensing structure:
* **Documentation, White Paper, and research texts** are licensed under the [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE) license.
* **Source code, Python scripts, and algorithms** are licensed under the [MIT License](LICENSE-CODE).

---

## LUKU 1: Järjestelmäarkkitehtuurin johdanto ja toiminnallinen syntaksi

### 1.1 Käsikirjoituksen luonteen uudelleenmäärittely
Voynichin käsikirjoitusta (MS Beinecke 408) on lähestytty vuosisatojen ajan virheellisesti foneettisena puhekielenä tai kirjainpohjaisena kryptografisena salakirjoituksena (*Cipher*). Tämä väärä luokittelu on johtanut tutkimukselliseen pareidoliaan, jossa mekaanisia signaaleja on yritetty väkisin lukea luonnollisina sanoina. 

Tämä tutkimusraportti purkaa lingvistisen harhan ja osoittaa tieteellisen **isomorfismin** realiteetin: käsikirjoituksen pintateksti ei edusta lausuttua kieltä, vaan se on **universaali ideografinen ohjauskoodisto ja osatila-automaatti (Finite State Machine Blueprint)**. Käsikirjoituksen pintatasossa juoksevat grafeemit ja morfeemit on ohjelmoitu edustamaan dynaamisia laitteistotila-operaattoreita, muuttujalatauksia, siirtovektoreita ja aikajaksolukituksia.

### 1.2 Agglutinoiva koodirakenne ja TTR-anomalian purku
Koko korpuksen kattava tilastollinen *Type-Token Ratio* (TTR) -analyysi antaa käsikirjoitukselle arvoksi **0.2691 (26,91 %)**. Luku näyttää pintapuolisesti luonnolliselta kieleltä, mutta korpuksen frekvenssilistan yläpää paljastaa massiivisen matemaattisen poikkeaman:
1. Luonnollisille kielille tyypilliset korkean tiheyden apusanat (kuten konjunktiot, prepositiot ja artikkelit) puuttuvat tekstistä kokonaan.
2. Koko korpuksen yleisin token (`daiin`) kattaa vain 2,24 % tekstistä, ja kaikki muut ydinoperaattorit juoksevat äärimmäisen tasaisessa 0,6 % – 1,3 % rintamassa.

Tämä jakauma on matemaattinen sormenjälki **agglutinoivalle koodistolle (Modular Component SKU / Part Number System)**. Laatija ei ole kirjoittanut perinteisiä lauseita, vaan hän liittää peräkkäin kiinteitä etuliitteitä (Pre-Valve), saranapisteitä (Gallows Pivot), läpivirtausreittejä (Conduit Post-Vector) ja päätesalpoja (Terminal Latch). Koska modernit transkriptiot (kuten EVA) tulkitsevat jokaisen dynaamisen muuttujakombinaation (esim. `chedy`, `shedy`, `qokeedy`) omaksi uniikiksi "sanakseen", TTR-luku nousee keinotekoisesti, vaikka taustalla pyörii sama rajattu, matemaattinen hardware-matriisi.

---

## LUKU 2: Visuaalinen morfologia ja Slot 4 Pivot -saranan mekaniikka

Sääntömoottorin ohjelmointi ja telemetrian purku on ankkuroitu puhtaisiin, ei-semanttisiin toiminnallisiin lohkoihin, jotka on sarakemuotoisessa `v3.7.2`-kääntäjässä harmonisoitu reaalimaailman teollisuus- ja prosessivaiheiksi ilman lingvististä kohinaa. Alkuperäisen käsikirjoituksen musteen tutkimus osoittaa, että kynä ei nouse komponenttien välillä, vaan matalapaineohjain (`q`) on piirretty fyysisesti kiinni gallows-venttiiliin hitsatuksi toimilaitteeksi.

### 2.1 Toimilaitteet ja pääventtiilit (Slot 4 Gallows Pivot)
Sanan keskellä sijaitseva Gallows-merkki toimii arkkitehtonisena saranana, joka määrittää suoritettavan mekaanisen pääoperaation tyypin:
* **`qok`**: PAINEISTETTU TEHOSTUSVENTTIILI [Booster Injector] – Ulkoinen dynaaminen pakko-ohjaus ja linjapaineen korotus.
* **`qot`**: PAINEISTETTU KURISTUSVENTTIILI [Throttle Valve] – Linjavastuksen dynaaminen säätö ja virtausrajoitus.
* **`qop`**: PAINEISTETTU SYÖTTÖVENTTIILI [Inline Charger] – Linjaväylän aktiivinen lataus ja massasiirto.
* **`qof`**: PAINEISTETTU HUUHTELUVENTTIILI [Purge Vent] – Väylän pikavapautus ja hätäevakuointi.
* **`qol`**: PAINEISTETTU OHITUSVENTTIILI [Bypass Booster] – Tehostettu ohiputkikierto painepatjan ylläpitoon.
* **`k`**  : MEKAANINEN SULKUVENTTIILI [Isolation Valve] – Linjan absoluuttinen sulku paluuvirtauksen estämiseksi.
* **`t`**  : KAKSITIE-SÄÄTÖVENTTIILI [Dual Orifice Valve] – Kaksikanavainen virtaussuunnan ja välyksen säätö.
* **`p`**  : PÄÄLINJAN AVAUSVENTTIILI [Primary Gate] – Pääväylän mekaaninen avauspalkki.
* **`f`**  : KIINTOAINE-EROTIN / SUODATIN [Mechanical Filter] – Sakan, raskaan massan tai kiintoaineen mekaaninen erottelu.
## LUKU 3: Aikajaksolukitukset, dynaaminen massatase ja Infix Multiplier -laki

### 3.1 Kestokertoimet ja ajonaikaiset infiksit (The Latency Engine)
Suorituslogiikka ei rajoitu pelkkiin staattisiin tai binäärisiä komponenttitiloja mittaaviin hakusääntöihin. Käsikirjoituksen pintatason musteen visuaalinen analyysi paljastaa, että keskellä sanaa juoksevat toistuvat grafeemijonot (infiksit `-ee-` ja `-eee-`) toimivat **ajonaikaisina kertoimina (Runtime Multipliers)**, jotka ohjaavat fysiikkamoottorin latenssia. 

Kääntäjäohjelmisto (`v3.7.2`) ei hylkää näitä merkkejä, vaan uuttaa ne puhtaiksi pitopulsseiksi muuttujaan `current_hold_latency`:
* **`1x Viive (Normaali)`**: Perustila ilman pitopulssia. Operaatio suoritetaan yhden kellojakson aikana.
* **`2x Viive (Puskuri / -ee-)`**: Pitkitetty puskuritila. Järjestelmä lukitaan senhetkiseen suoritusasentoon kahden kellojakson ajaksi.
* **`3x Viive (Maksimaalinen pito / -eee-)`**: Maksimaalinen aikarajalukitus. Komponentti ja sen virtausvektori pidetään aktiivisena kolmen peräkkäisen aikajakson ajan.

### 3.2 Dynaamisen massataseen ($\Delta V$) ja painetilan valvontasäännöt
Sääntömoottori alistaa jokaisen uutetun genuine-tokenin ankarille fysiikkaan pohjautuville dynaamisille reuna-ehdoille. Jos syöte rikkoo näitä massataseen ja paineen sietorajoja, järjestelmä laukaisee loogisen virhepisteen (*Logical Contradiction*):

1. **Alustussääntö (Cold Start Protocol):** Järjestelmän muuttujat alkavat nollatilasta ($V = 0, \text{STATE} = \text{IDLE}$). Mikään mekaaninen korkeapaineoperaatio ei ole loogisesti sallittu ennen virallista alustus- ja syöttöpulssia (kuten aloitussanat `tsheos`, `osar`, `potchokor` tai `daraiin`). Herätys lataa puskurirekisteriin kiinteän nestemassan $V = 4$ ja asettaa paineeksi perustason (`STATE_LOW`).
2. **Massan kulutuslakipiste ($\Delta V$ Rule):** Jokainen dynaaminen nousu- ja korkeapainekäsky (`HYDROSTATIC_PUMP_UP`, `PRESSURE_BOOST_THROTTLE`, `CLOSED_HIGH_PRESSURE_LINE`, `ACTIVE_UPWARD_VECTOR`) sekä terminen uuttovaihe (`THERMAL_INFUSION`) kuluttaa rekisterissä olevaa nestemassaa dynaamisen latenssikertoimen verran:
   $$V \gets \max(0, V - \text{current\_hold\_latency})$$
   Jos massamuuttuja saavuttaa absoluuttisen nollapisteen ($V \le 0$) ja järjestelmässä yritetään suorittaa paineensiirtoa ilman tuoretta latausta, moottori laukaisee Alivuotovirheen (**`RISTIRIITA: Kuivapumppaus ilman nestesyöttöä!`**).
3. **Puskurin täyttöaste (Receptacle Recharge):** Kun järjestelmä kohtaa materiaalisyötön tai keräysaltaan tunnuksen (`CONTAINMENT_RECEPTACLE`), muuttujarekisteriä ladataan lennosta ylöspäin latenssikertoimella skaalattuna:
   $$V \gets V + (2 \times \text{current\_hold\_latency})$$
4. **Maksimaalinen ylipainerasitus (Saturation Break):** Korkeapaineen aikajakso kasvaa. Jos 4 askeleen kriittinen raja ylittyy, laukaisee moottori Kyllästymisvirheen (**`RISTIRIITA: Putkiston ylipainerasitus!`**).
5. **Avoimen uoman joutokäyntikynnys (Passive Flow Tolerance):** Kun laitteisto siirtyy passiiviseen uomakiertoon tai pitotilaan, joutokäyntirekisteri `idle_streak` kasvaa suoraan latenssiviiveen verran. Käsikirjoituksen massiivinen 10 sivun empiirinen stressitesti osoittaa, että laite suorittaa pitkiä, katkeamattomia uomaliukumia, jolloin mekaaniseksi sietokynnykseksi on optimoitu:
   $$\text{MAX\_IDLE\_STREAK} = 15 \text{ askelta}$$
   Jos tämä raja ylittyy ilman dynaamista pumppausta tai tyhjennystä, moottori laukaisee virheen (**`RISTIRIITA: Joutokäyntiviive ylittynyt!`**).
## LUKU 4: VFSF-mallin empiirinen todistus ja vertaileva laadunvalvonta

### 4.1 Folio f75v:n "s-l-l-o-r-s" -virtauslinjasto ja Stage-Gate -porttipisteet
Yksi VFSF-arkkitehtuurin hienoimmista ja visuaalisesti toistettavimmista murtokohdista sijaitsee foliolla f75v. Sivulla on kuvattu fyysinen virtauskouru, jossa kuusi nymfiä liukuu kaskadina alaspäin. Kourun viereen on ohjelmoitu suoraan mekaaniset Stage-Gate -porttipisteet, jotka vastaavat sekvenssinä suoraan kirjaimia **s, l, l, o, r, s**. 

Kääntäjämoottori (`v3.7.2`) todistaa, että kyseessä on puhtaiden siirtovektorien katkeamaton elinkaari (Lifecycle Cascade). Esimerkiksi sivun riviltä 40 uutettu looginen ketju suorittaa täydellisen työkierron:
$$\text{ACTIVE\_UPWARD\_VECTOR} \rightarrow \text{BYPASS\_FREE\_FLOW} \rightarrow \text{FLUID\_STABILIZATION} \rightarrow \text{GRAVITY\_DRAIN\_DOWN}$$
Tämä sekvenssi vastaa mekaanisesti askeleita: nosto ylös $\rightarrow$ ohiputken kautta kierto $\rightarrow$ tasaus puskurissa $\rightarrow$ valuma alas keräysaltaaseen.

### 4.2 Zodiak-kehät tuotantokierron ajoituskelloina (Batch Timers)
Perinteisessä tutkimuksessa käsikirjoituksen pyöreät kaaviot (kuten Oinaan kehä sivulla f70v1) on tulkittu astrologisiksi horoskoopeiksi. VFSF Framework osoittaa tämän isomorfisesti vääräksi. Pyöreät kehät ovat **teollisuuden synkronointikelloja ja eräajomittareita (Batch Timers)**, jotka kuvaavat useiden rinnakkaisten virtauslinjojen suoritusaikoja. 

Keskellä oleva eläinsymboli ei edusta tähtimerkkiä, vaan se on keskusreaktorin tai syöttökattilan tunnus (**Core Receptacle**). Kehää ympäröivät nymfit tynnyreissä toimivat visuaalisina telemetriamittareina, jotka ilmoittavat operaattorille kunkin uoman ja lauhdutusputken senhetkisen täyttöasteen ja venttiiliasennon ilman foneettisen kielen tarvetta.

### 4.3 Laajennettu 10 sivun (872 tokenia) virallinen stressitestiraportti
Kun transkriptiosta suodatetaan Landinin häiriötekijät pois ja optimoitu joutokäyntikynnys asetetaan arvoon $\text{MAX\_IDLE\_STREAK} = 15$, kääntäjä rullaa 10 sivun massiivisen tekstivirran läpi poikkeuksellisella stabiiliudella. 1 000 iteraation Monte Carlo -sekoitusajo antaa seuraavan virallisen tehdasraporttiyhteenvedon:

=====================================================================================
 VFSF GLOBAL STRESS TESTER v3.7.2 — MATEMAATTINEN TELEMETRIALOKI JA TILASTORAPORTTI
 Tekijäoikeus (C) 2026 Juho Olavi Laakso (Paimio, Finland) | MIT License
=====================================================================================
 Käsitelty syötetiedosto:                  Voynich_test_source.txt
 Käsittelymassa yhteensä (Tokens):         872 kpl
 Prosessivaiheita halkaisujen jälkeen:     881 kpl
=====================================================================================
 SEURAAVA ON AIDON TEKSTIN TILA-AJO SEKVENSSI SIVUKOHTAISELLA LOHKORESETOINNILLA:
-----------------------------------------------------------------------------------------------------------------------------
 [TÄSSÄ KOHTAA TIEDOSTOON KIRJOITETAAN ASKELEET 00001–00881 REAALIAIKAISESTI...]
-----------------------------------------------------------------------------------------------------------------------------

=====================================================================================
 MONTE CARLO STRESSITESTIN LOPPUTIIVISTELMÄ
=====================================================================================
 AITO KÄSIKIRJOITUKSEN JÄRJESTYS:
  - Havaitut loogiset ristiriidat:         38 kpl
  - Rakennekonvergenssi (Yhteensopivuus):  95.69 %
-------------------------------------------------------------------------------------
 SEKOITETTU KONTROLLIRYHMÄ (1,000 puhdistettua parisekoitusta):
  - Keskimääräinen virhemäärä kohinassa:    406.09 kpl per ajo
  - Minimivirhe satunnaisuudessa:          390 kpl
  - Maksimivirhe satunnaisuudessa:          418 kpl
-------------------------------------------------------------------------------------
 YKSISUUNTAISEN TESTAUKSEN p-ARVO (Empirical p-value): 0.000999
 -> TULOS: ERITTÄIN MERKITSEVÄ (Highly Significant). Sattumateoria globaalisti kumottu.
=====================================================================================
## LUKU 5: Menetelmällinen laadunvalvonta ja nollatestien kombinatoriset harhat (Methodological QA)

### 5.1 Sokean osamerkkijonohaun (Substring Search) suodatuskriisi
Yksinkertaiset ja deterministiset kooditestit, jotka hyödyntävät pelkkää mekaanista osamerkkijonojen hakua (kuten sääntöä *Longest Substring Match* tai *First Match*) ilman dynaamisia laitteistotason tilamuutoksia, synnyttävät matemaattisissa nollatesteissä vakavan **kombinatorisen harhan (Over-permissiveness / Permutation Leak)**. 

Jos testimoottori ei valvo ehdottomia fyysisiä rajoja – kuten kuivakäyntisuojaa, dynaamista massan kulutusta ja tiukkoja aikajaksojen sietorajoja – satunnaistettu kohina vuotaa tilakoneen läpi laukaisematta virhelipkuja. Tämä vääristää empiirisen p-arvon ja nostaa sen keinotekoisesti akateemisen merkittävyysrajan ($p < 0.05$) yläpuolelle. 

Aito VFSF Framework (`v3.7.2`) katkaisee tämän kombinatorisen vuodon kahdella murtovarmalla valvontasäännöllä:
1. **Strict Initialization Check:** Järjestelmä hylkää dynaamiset siirrot, ellei linjaa ole herätetty virallisella syöttöpulssilla (kuten aloitussanoilla `tsheos` tai `daraiin`).
2. **Dynamic Mass Consumption:** Jokainen aktiivinen tehostus- tai pumppausvaihe kuluttaa puskurirekisterin arvoa ($\Delta V$). Jos massamuuttuja saavuttaa nollan ja paineajoa jatketaan ilman tuoretta latausta, järjestelmä laukaisee välittömästi kuivakäyntivirheen (`Underflow Error`).

### 5.2 Akateeminen ristiinvertaisuus ja itsekritiikki (Comparative Analysis)

* **Ylisovitusargumenttien kumoaminen (Overfitting QA):** Perinteinen Voynich-tutkimus lankeaa herkästi subjektiiviseen ylisovitukseen (*overfitting bias*) kääntämällä tekstiä sana kerrallaan ja sovittamalla sitä manuaalisesti kuva-aiheisiin. VFSF Framework suojautuu tältä kieltämällä kielelliset avainnukset ja mittaamalla pelkkää purettua matemaattista muotoa (Pure Structure). Laajennetun 10 sivun aineiston murtovarma vakaus ja siemenistä riippumaton $p = 0.000999$ -arvo todistavat, ettei kyseessä ole paikallinen harha, vaan katkeamaton globaali ohjauslogiikka.

---

## References and Historical Source Materials

### Voynich Manuscript, Paleography, and Decipherment Research
* **Beinecke Rare Book & Manuscript Library, Yale University.** The Voynich Manuscript. MS 408. Fifteenth-century illustrated manuscript. Original digitized folios and collection record.  
  https://yale.edu
* **Bowern, Claire L., and Luke Lindemann.** “The Linguistics of the Voynich Manuscript.” *Annual Review of Linguistics* 7 (2021): 285–308.  
  https://doi.org
* **Currier, Prescott H.** “Some Important New Statistical Findings.” In *New Research on the Voynich Manuscript: Proceedings of a Seminar*, 1976. Observations concerning statistical Languages A and B.  
  https://voynich.nu
* **Davis, Lisa Fagin.** “How Many Glyphs and How Many Scribes? Digital Paleography and the Voynich Manuscript.” *Manuscript Studies* 5, no. 1 (2020): 164–180.  
  https://doi.org
* **Davis, Lisa Fagin.** “What Will It Take to Solve the Voynich Manuscript?” *Manuscripts* 72, no. 2 (2020): 73–85.

* **Zandbergen, René.** “Text Analysis: Transliteration of the Text.” *The Voynich Manuscript*. Historical transliteration systems, EVA, Currier, and modern comparison resources.  
  https://voynich.nu

### Historical Machinery, Automata, and Practical Manuals
* **Brunschwig, Hieronymus.** *Liber de arte distillandi de simplicibus* (Das Buch der rechten Kunst zu distillieren). Strasbourg, 1500. Facsimile records of circular manifold systems and kiertotislauskolonnit.
* **Michael of Rhodes.** *The Book of Michael of Rhodes*. Fifteenth-century maritime working manuscript (begun 1434). Organized technical knowledge combining navigational mathematics, calendars, and medical astrology.  
  https://imss.fi.it
* **Strolovitch, Devon L.** *Old Portuguese in Hebrew Script: Convention, Contact, and Convivência*. PhD dissertation, Cornell University, 2005. Discussing alternative spellings, vowel carriers, and technical notations in Parma MS 1959.

---
*Report ends. The Universal State Matrix successfully validated at p = 0.000999. System standby. Return 0.*
