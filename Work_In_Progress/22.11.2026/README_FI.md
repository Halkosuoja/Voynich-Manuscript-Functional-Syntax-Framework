[![DOI](https://zenodo.org/badge/1398740941.svg)](https://doi.org/10.5281/zenodo.23916072)

# Voynich Manuscript Functional Syntax Framework (VFSF)
### Black-Box-rakenne-, raja- ja rinnakkaiskorpusanalyysi
**Tekijä:** Juho Olavi Laakso (Paimio, Finland)  
**Tila:** Kokeellinen black-box-tutkimus ja tilastollinen verifiointi (*Work in Progress / Pre-release*)  
**Dokumentaatiolisenssi:** [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE)  
**Lähdekoodilisenssi:** [MIT License](LICENSE-CODE)  
[In English](README.md)

---

## 1. Projektin tarkoitus ja menetelmä

Tämä projekti tutkii Voynichin käsikirjoituksen (MS Beinecke 408, Zandbergen–Landini-transkriptio `ZL3b-n.txt`: `5 376` riviä, `38 216` raakasanuetta / `35 358` sanaa epävarmojen `,`-välien yhdistämisen jälkeen) pintarakennetta **black-box**-lähestymistavalla ilman ennakko-oletuksia siitä, edustaako teksti puhuttua kieltä vai formaalia protokollaa.

Lähtökohtana on paikkasidonnainen sanamalli:

`[ PREFIX ] + [ LIGATUURI / YDIN + INFIKSI ] + [ SUFFIX ]`

### Tilastolliset kontrollit
Kaikki sekvenssi-, raja- ja toistotestit on suoritettu **sivun, kappaleen ja tarkan riviaseman (`PF`, `LF`, `LM`, `LL`, `S`) lukitsevilla** Monte Carlo -permutaatioilla (`150–200` iteraatiota, kiinteä siemen `1337`), ja niitä on verrattu täsmälleen samalla mittarilla luonnollisiin kieliin, synteettisiin generaattoreihin sekä oikeaan C-ohjelmakoodiin.
* **Empiirinen merkitsevyysraja:** Kaavalla `p = (k + 1) / (N + 1)` iteraatiomäärien `N = 200` ja `N = 150` alimmat mahdolliset arvot ovat `p < 0.005 (0/200)` ja `p < 0.007 (0/150)`. Ne raportoidaan rehellisesti otosrajoina jatkuvien todennäköisyyksien sijaan.
* **Yhteys vuoden 2026 kirjallisuuteen:** Vuoden 2026 itsenäiset tutkimukset (*"A Glyph Is Not a Letter, a Token Is Not a Word, a Space Is Not a Space"*, arXiv 2026; *Voynich Lucidity* CBMI, 2026) ovat päätyneet samaan ~0.2 bitin reunamerkki-informaatioon, epävarmojen välien toimintaan sekä Etäisyys 2 -pudotukseen. Tämä repositorio toistaa nuo mittaukset itsenäisesti `ZL3b-n.txt`-aineistolla ja laajentaa niitä yhtenäisellä gallows-/liitinmatriisilla, `-y`-alaluokkien erottelulla, generatiivisilla mekanismitesteillä, toistoröntgenillä ja 11 tekstin vertailulla.

---

## 2. Keskeiset empiiriset löydökset (`ZL3b-n.txt`)

### 2.1 EVA-transkription epävarmat välit (`,`) vs. selvät välit (`.`)
EVA-transkription kapeat/epävarmat välit (`,`) selittävät merkittävän osan tietyistä rajapareista:
* `o -> r`: `50.5 %` tapauksista johtuu `,`-välistä
* `o -> l`: `44.8 %` johtuu `,`-välistä (`ol` esiintyy `5 507` kertaa yhteen kirjoitettuna vs. `119` kertaa selvän välin yli)
* `s -> a`: `38.4 %` johtuu `,`-välistä (`s+ai` esiintyy `376` kertaa yhteen vs. `127` välillä)
* `r -> a`: `27.9 %` johtuu `,`-välistä (`r+ai` esiintyy `425` kertaa yhteen vs. `304` välillä)
* Sen sijaan `y + qo` (`98.2 %` välilyönnin erottamana, `3 382` vs. `61`), `n + ch` (`98.0 %` välillä, `1 294` vs. `26`) ja `y + lk` (`96.5 %` välillä, `246` vs. `9`) toimivat lähes ehdottomina sanarajoina.

### 2.2 Välitön 1-askeleen rajakytkentä (Etäisyys 1 vs. Etäisyys 2)
Kun `,`-välit yhdistetään ja kappale sekä riviasema lukitaan, vierekkäisten sanojen reunamerkeillä on voimakas keskinäinen informaatio (*Mutual Information*), joka katoaa lähes kokonaan jo yhden sanan yli hypättäessä:
* **Selvillä sanaväleillä (`,`-välit yhdistetty):** Etäisyys 1 = `MI 0.16327 vs. 0.01438` (`x11.35`, netto `+0.1489` bittiä, `Z = +154.65`) $\rightarrow$ Etäisyys 2 = `0.02252 vs. 0.01568` (`x1.44`, netto `+0.0068` bittiä, `Z = +6.52`). **`95.4 %`** signaalista katoaa heti etäisyydellä 2.
* **Vaikka myös sanansisäisesti yleiset `o+l`, `r+ai` ja `s+ai` yhdistetään:** Etäisyys 1 säilyy lähes ennallaan (`MI 0.14035 vs. 0.01474`, `x9.52`, netto `+0.1256` bittiä), ja **`95.1 %`** siitä katoaa edelleen etäisyydellä 2 (`x1.38`).
* **Signaalin keskittyminen sanarajalle (globaali testi vakioidun alun sisällä):** Kun seuraavan sanan alku vakioidaan (`ch-`, `sh-`, `ok-`, `ot-`) ja testataan koko laaja siirtymätaulu siitä, ennustaako edellisen sanan loppu *mitä tahansa* seuraavan sanan loppupäätettä, globaali ero ei ole merkitsevä (`p = 0.055–0.124`). Ainoastaan `qo-`-sanojen sisällä säilyy pieni pääteharmoninen jäänne (`Z = +2.66`, `p = 0.010`, esim. `-ey -> qok+ey` `Z = +3.70` ja `-dy -> qok+dy` `Z = +2.88`).

### 2.3 Yleinen "liitinmatriisi" (`Herbal` vs. `Bio + Recipes`)
Edellisen sanan loppukirjaimen ja seuraavan alkukirjaimen välinen yhteensopivuussuhde (havainto / odotusarvo) jakaa alut neljään selvään ryhmään, ja **sama perusmatriisi toistuu sekä `Herbal` (Currier A) että `Bio + Recipes` (Currier B) -osioissa**:

* **`q-` (`qo-`, `13.1 %` koko korpuksesta):** `72.6 %` seuraa `-y`-päätettä (`1.72x` koko korpus; `1.53x` Herbal / `1.66x` Bio+Recipes), hylkii muita päätteitä (`0.25x–0.62x`).
* **Gallows-merkit (`k, t, p, f`):** Suosivat edellään `-o`:ta (`1.66x–3.81x`, pääosin `-sho/-cho/-sheo`-sanoja kuten `sho -> koeam`, `cho -> cthy`), `-y`:tä (`1.15x–1.56x`) ja `-l`:ää (`k/t` erityisesti B-osiossa `2.76x / 1.91x`), ja torjuvat jyrkästi `-s`, `-n` ja `-r` (`0.12x–0.52x`).
* **`a-` (`aiin, ain, al, ar...`):** Suosii jyrkästi `-s`:ää (`4.68x` koko korpus; `4.60x` Herbal / `6.28x` Bio+Recipes, esim. `ches -> aiin`) ja `-r`:ää (`2.99x`; esim. `or -> aiin`, `ar -> al`), ja torjuu jyrkästi `-y`:tä (`0.20x`).
* **`c-`, `o-`, `s-`:** Suosivat maltillisesti `-n`:ää (`1.23x–1.39x`), `-r`:ää ja `-l`:ää, ja esiintyvät harvemmin `-y`:n perässä (`0.73x–0.86x`).

### 2.4 Kolme erilaista gallows-roolia (`BARE_GAL` vs. `BRIDGED_GAL` vs. `QO_GAL`)
Vaikka paljaat `k, t, p, f` jakavat yhteisen rajaprofiilin, niiden liittäminen `ch`-penkkiin (`ckh/cth/cph/cfh`) tai `qo-`-etuliitteeseen muuttaa sanan syntaktisen roolin ja sijainnin täysin:

| Ryhmä | Määrä (`N`) | `PF` (Kappaleen alku) | `LF` (Rivin alku) | `LM` (Rivin keskikohta) | `LL` (Rivin loppu) | Edeltävän lopun profiili |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **`BARE_GAL`** (`k/t/p/f-`) | 2 504 | **24.3 %** | 12.3 % | 53.8 % | 8.3 % | `-o: 2.47x`, `-l: 1.37x`, `-y: 1.36x` (hylkii `-s/-n/-r`) |
| **`BRIDGED_GAL`** (`ckh/cth/cph/cfh-`) | 763 | 0.5 % | 1.2 % | 79.3 % | **18.6 %** | `-o: 1.60x`, `-n: 1.49x`, `-s: 1.24x`, `-y: 0.75x` |
| **`PLAIN_CH`** (`ch-`, ei gallowsia) | 5 660 | 0.1 % | 2.6 % | 85.4 % | 11.1 % | `-n: 1.38x`, `-l: 1.24x`, `-r: 1.16x`, `-o: 0.70x` |
| **`QO_GAL`** (`qok/qot/qop/qof-`) | 4 379 | 0.4 % | 9.4 % | 82.6 % | 7.4 % | `-y: 1.75x` (hylkii kaikki muut: `0.18x–0.55x`) |

*Lyhenteet: `PF` = kappaleen ensimmäinen sana (`PAR_FIRST`), `LF` = rivin ensimmäinen sana (`LINE_FIRST`), `LM` = rivin keskiosa (`LINE_MID`), `LL` = rivin viimeinen sana (`LINE_LAST`), `S` = yksittäissana/lappu.*

Kaikki neljä silloitettua gallows-muotoa (`ckh`, `cth`, `cph`, `cfh`) käyttäytyvät keskenään yhdenmukaisesti (`77–85 %` rivin keskellä, `15–21 %` rivin lopussa), muodostaen aidon välimuodon paljaan gallowsin (`-o: 2.47x`) ja penkkimerkin (`-n: 1.38x`) välille.

### 2.5 `-y`-luokkien eriytyminen, spesifi päätesointu ja suunnattu sekvenssi
* **`-y`-päätteiden sisäinen ero (`Z = +15.39`, `p < 0.005 [0/200]`):** Kappale, riviasema ja loppukirjain `-y` lukittuina eri `-y`-luokat (`N = 12 613`) käyttäytyvät eri tavoin: `-ey` (`4.5 %` rivin lopussa), `-dy` (`10.4 %` lopussa, `32.9 %` seuraa `qo-`), `-hy` (`9.7 %` lopussa), `-ky/-ty` (`18.3–19.0 %` lopussa) ja `-ly` (**`36.1 %`** rivin lopussa).
* **Spesifi saman päätteen toistuminen (`w1 != w2`):** Vaikka globaalissa taulussa `ch-/sh-`-sanojen sisällä ei näy yleistä pääte-ennustettavuutta (kohta 2.2), spesifisti **identtisen päätteen toistumista (`w1_end == w2_end`)** mitattaessa eri sanat jakavat saman päätteen yli odotetun sekä Etäisyydellä 1 (`21.75 % vs. 19.44 %`, `Z = +8.66`) että Etäisyydellä 2 (`21.31 % vs. 19.41 %`, `Z = +6.25`). Tätä ajavat etuliitevaihtelut päätteissä `-dy` (`Z = +9.63`, esim. `shedy -> qokedy`), `-ey` (`Z = +6.20`, `okeey -> qokeey`) ja `-ol` (`Z = +5.18`, `otol -> chol -> shol`), kun taas `-aiin` välttää toistumista (`Z = -1.76`).
* **Produktiivinen suunnattu kierto:** Rivien sisällä esiintyy yksisuuntainen kierto (`BARE_OLR -> CH_DY -> QO_DY/EY -> QO_OTH -> BARE_OLR`), joka yleistyy myös harvinaisempiin sanoihin (kaikki `freq > 50` sanat poistettuna `Z = +10.09`, `p < 0.007 [0/150]`) ja selittyy suurelta osin edellä kuvatuista rajaliitinsäännöistä.

### 2.6 Generatiiviset mekanismitestit ja toistoröntgen (`d1: A-A`, `d2: A-X-A`)
Rakennetun mekanismin testaamiseksi kokeiltiin sekä käänteistä 1-askeleen generaattoria että luonnollisen tekstin mekaanisia muunnoksia (`vfsf_mechanism_test.py`, `vfsf_repeat_xray.py`):

* **1-askeleen Liitin-generaattori (`35 358` sanaa pelkästä `w_i[-1]`-ehdosta):** Toistaa hyvin Etäisyys 1 -kytkennän (`MI 0.17008 vs. 0.00756`, netto `+0.1625` bittiä) ja Etäisyys 2 -pudotuksen (`2.1 %` säilyvyys), **mutta epäonnistuu** toistamaan Voynichin päätesointua (`15.51 % / 13.92 %` vs. aito `21.73 % / 21.34 %`) sekä saman sanan toistoja (`d1 = 0.33 %`, `d2 = 0.28 %` vs. aito `0.86 %`, `0.96 %`).
* **Luonnollisen kielen mekaaninen muuntaminen (`plinius_ii.txt` & `Matteus1548.txt`):**
  * 1-merkin rajasiirto (`A1`) ampuu rajakytkennän liian korkealle (`+1.06–1.23` bittiä, `47x–63x`); 2-merkin bigrammikoodi (`A3`) romahduttaa sanaston (`388–612` uniikkia sanaa vs. Voynichin `9 340`).
  * Jatkuvan tekstin katkominen ennen merkkejä `c/k/p/t/q` (`A2`) tuottaa lähes täsmälleen Voynichin Etäisyys 1 -tason (`+0.132–0.162` bittiä) ja Etäisyys 2 -romahduksen (`1.8–3.9 %`), **mutta** jättää sanatoistot lähes nollaan (`d1 = 0.01 %`, `d2 = 0.09–0.10 %`).
* **Päinvastainen toistoprofiili (`d1` ja `d2` vs. proosa):**
  Kappale- ja riviasemalukitussa kontrollissa luonnollinen proosa välttää jyrkästi saman sanan välitöntä ja vuorottelevaa toistoa:
  * `Matteus1548.txt` (1548 suomi): `d1 = 0.11 % vs. 1.15 %` (`Z = -15.78`), `d2 = 0.62 % vs. 1.15 %` (`Z = -7.96`; vain `42 %` $\ge 4$ merkkiä).
  * `plinius_ii.txt` (latina): `d1 = 0.01 % vs. 0.49 %` (`Z = -9.02`), `d2 = 0.37 % vs. 0.50 %` (`Z = -2.43`; `45 %` $\ge 4$ merkkiä).
  * `3DBenchy.txt` (3D STL -koordinaatit): `d1 = 0.00 %` (`Z = -417.21`), `d2 = 0.00 %` (`Z = -208.21`).
  * **`ZL3b-n.txt` (Voynich):** käyttäytyy täysin päinvastoin: `d1 = 0.86 % vs. 0.74 %` (`Z = +2.49`, `105` uniikkia sanaa, `87 % >= 4` merkkiä) ja **`d2 (A - X - A) = 0.96 % vs. 0.71 %` (`Z = +5.00`, `94` uniikkia sanaa, `83 % >= 4` merkkiä)**, sisältäen rytmisiä lähivariaatioita (`qokedy - qokeedy - qokedy`, `shedy - qokedy - shedy`) ja sidottuja toistoja (`chol - daiin - chol`).
  * Myös C-lähdekoodi (`sqlite3_puhdas_prosessikoodi.txt`) saa positiiviset `d1/d2`-arvot (`Z = +63.15 / +235.65`), mutta eroaa täysin Voynichista Etäisyys 2 -tasolla (ks. Luku 3).
  * `kalevala_test_source.txt` (koko Kalevala): `d1 = 0.19 % vs. 0.47 %` (`Z = -11.44`, `100 % >= 4` merkkiä), mutta `d2 (A - X - A) = 1.09 % vs. 0.45 %` (`Z = +21.19`, `97 % >= 4` merkkiä) kalevalamitan kertosäkeen ja rinnakkaisrakenteen vuoksi (*"vieri kyynel, vieri toinen"*).
  * **Alustavat suomalaiset kansanperinneverrokit (siivoamattomat Gutenberg-versiot — `Arwoituksia.txt` 26 922 sanaa, `Loitsurunoja.txt` 81 517 sanaa, `vanhatRunot.txt` 176 652 sanaa):** Kaikissa kolmessa esiintyi vastaava positiivinen `d2` (`Z = +6.15 ... +15.18`), mutta vahvasti negatiivinen `d1` (`Z = -6.17 ... -23.49`, myös hokemia kuten *"lennä lennä"* sisältäneessä aineistossa) sekä korkea Etäisyys 2 -säilyvyys (`38.0 %`, `61.3 %` ja `90.3 %`, vs. Voynichin `4.6 %`). *(Tarkat luvut ovat alustavia ilman toimituksellisten selitysten ja varianttikirjainten siivousta.)*

---

## 3. Rinnakkaisvertailu (11 tekstiä: luonnolliset kielet, generaattorit & C-koodi)

Kaikki yksitoista tekstiä ajettiin samalla kieliriippumattomalla mittarilla (`universal_syntax_bench.py`) kappale- ja riviasemalukituksella (`150` iteraatiota, siemen `1337`):

| Teksti | Sanoja | Etäisyys 1 (netto-MI & kerroin) | Etäisyys 2 (netto-MI & kerroin) | Säilyvyys (Et. 2 / Et. 1) | Suunta-asymmetria | Vahvin rajakytketty alku (% tekstistä) |
| :--- | :---: | :--- | :--- | :---: | :---: | :--- |
| **`control_slot.txt`** (Slot-gen.) | 35 002 | `-0.00001` (`0.99x`) | `+0.00032` (`1.34x`) | – | `0.94x` (`Z=-0.36`) | `'ck-'` (`+3.6 %`, *kohinaa*) |
| **`control_selfcite.txt`** (1-sana kopiointi) | 35 000 | `+0.00018` (`1.04x`) | `+0.00075` (`1.15x`) | – | `0.97x` (`Z=-0.21`) | `'sh-'` (`+1.7 %`, *kohinaa*) |
| **`plinius_ii.txt`** (klass. latina) | 17 452 | `+0.0225` (`2.46x`) | `+0.0004` (`1.02x`) | ~1.6 % | `3.04x` (`Z=+18.21`) | `'es-'` (`1.6 %`, `+12.3 %`) |
| **`latin_abbrev.txt`** (lyh. latina) | 17 453 | `+0.0174` (`2.12x`) | `+0.0002` (`1.02x`) | ~1.4 % | `2.90x` (`Z=+16.04`) | `'es-'` (`1.6 %`, `+12.1 %`) |
| **`Herbarum.txt`** (yrttilatina) | 2 434 | `+0.2129` (`3.33x`) | `+0.0313` (`1.28x`) | **14.7 %** | `1.68x` (`Z=+4.38`) | `'ui-'` (`2.0 %`, `+32.2 %`) |
| **`Matteus1548.txt`** (1548 suomi) | 25 170 | `+0.0344` (`2.64x`) | `+0.0071` (`1.35x`) | **20.5 %** | `5.96x` (`Z=+51.20`) | `'et-'` (`1.9 %`, `+17.4 %`) |
| **`kalevalaTesti.txt`** (suomi) | 14 126 | `+0.0617` (`4.34x`) | `+0.0137` (`1.62x`) | **22.2 %** | `2.31x` (`Z=+19.71`) | `'vä-'` (`1.6 %`, `+35.7 %`) |
| **`hamlet.txt`** (engl. näytelmä) | 32 878 | `+0.0668` (`5.64x`) | `+0.0217` (`2.32x`) | **32.5 %** | `4.73x` (`Z=+83.10`) | `'lo-'` (`1.3 %`, `+38.1 %`) |
| **`LinuxTesti.txt`** (engl. ohje) | 5 774 | `+0.1429` (`2.70x`) | `+0.0548` (`1.65x`) | **38.3 %** | `5.57x` (`Z=+33.18`) | `'ca-'` (`1.3 %`, `+47.8 %`) |
| **`sqlite3_35k.txt`** (siivottu C-koodi) | 32 278 | `+0.2697` (`15.91x`) | `+0.2380` (`10.93x`) | **88.3 %** | `4.45x` (`Z=+258.67`) | `'pr-'` (`4.3 %`, `+56.8 %`) |
| **`ZL3b-n.txt` (Voynich)** | 35 358 | **`+0.1489` (`11.35x`)** | **`+0.0068` (`1.44x`)** | **4.6 %** | `3.80x` (`Z=+49.94`) | **`'qo-'` (`13.1 %`, `+30.3 %`)** |

### Vertailun johtopäätökset
1. **Suuntaepäsymmetria ei yksin erota Voynichia kielestä tai koodista:** 1548 suomi (`5.96x`), englanti (`4.73x–5.57x`), C-koodi (`4.45x`) ja latina (`3.04x`) saavat vastaavan tai suuremman suuntaepäsymmetrian kuin Voynich (`3.80x`).
2. **Yksinkertaiset generaattorit eivät tuota rajakytkentää:** Riippumaton Slot-generaattori (`0.99x`) ja 1-sanan kopioi-ja-muunna -malli (`1.04x`) eivät synnytä mitattavaa naapurikytkentää.
3. **Voynich asettuu selvästi erilleen sekä luonnollisesta proosasta että C-ohjelmakoodista:** Oikea C-koodi (`sqlite3_35k.txt`) säilyttää peräti **`88.3 %`** rajainformaatiosta vielä Etäisyydellä 2 (monisanaiset koodikaavat) eikä näytä harvinaisilla sanoilla (`<=20`) epäsymmetriaa (`Z = +0.16`, `p = 0.404`). Englanti ja suomi säilyttävät `20–38 %` etäisyydellä 2, kun taas latinan Etäisyys 1 -taso jää matalaksi (`2.12x–2.46x`). Voynich yhdistää korkean Etäisyys 1 -kytkennän (`11.35x`, `+0.1489` bittiä), **`95.4 %`:n pudotuksen Etäisyydellä 2**, positiivisen `d1/d2`-toiston (`Z = +2.49 / +5.00`) ja yhden `-y`-päätteeseen sitoutuneen etuliitteen (`qo-`, `13.1 %` koko tekstistä).

---

## 4. Tällä hetkellä varmentamattomat ja perustasosta rajatut hypoteesit (Methodological QA)

Seuraavat varhaisempien kehitysvaiheiden (`v1.5–v3.8.2`, `Digital Twin v2.0`) hypoteesit eivät saaneet tilastollista tukea nykyisissä nollatesteissä `ZL3b-n.txt`-aineistolla, minkä vuoksi ne on **rajattu pois varmistetusta empiirisestä perustasosta**. Se, ettei yksittäinen toteutus läpäissyt testiä nykyisellä EVA-transkriptiolla, ei vielä sulje lopullisesti pois kaikkia mahdollisia tulkintamuotoja – erityisesti kun otetaan huomioon EVA-merkistön tunnetut rajoitukset (ligatuurien pilkkominen, epävarmat välit, harvinaisten merkkien kuten `g` tulkintaerot) sekä historiallisen kuvavertailuaineiston tämänhetkinen rajallisuus. Nykyisellä näytöllä näitä ei kuitenkaan ole voitu osoittaa todeksi:

1. **Tislaussimulaattori (`Digital Twin v2.0`):** Testatuilla fysiikkaparametreilla (`1 000` sekoitusta) satunnainen sanajärjestys saavutti vastaavan tai suuremman tuoton ja turvallisuustason kuin aito teksti (`p = 0.52–0.72`). Nykyinen parametrimalli ei siis erottele aitoa järjestystä kohinasta.
2. **`-ain` vs. `-aiin` erottelu eri painetiloiksi:** Seuraavan sanan ennustamisen osalta ne käyttäytyvät kappaleen sisällä lähes identtisesti (`Z = +1.30`, `p = 0.090`). Mahdollinen muu asiayhteys- tai merkistökohtainen ero on yhä varmentamatta.
3. **`-g` pelkästään tislaus-/reseptisivujen merkkinä:** Nykyisessä `ZL3b-n.txt`-transkriptiossa `-g`-loppuiset sanat ovat suhteellisesti tiheimpiä `Astro/Zodiac`- (`6.9 / 1 000`) ja `Herbal`- (`4.9 / 1 000`) osioissa, eivät resepteissä (`1.3 / 1 000`).
4. **`oror` universaalina linjanlopetuksena:** Itsenäisenä sanana (`,`-välit yhdistettynä) `oror` esiintyy `8` kertaa (`4` rivin lopussa `50.0 %`, `1` lappu, `1` rivin alussa `f116v`:ssä, `2` rivin keskellä). Myös pidemmät `*oror*`-muodot (`N = 24`) painottuvat tavallista enemmän rakenteellisiin reunoihin (`PF 20.8 %`, `LL 20.8 %`, `S 12.5 %`, kun tavallisilla `-or`-sanoilla `LL` on vain `6.0 %`), mukaan lukien kappaleen loput (`okorory`, `okchedyoror`). Kuitenkin `PF`-sijainnit selittyvät pitkälti `p-/t-`-etuliitteillä, `34 %` (`11/32`) esiintyy yhä rivin keskellä, ja otos (`N = 32`) on pieni – joten vaikka `oror`-muodoissa näkyy aito reunapainotus, universaalia sulkukomentoa ei voida tällä perusteella vahvistaa.
5. **Semanttiset käännökset, `e/ee/eee`-kesto-oletukset ja kasvikuvien tulkitseminen putkistoiksi:** Vaikka `e/ee/eee`-pituuksissa näkyy paikallista ryvästymistä (`Z = +13.37`) ja historialliset tislaus- ja yrttioppaat ovat kiinnostava vertailukonteksti jatkotyölle, nämä yksittäiset merkitys- ja kuvatulkinnat ovat toistaiseksi varmentamattomia ja pidetään erillään tilastollisesta perustasosta.

---

## 5. Lähdekirjallisuus / References
* **Beinecke Rare Book & Manuscript Library, Yale University.** *The Voynich Manuscript*, MS 408.
* **Bowern, Claire L., and Luke Lindemann.** “The Linguistics of the Voynich Manuscript.” *Annual Review of Linguistics* 7 (2021): 285–308.
* **Currier, Prescott H.** “Some Important New Statistical Findings.” *New Research on the Voynich Manuscript*, 1976.
* **Reddy, Sravana, and Kevin Knight.** “What We Know About the Voynich Manuscript.” *ACL LaTeCH*, 2011.
* **Stolfi, Jorge.** “A Grammar for Voynichese Words.” (Morphological slot model.)
* **Voynich Lucidity (2026).** *Cross-Boundary Mutual Information (CBMI) in the Voynich Manuscript*.
* **Zandbergen, René.** *The Voynich Manuscript: Text Analysis and Transliteration* (`ZL3b-n.txt`).
* **Zattera, Massimo.** “A New Approach to Voynich Manuscript Text Structure” (Slot-based templates, 2022).
* *A Glyph Is Not a Letter, a Token Is Not a Word, a Space Is Not a Space: What the Units of Voynichese Are Not* (arXiv preprint, August 2026).