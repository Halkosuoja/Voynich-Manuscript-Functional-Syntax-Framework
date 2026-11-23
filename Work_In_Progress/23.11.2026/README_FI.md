[![DOI](https://zenodo.org/badge/1398740941.svg)](https://doi.org/10.5281/zenodo.23916072)

# Voynich Manuscript Functional Syntax Framework (VFSF)
### Black-Box-rakenne-, raja- ja rinnakkaiskorpusanalyysi (Päivitetty perustaso)
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
Kaikki sekvenssi-, raja- ja toistotestit on suoritettu **sivun, kappaleen ja tarkan riviaseman (`PF`, `LF`, `LM`, `LL`, `S`) lukitsevilla** Monte Carlo -permutaatioilla (`150–200` iteraatiota, kiinteä siemen `1337`), ja niitä on verrattu täsmälleen samalla mittarilla luonnollisiin kieliin, synteettisiin generaattoreihin sekä C-ohjelmakoodiin.
* **Empiirinen merkitsevyysraja:** Kaavalla `p = (k + 1) / (N + 1)` iteraatiomäärien `N = 200` ja `N = 150` alimmat mahdolliset arvot ovat `p < 0.005 (0/200)` ja `p < 0.007 (0/150)`. Ne raportoidaan otosrajoina jatkuvien todennäköisyyksien sijaan.
* **Yhteys vuoden 2026 kirjallisuuteen:** Vuoden 2026 tutkimukset (*"A Glyph Is Not a Letter, a Token Is Not a Word, a Space Is Not a Space"*, arXiv 2026; *Voynich Lucidity* CBMI, 2026) ovat päätyneet samaan ~0.2 bitin reunamerkki-informaatioon, epävarmojen välien toimintaan sekä Etäisyys 2 -pudotukseen. Tämä repositorio toistaa mittaukset `ZL3b-n.txt`-aineistolla ja laajentaa niitä yhtenäisellä liitinmatriisilla, kirjurivertailulla (Scribe 1–5), generatiivisilla mekanismitesteillä ja 11 tekstin vertailulla.

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

### 2.4 Kolme gallows-roolia (`BARE_GAL` vs. `BRIDGED_GAL` vs. `QO_GAL`)
| Ryhmä | Määrä (`N`) | `PF` (Kappaleen alku) | `LF` (Rivin alku) | `LM` (Rivin keskikohta) | `LL` (Rivin loppu) | Edeltävän lopun profiili |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **`BARE_GAL`** (`k/t/p/f-`) | 2 504 | **24.3 %** | 12.3 % | 53.8 % | 8.3 % | `-o: 2.47x`, `-l: 1.37x`, `-y: 1.36x` (hylkii `-s/-n/-r`) |
| **`BRIDGED_GAL`** (`ckh/cth/cph/cfh-`) | 763 | 0.5 % | 1.2 % | 79.3 % | **18.6 %** | `-o: 1.60x`, `-n: 1.49x`, `-s: 1.24x`, `-y: 0.75x` |
| **`PLAIN_CH`** (`ch-`, ei gallowsia) | 5 660 | 0.1 % | 2.6 % | 85.4 % | 11.1 % | `-n: 1.38x`, `-l: 1.24x`, `-r: 1.16x`, `-o: 0.70x` |
| **`QO_GAL`** (`qok/qot/qop/qof-`) | 4 379 | 0.4 % | 9.4 % | 82.6 % | 7.4 % | `-y: 1.75x` (hylkii kaikki muut: `0.18x–0.55x`) |

*Lyhenteet: `PF` = kappaleen ensimmäinen sana (`PAR_FIRST`), `LF` = rivin ensimmäinen sana (`LINE_FIRST`), `LM` = rivin keskiosa (`LINE_MID`), `LL` = rivin viimeinen sana (`LINE_LAST`), `S` = yksittäissana/lappu.*

### 2.5 Nimilappujen (`@L`) ja leipätekstin (`@P`) jyrkkä ero
IVTFF-locus-tagien analyysi paljasti tekstityyppien välisen toiminnallisen kuilun:
* **`qo-`-etuliite katoaa nimilapuista:** Leipätekstissä (`@P`) `qo-`-sanoja on **12.1 %**, kun taas nimilapuissa (`@L`, `N = 440`) niitä on **tasan 1 kpl (0.2 %)** ja kehäkaavioissa (`@R/@C`) **2.7 %**. Tämä vahvistaa, että `qo-` on tiukasti tekstinsisäinen sekvenssiside (joka vaatii edeltävän `-y`:n), eikä itsenäinen nimeävä sana.
* **`ot-` ja `ok-` hallitsevat nimilappuja:** Nimilapuissa `ot-` (`19.8 %`) ja `ok-` (`16.6 %`) kattavat yhdessä **36.4 %** kaikista sanoista (leipätekstissä vain `~6 %`).
* **Sanaston 83 % erillisyys:** Nimilappujen 385 uniikista sanasta **82.9 % (319 sanaa) esiintyy VAIN nimilapuissa**, eikä lainkaan leipätekstissä.

### 2.6 Kirjurien 1–5 ja lehtivihkojen (Quiret) säännönmukaisuus
Analyysi Lisa Fagin Davisin (2020) viiden kirjurin ja 20 lehtivihkon yli osoitti:
* **`y -> qo` -liitinlaki on universaali:** Se toimii poikkeuksetta kaikilla viidellä kirjurilla (Scribe 1: `54.3 %`, Scribe 2: `87.5 %`, Scribe 3: `64.6 %`, Scribe 4: `73.4 %`, Scribe 5: `58.7 %`, kaikkialla pohjatason `35–55 %` yläpuolella).
* **Kirjurikohtaiset erot:** Silloitetut gallowsit (`BRIDGED_GAL`) ovat lähes yksinomaan **Scribe 1:n työkalu (`5.5 %` vs. Scribe 2 ja 4: `0.4 %`)**. Scribe 2 (Bio B) on "hyperkytketty virtausmurre" (`qo-`: 25.0 %, $d_2$: 1.61 %), kun taas Scribe 5 (Astro) käyttää eniten nimeäviä `ot/ok`-tunnisteita (`23.9 %`).

### 2.7 Toistorakenne (`d1: A-A` ja `d2: A-X-A`)
* **Spesifi saman päätteen toistuminen (`w1 != w2`):** Identtisen päätteen toistuminen kahdella eri sanalla on kohonnut sekä Etäisyydellä 1 (`21.75 % vs. 19.44 %`, `Z = +8.66`) että Etäisyydellä 2 (`21.31 % vs. 19.41 %`, `Z = +6.25`). Tätä ajavat etuliitevaihtelut päätteissä `-dy` (`Z = +9.63`, esim. `shedy -> qokedy`), `-ey` (`Z = +6.20`, `okeey -> qokeey`) ja `-ol` (`Z = +5.18`, `otol -> chol -> shol`), kun taas `-aiin` välttää toistumista (`Z = -1.76`).
* **Vuorotteleva sanatoisto ($A - X - A$, `len(A) >= 4`, $N = 242$):** Toisin kuin luonnollinen proosa, joka välttää toistoa ($Z < 0$), Voynich suosii tarkkaa yhden sanan yli palaavaa vuorottelua (`0.78 %`, `Z = +4.82`; Currier A `0.71 %`, Currier B `0.82 %`), ja **`88.0 %` (`213 / 242`)** tapauksista tapahtuu **saman rivin sisällä**.
  * **Palaavat `A`-sanat:** Yleisin palaava sana on `daiin` (`28` kertaa = `11.6 %` kaikista toistoista vs. `2.35 %` perusyleisyys), jota seuraavat `shedy` (`16x`), `qokedy` (`14x`), `chedy` (`14x`), `chol` (`13x`) ja `qokeedy` (`12x`).
  * **Siltasanat `X` (`500` kappalesekoitusta):** Keskipaikalla rikastuvat sekä sidossanat (`okar` `12.99x, Z = +8.58`, `sheol` `7.12x, Z = +4.54`, `qol` `4.44x, Z = +3.32`, `chol` `3.50x, Z = +3.25`) että 1-merkin lähivariaatiot (`qokedy` `3.91x, Z = +4.44`, `qotedy` `4.85x, Z = +3.03`, `qokeedy` `2.76x, Z = +2.89`), tuottaen rakenteita kuten `qokedy - qokeedy - qokedy`, `qokeedy - qotedy - qokeedy`, `shedy - qol - shedy` ja `chol - daiin - chol`.

### 2.8 Kohdeglyyfit (`@L`) vs. prosessioperaattorit (`@P`) (Ligatuurikorjattu analyysi)
Kun EVA:n pilkkomat yhtenäiset käsikirjoitusligatuurit (`ckh`, `cth`, `cph`, `cfh`, `ch`, `sh`, `aiin`, `iin`, `ain`, `ee`, `oo`) yhdistetään atomisiksi glyyfeiksi, nimilappujen (`@L`, `N = 914` sanaa) ja leipätekstin (`@P`, `N = 31 806` sanaa) glyyfistö jakautuu kahteen toiminnalliseen järjestelmään:
* **Kohde-/luokkakoodisto (rikastuu nimilapuissa `@L`):** Avoimet `a`- ja `l/r`-pohjaiset rakenteet hallitsevat nimilappuja: `fa` (`8.06x`), `la` (`6.30x`), `rd` (`6.24x`), sananloppuinen `-a` (`6.04x`), `ry` (`5.82x`), `ra` (`5.37x`), `of` (`4.69x`), `sy` (`4.60x`), `ly` (`4.59x`) ja `ls` (`4.15x`).
* **Operaattorikoodisto (katoaa lähes täysin nimilapuista):** `qo-` (`19.1x` harvinaisempi `@L`:ssä, `9` vs. `5 200`), `p-` (`15.4x`), `dain` (`12.4x`, `1` vs. `406`), `aiin-` (`9.2x`), `chee-` (`7.7x`) ja `cth-` (`7.0x`) toimivat lähes yksinomaan juoksevan tekstin operaattoreina.
* **Purkki- ja kasvinosalappujen parit (`N = 14` `a/b/c`-paria):** Saman esineen vierekkäiset laput jakavat pidemmän yhteisen glyyfijakson kuin satunnaiset saman sivun laput (`1.79` vs. `1.37` glyyfiä, `p = 0.0470`, `1 000` sekoitusta; esim. `okaradag / okary`, `okeoly / yteold`, `keoraiiin / okeody`).
* **Syntaktinen kytkentä leipätekstissä:** Kun `@L`-tyyppinen kohdesana esiintyy juoksevassa tekstissä (`N = 2 846`), sen oikealle puolelle lukittuvat tilastollisesti merkitsevästi `saiin` (`2.07x`, `Z = +4.08`) ja `daiin` (`1.28x`, `Z = +2.50`, `500` kappalesekoitusta).

### 2.9 Sanaston morfologinen kompressio ja Currier A/B -rekisterit (`N = 32 553`)
Kun kuvakatkokset (`<->`, `<~>`) erotetaan oikeiksi sanaväleiksi ja sanoista kuoritaan etu- ja loppuliitteet (`7 954` uniikkia pintasanaa $\rightarrow$ `2 460` uniikkia perusydintä):
* **Äärimmäinen sanastokompressio:**
  * **Top-9 ydintä** kattaa **50 %** koko käsikirjoituksen sanoista.
  * **Top-46 ydintä** kattaa **80 %** koko käsikirjoituksen sanoista.
  * **Top-225 ydintä** kattaa **90 %** koko käsikirjoituksen sanoista.
* **Currier A ja B käyttävät samaa ydinjärjestelmää eri vokaalirekisterissä:**
  * **`e`-tila (`5 321` esiintymää, `16.3 %`):** `chedy`, `shedy`, `qokeedy`, `qokeey` – **81 % Currier B** (ja `ed`-ydin **99 % Currier B**).
  * **`o`-tila (`2 338` esiintymää, `7.2 %`):** `chol`, `chor`, `shol`, `sho` – **65 % Currier A**.
  * **`a`-tila (`2 019` esiintymää, `6.2 %`):** `ar`, `qokal`, `qokar`, `al` – **81 % Currier B**.
* **Koneistokerros (80 %) vs. sisältökerros (20 %):** Top-46-ytimien ulkopuolinen sisältökerros (`264` ydintä, `N >= 5`) keskittyy voimakkaasti tekstin rakenteellisiin reunoihin: kappaleen avaukseen `PF` (**`7.55x`**, `7.4 %` vs. `1.0 %`) ja rivin loppuun `LL` (**`1.67x`**, `18.5 %` vs. `11.1 %`), kun taas rivin keskiosa (`LM`) on pääosin Top-46-koneistoa (`78.3 %`).

### 2.10 Rivin reunakehys ja syklinen lausekielioppi
Distributiivinen PPMI-klusterointi (`103` yleisintä sanaa, `N >= 45`, `6` rooliluokkaa) ja rivipaikka-analyysi paljastavat itsenäisen rivitason lausekehyksen:
* **Rivin reunamerkit (`LF` ja `LL`):**
  * **Rivin aloittajat (`LF`, ei `PF`):** `d`- ja `s`-alkuiset muodot: `dshedy` (`90.6 %` rivin alussa, `8.73x`), `sor` (`57.8 %`, `5.57x`), `sain` (`50.7 %`, `4.89x`), `sar` (`41.7 %`, `4.01x`), `saiin` (`40.6 %`, `3.91x`), `sho` (`28.6 %`), `dain` (`24.5 %`) ja `daiin` (`20.3 %`).
  * **Rivin lopettajat (`LL`):** `-am`- ja `-y`-päätteiset muodot: `am` (`77.1 %` rivin lopussa, `6.09x`), `oly` (`67.9 %`, `5.37x`), `otam` (`65.1 %`, `5.15x`), `dam` (`64.8 %`, `5.12x`), `dy` (`34.9 %`, `2.76x`), `cthy` (`26.5 %`) ja `dal` (`24.6 %`).
* **Merkitsevimmät 3 sanan lauseketjut (`500` kappalesekoitusta):**
  * **Vuorottelusilmukka (`C3 <-> C6`):** `chedy`-luokka (`ch/sh-`) ja `qokain`-luokka (`qo-` + `-ain/-al/-ar`) vuorottelevat: `C3(chedy) -> C6(qokain) -> C3(chedy)` (`131 vs. 76.7`, `1.71x`, **`Z = +6.75`**) ja `C6(qokain) -> C3(chedy) -> C6(qokain)` (`91 vs. 53.9`, `1.69x`, **`Z = +5.35`**).
  * **Ketjuuntuva tila (`C2`):** `qokeedy`-luokka (`qo-` + `-edy/-eey`) muodostaa peräkkäisiä ketjuja: `C2(qokeedy) -> C2(qokeedy) -> C2(qokeedy)` (`230 vs. 169.6`, `1.36x`, **`Z = +4.84`**).
  * **Avausketjut:** `C5(daiin) -> C3(chedy) -> C6(qokain)` (`84 vs. 51.7`, `1.63x`, **`Z = +4.84`**) ja `C4(ol) -> C3(chedy) -> C2(qokeedy)` (`92 vs. 58.0`, `1.59x`, **`Z = +4.65`**).
  
  ### 2.11 Kappaleen sisäinen tilasiirtymä ja avaus-/lopetusrivin avainsanat (`N = 668`)
Monirivisten kappaleiden ($\ge 3$ riviä) vertailu riviltä 1 (`Avaus`) keskiriveille (`Keski`) ja viimeiselle riville (`Loppu`) osoittaa tilastollisesti merkitsevän suunnatun tilasiirtymän sekä tähtiosiossa (`Quire 20`, $N = 232$, Jensen–Shannon `0.55100 vs. 0.40945`, `p < 0.001`) että muussa käsikirjoituksessa ($N = 436$, `0.53548 vs. 0.36955`, `p < 0.001`, `1 000` rivijärjestyspermutaatiota):
* **Suunnattu etuliite- ja päätegradientti (`Rivi 1 -> Keskirivit -> Rivi N`):**
  * **Alkupainotteiset rakenteet (vähenevät loppua kohti):** `gallows (p/t/k/f)` (`16.4 % -> 4.0 % -> 3.0 %` Quire 20; `15.5 % -> 5.7 % -> 5.3 %` muu), `-dy/-edy`-päätteet (`25.3 % -> 19.4 % -> 17.3 %` Quire 20; `20.0 % -> 18.3 % -> 15.1 %` muu) sekä `qo-` (`20.3 % -> 18.2 % -> 13.7 %` Quire 20).
  * **Loppupainotteiset rakenteet (kasvavat loppua kohti):** `ch/sh-` (`18.0 % -> 25.0 % -> 29.5 %` Quire 20), `d/s-` (`3.7 % -> 7.0 % -> 8.8 %` Quire 20; `12.1 % -> 16.3 % -> 17.9 %` muu), `y-` (`2.0 % -> 3.5 % -> 6.4 %`) sekä `-aiin/-ain`-päätteet (`15.0 % -> 22.1 % -> 24.5 %` Quire 20; `13.2 % -> 15.8 % -> 17.2 %` muu).
  * **Kappaleen läpi vakiot:** `o-` (`ok/ot/ol/or`, `~20–24 %`), `-ol/-al` (`~11–15 %`) ja `-or/-ar` (`~10–14 %`) pysyvät muuttumattomina alusta loppuun.
* **Avausrivin (`Rivi 1`) avainsanaperhe:** Koko avausrivi (myös rivin sisäiset sanat) rikastaa voimakkaasti `p`-gallowsin ja `ch`-ytimen yhdistelmiä: `qopchedy` (`81.5 %` Rivi 1:llä, `4.46x`), `opchedy` (`80.5 %`, `4.41x`), `opchey` (`80.0 %`, `4.38x`), `qotchedy` (`47.8 %`), `pchedy` (`44.4 %`), `okchedy` (`40.0 %`) ja `qokchedy` (`37.8 %`).
* **Lopetusrivin (`Rivi N`) ja kappaleen päätössanan (`PAR_LAST`) avainsanat:** Lopetusrivillä rikastuvat `dchedy` (`36.0 %`, `3.11x`), `olor` (`34.6 %`, `2.99x`), `cheody` (`29.3 %`), `chedal` (`28.6 %`) ja `sain` (`24.6 %`). Koko kappaleen viimeisenä sanana rikastuvat erityisesti `olkam` (`30.0 %` esiintymistä kappaleen päätössanana, `14.10x`), `olor` (`19.2 %`, `9.04x`), `okeeey` (`14.3 %`, `6.72x`) ja `orain` (`13.6 %`, `6.41x`).

### 2.12 Transkription robustisuus ja paleografinen audit (`ZL3b-n.txt`, `@P`)
Koko leipätekstin (`27 705` selvää `.`-väliä ja `2 461` epävarmaa `,`-väliä = `8.2 %` väleistä) paleografinen tarkastus osoittaa, että VFSF-perustaso on vakaa lukutapavaihteluille:
* **Lukutapojen invarianttius:** Tekstissä on `652` hakasulkeisiin merkittyä kaksoislukutapaa (`[a:b]`, `~2.0 %` sanoista) ja `131` harvinaista `@numero;`-erikoisglyyfiä (`0.4 %`). Yleisimmät kaksoislukutavat koskevat merkkejä `[o:a]` / `[a:o]` (`141` kpl), `[s:r]` / `[r:s]` (`91` kpl) ja `[ch:ee]` / `[ee:ch]` (`24` kpl). Kun kaikkien kaksoislukutapojen tilalle vaihdetaan toinen vaihtoehto, uniikin sanaston Jaccard-yhdenmukaisuus pysyy tasolla **`0.935` (`93.5 %`)**.
* **Epävarmojen `,`-välien vaikutus:** Pilkkuvälien erottaminen sanaväleiksi kasvattaa sanamäärää `+2 454` sanalla (`+7.5 %`), mutta pienentää uniikkien sanamuotojen määrää (`7 929 -> 6 952`), koska pilkuilla erotetut jaksot koostuvat pääosin olemassa olevien lyhyiden sanojen yhdistelmistä (`o,l`, `s,aiin`, `d,aiin`).

### 2.13 Erikoislopetusrivit (`=Pt`, `+Pr`, `+Pc`) ja osiokohtaiset kappalekehykset
Visuaalisesti muusta tekstistä erotetut lopetusrivit (`=Pt` häntärivi, `+Pr` oikealle tasattu, `+Pc` keskitetty; $N = 37$ riviä, $112$ sanaa, keskipituus `3.03` sanaa) eroavat sanastoltaan tilastollisesti merkitsevästi tavallisista `+P0`-lopetusriveistä ($N = 662$, Jensen–Shannon `0.80890 vs. 0.61217`, `p < 0.001`, `1 000` permutaatiota):
* **Erikoislopetusrivien pääteprofiili:** `-am/-m`-päätteet yli kolminkertaistuvat (`7.1 % vs. 2.2 %`, `+5.0 %-yks.`) ja `-ol/al/or/ar` kasvaa (`28.6 % vs. 25.5 %`), kun taas `-aiin/-n` vähenee (`15.2 % vs. 20.7 %`).
* **Osiokohtainen avaus- ja päätösvertailu ($N \ge 2$ riviä):**
  * **Universaali avaus (`PF`):** Kaikissa viidessä pääosiossa (`Herbal A`, `Pharma A`, `Herbal B`, `Bio B`, `Quire 20`) kappaleen avaus on lukittu `p`-gallowsin (`pc-`, `po-`) ja `t`-gallowsin (`to-`, `tc-`, `ts-`) yhdistelmiin (`25–43 %` kaikista aloituksista).
  * **Osiokohtainen sulku (`PAR_LAST`):** `Herbal A`:ssa ($N = 190$) kappale päättyy yleisimmin `-aiin/-n`-päätteeseen (`30 %`, yksin `daiin` `20` kertaa = `10.5 %`), `Bio B`:ssä ($N = 91$) `-dy/-edy`-päätteeseen (`34 %`, `shedy`, `olor`, `lshedy`, `chedy`; `-aiin/-n` vain `7 %`), ja `Quire 20`:ssä ($N = 285$) tasaisesti `-y/-ey` (`24 %`), `-aiin/-n` (`23 %`) ja `-dy/-edy` (`21 %`) -päätteisiin.

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
3. **Voynich asettuu selvästi erilleen sekä luonnollisesta proosasta että C-ohjelmakoodista:** Oikea C-koodi (`sqlite3_35k.txt`) säilyttää peräti **`88.3 %`** rajainformaatiosta vielä Etäisyydellä 2 (monisanaiset koodikaavat). Englanti ja suomi säilyttävät `20–38 %` etäisyydellä 2, kun taas latinan Etäisyys 1 -taso jää matalaksi (`2.12x–2.46x`). Voynich yhdistää korkean Etäisyys 1 -kytkennän (`11.35x`, `+0.1489` bittiä), **`95.4 %`:n pudotuksen Etäisyydellä 2**, positiivisen `d1/d2`-toiston (`Z = +2.49 / +5.00`) ja yhden `-y`-päätteeseen sitoutuneen etuliitteen (`qo-`, `13.1 %` koko tekstistä).

### 3.1 Generatiivinen synteesivertailu (Aito Voynich vs. VFSF-tilakone)
Kun `ZL3b-n.txt`:n kappale- ja rivirakenteilla generoidaan synteettistä tekstiä VFSF-säännöillä (`paikka + rooliluokka + reunaliitin`), pelkkä 1-askeleen tilakone toistaa rajainformaation täydellisesti, mutta vaatii erillisen 2-askeleen sanakaiun `A - X - A` -toiston tuottamiseksi:

| Aineisto / Synteesimalli | Etäisyys 1 MI | Etäisyys 2 MI | Pudotus (Et. 2) | `A - X - A` (%) | `A - X - A` ($Z$) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Aito Voynich (`ZL3b-n.txt`)** | `0.14805` | `0.01575` | `89.4 %` | `0.78 %` | **`+4.82`** |
| **Malli 1: Paikkalukittu nolla** | `0.01473` | `0.00812` | `44.9 %` | `0.28 %` | `+1.64` |
| **Malli 2: VFSF 1-askeleen tilakone** | `0.15283` | `0.01152` | `92.5 %` | `0.25 %` | `+0.52` |
| **Malli 3: VFSF + 2-askeleen kaiku** | `0.15329` | `0.01090` | `92.9 %` | `0.71 %` | `+16.41` |

---

## 4. Tällä hetkellä varmentamattomat ja perustasosta rajatut hypoteesit (Methodological QA)

Seuraavat varhaisempien kehitysvaiheiden (`v1.5–v3.8.2`, `Digital Twin v2.0`) hypoteesit eivät saaneet tilastollista tukea nykyisissä nollatesteissä `ZL3b-n.txt`-aineistolla, minkä vuoksi ne on **rajattu pois varmistetusta empiirisestä perustasosta**. Se, ettei yksittäinen toteutus läpäissyt testiä nykyisellä EVA-transkriptiolla, ei vielä sulje lopullisesti pois kaikkia mahdollisia tulkintamuotoja – erityisesti kun otetaan huomioon EVA-merkistön tunnetut rajoitukset (ligatuurien pilkkominen, epävarmat välit, harvinaisten merkkien kuten `g` tulkintaerot) sekä historiallisen kuvavertailuaineiston tämänhetkinen rajallisuus. Nykyisellä näytöllä näitä ei kuitenkaan ole voitu osoittaa todeksi:

1. **Tislaussimulaattori (`Digital Twin v2.0`):** Testatuilla fysiikkaparametreilla (`1 000` sekoitusta) satunnainen sanajärjestys saavutti vastaavan tai suuremman tuoton ja turvallisuustason kuin aito teksti (`p = 0.52–0.72`). Nykyinen parametrimalli ei siis erottele aitoa järjestystä kohinasta.
2. **`-ain` vs. `-aiin` tulkitseminen nimenomaan eri painetiloiksi:** Tilastolliset testit (`Testi A`, `F5`, `F6`) osoittavat, että `i`- ja `ii`-muodot ovat paradigmaattisesti korvattavissa (`r = 0.90–0.94`) ja pysyvät kappaleen sisällä täysin vakioina (`63.3 % -> 63.5 %`, `p = 0.9301`), mutta toimivat staattisena osiorekisterivakiona (`Herbal/Pharma` suosii `ii`:tä `3.4:1` vs. `Bio` `0.8:1`). Niiden semanttinen tulkitseminen juuri painetiloiksi on kuitenkin yhä varmentamatta.
3. **`-g` pelkästään tislaus-/reseptisivujen merkkinä:** Nykyisessä `ZL3b-n.txt`-transkriptiossa `-g`-loppuiset sanat ovat suhteellisesti tiheimpiä `Astro/Zodiac`- (`6.9 / 1 000`) ja `Herbal`- (`4.9 / 1 000`) osioissa, eivät resepteissä (`1.3 / 1 000`).
4. **`oror` universaalina linjanlopetuksena:** Itsenäisenä sanana (`,`-välit yhdistettynä) `oror` esiintyy `8` kertaa (`4` rivin lopussa `50.0 %`, `1` lappu, `1` rivin alussa `f116v`:ssä, `2` rivin keskellä). Myös pidemmät `*oror*`-muodot (`N = 24`) painottuvat tavallista enemmän rakenteellisiin reunoihin (`PF 20.8 %`, `LL 20.8 %`, `S 12.5 %`, kun tavallisilla `-or`-sanoilla `LL` on vain `6.0 %`), mukaan lukien kappaleen loput (`okorory`, `okchedyoror`). Kuitenkin `PF`-sijainnit selittyvät pitkälti `p-/t-`-etuliitteillä, `34 %` (`11/32`) esiintyy yhä rivin keskellä, ja otos (`N = 32`) on pieni – joten vaikka `oror`-muodoissa näkyy aito reunapainotus, universaalia sulkukomentoa ei voida tällä perusteella vahvistaa.
5. **Yksittäiset sanakäännökset ja kasvikuvien tulkitseminen putkistoiksi:** Vaikka `e/ee/eee`-pituuksien rakenteellinen rooli syntaksista riippumattomana (`F1`: MI-säilyvyys `104.3 %`) ja kappaleen keskivaiheeseen kasvavana dynaamisena aste-/kestoparametrina on nyt tilastollisesti vahvistettu (`F6`: `25.9 % -> 34.4 %`, `p < 0.0010`), yksittäiset semanttiset käännökset sekä kasvi-, nymfi- tai lieriökuvien tulkitseminen putkistoiksi tai tislauslaitteiksi ovat toistaiseksi varmentamattomia ja pidetään erillään tilastollisesta perustasosta.
6. **Sivukohtaiset kasvien erisnimet (`Herbal` ↔ `Pharma` -kuvaparit ja `@Lc/@Lf`-tunnisteet):** Tutkijoiden kommenteissa samoiksi kasveiksi tunnistettujen sivuparien (`N = 14` paria, `1 000` satunnaista Herbal–Pharma-verrokkiparia) välillä harvinaisten sanojen (`2..30x`) Jaccard-vastaavuus ei ylitä satunnaistasoa (`0.0083` vs. saman kielimuodon nolla `0.0150`, `p = 0.9590`), eikä Top-46-koneiston ulkopuolisissa sisältöytimissäkään ole tilastollisesti merkitsevää eroa (`0.0364` vs. `0.0280`, `p = 0.1648`). Myöskään Pharma-osion lieriö- ja juuririvien `@Lc/@Lf`-tunnisteet eivät toistu suoraan alla olevassa `@P0`-kappaleessa satunnaista enempää (`1.36 %`, `p = 0.9021`), eivätkä `@L`-tyyppiset sanat keskity yksittäisille sivuille tiheämmin kuin muut sanat (`1.117` vs. `1.287` esiintymää/sivu). Näin ollen ytimet ja `@L`-tunnisteet toimivat toistuvina luokka- tai tilamääreinä, eivät sivukohtaisina lajierisniminä.
7. **`daiin / dain` tasavälisenä lauseenrajaajana:** `daiin`- ja `dain`-sanojen välinen etäisyys kappaleissa (`keskiarvo 13.07 sanaa`, `N = 465` väliä) on suhteelliselta hajonnaltaan suurempi kuin satunnaisessa sanajärjestyksessä (`CV = 1.389` vs. `1.212`, `p = 0.9820`), mikä osoittaa niiden esiintyvän ryvästyneissä rinnakkaisrakenteissa (esim. `f75r`: `dain ol sheol / dain ol qoly darajy`) eikä tasamittaisina välimerkkeinä.
8. **Tähtisymbolien visuaaliset muodot kappaleen sisällön koodina (`Quire 20`, `f103r–f116r`):** Tähtiosion `322` kappaleen (`9 523` sanaa) analyysi (`1 000` permutaatiota) osoittaa, ettei marginaalitähtien visuaalisilla ominaisuuksilla ole tilastollisesti merkitsevää vaikutusta kappaleen sanastoprofiiliin: tumma vs. vaalea tähti (`Dark` $N=16$ vs. `Light` $N=306$, Jensen–Shannon `0.52907 vs. 0.51129`, `p = 0.1898`), pisteellinen vs. pisteetön tähti (`Dotted` $N=148$ vs. `Plain` $N=174$, `0.33234 vs. 0.32932`, `p = 0.2178`) ja sakaraluku (`7` vs. `8` sakaraa, `N = 305`, `0.34036 vs. 0.33795`, `p = 0.2787`).
9. **Pitkän kantaman alku–loppu-kytkentä kappaleen yli (`PAR_FIRST` / `Rivi 1` $\rightarrow$ `PAR_LAST` / `Rivi N`):** Ositettu permutaatiotesti (`N = 668` monirivistä kappaletta, `1 000` sekoitusta saman osion ja Currier-kielen sisällä) osoittaa, ettei kappaleen avaustyyppi ennusta kappaleen päätössanaa (`MI = 0.03174 vs. 0.02908`, `p = 0.3337`) eikä lopetusrivin hallitsevaa päätettä (`MI = 0.04035 vs. 0.03308`, `p = 0.1738`). Kappaleen rakenteellinen eteneminen on siten paikalliseen asemaan sidottu tilagradientti, ei kaukaa lukittu syöttö–tulos-pari.


## 5. Käänteispurkumalli (VFSF v4.0), falsifiointitestit (F1–F7) ja täydellinen koodikirja

Kylmän datan osioanalyysien (`Herbal`, `Zodiakki`, `Pharma`, `Bio`, `Quire 20`), paradigmaattisen korvattavuusanalyysin (`Testi A`) sekä seitsemän nollatestatun falsifiointikokeen (`F1–F7`, `ZL3b-n.txt`, `,`-välit yhdistettynä, `PF/LF/LM/LL`-asemien lukitus) perusteella Voynichin käsikirjoitus ei ole luonnollista puhuttua kieltä eikä aakkospohjaista salakirjoitusta. Kyseessä on **modulaarinen, tila- ja operaattoripohjainen formaali merkintäjärjestelmä (ideografinen/rakenteellinen koodisto)**, joka kuvaa syklisiä ja vaiheittaisia prosesseja.

### 5.1 Koko tutkimuksen keskeiset empiiriset tulokset (`F1–F7`)

| Testi | Tutkimuskysymys | Empiirinen tulos (`ZL3b-n.txt`) | Tilastollinen tulos | Johtopäätös |
| :--- | :--- | :--- | :--- | :--- |
| **Testi A** | Paradigmaattinen korvattavuus (`w1 ___ w2`) | `daiin=dain` (`r=0.938`), `chedy=shedy` (`r=0.918`), `qokeedy=qokedy` (`r=0.915`) | Kosinisamankaltaisuus `0.85–0.94` | EVA-kaksoismuodot (`ii/i`, `ee/e`, `ch/sh`) jakavat saman syntaktisen paikan. |
| **Testi B & C1** | Zodiakki-kehät (`@Lz` vs. `@Cc`, `f70v2–f73v`) | `@Lz` kääntyy kohdassa `f72v3`: `ot+a` (`79.1%`) → `ok+e` (`53.5%`); `@Cc` pysyy vakiona | `@Lz`: **`p < 0.001`**; `@Cc`: `p = 0.21–0.93` | `@Cc` on vakio-operaatio; `@Lz`-laput koodaavat vaiheen/tilan muutosta. Sisä- ja ulkokehä ovat samanarvoiset (`p = 0.289`). |
| **Testi D & F2** | Pharma-tunnisteet (`@Lc` vs. `@Lf` vs. `@P0`) | `@L`-sanat toistuvat alla olevassa `@P0`:ssa vain `1.36 %`; sivunsisäinen `@Lc-@Lf` ero `+0.45` merkkiä | Testi D: `p = 0.902`; F2: `p = 0.206` | **Falsifioitu:** Tunnisteet eivät ole tekstin erisnimiä eivätkä riisuntahierarkia, vaan itsenäinen kaavioindeksi. |
| **Testi F1** | Redusoitu tilakone (`ii=i`, `ee=e`, `ch=sh`) | Raaka `MI 0.16812` → Normalisoitu `MI 0.17541` (`104.3 %`), sanasto `-16.7 %` | MI-säilyvyys **`104.3 %`** | Ydin määrittää syntaksin; merkkiyhdistäminen poistaa kohinaa ilman informaatiohäviötä. |
| **Testi F3** | Sisältöytimien järjestys (`PF` vs. `LM`) | Top-46-koneiston ulkopuoliset ytimet rikastuvat avaukseen (`PF/LM = 2.11x`) | **`p < 0.0020`** (`0/500`) | Kappaleilla on suunnattu algoritminen rakenne: syöte/kohde alussa (`PF`), vakiotoiminnot keskellä (`LM`). |
| **Testi F4** | Currier A → Currier B -ristiinnustettavuus | Currier A:n rajasiirtymät ennustavat Currier B:n (`-5.47868` bittiä/raja) | **`p < 0.0050`** (`0/200`) | Currier A ja B ovat yhden saman järjestelmän kaksi vokaali-/toimintarekisteriä. |
| **Testi F5 & F6** | Pituusparametrit (`e/ee/eee` vs. `i/ii/iii`) | `ee/(e+ee)` nousee `Rivi 1: 25.9 %` → `Keski: 34.4 %`; `ii/(i+ii)` pysyy vakiona (`63.3–65.0 %`) | `ee`: **`p < 0.0010`**; `ii`: `p = 0.9301` | **`ee/eee` = dynaaminen kesto/voimakkuus** kappaleen sisällä; **`ii/i` = staattinen osiorekisteri** (`Herbal` 3.4:1 vs. `Bio` 0.8:1). |
| **Testi F7** | Laajennetut atomit (`BRIDGED`, `L_PREFIX`, `SOLO_KT`, `PARTICLES`) | `BRIDGED` (`Herbal` 9.1 % → `Stars` 3.4 %); `L_PREFIX` (`Herbal` 0.4 % → `Stars` 5.1 %); `SOLO_KT` (`LL/LM = 0.39x`) | Osio- ja asemakohtainen eriytyminen | Silloitetut gallowsit ja `l-`-etuliitteet ovat käänteisiä osiorekistereitä; `oke/ote` on puhtaasti rivinsisäinen. |

---

### 5.2 Täydellinen laajennettu VFSF-koodikirja

#### 1. Etuliite-operaattorit (Syntaktinen asema ja kytkentä)
* **`p- / t- / k- / f-` (`BARE_GAL` → `INIT / RULE`):** Kappaleen avausoperaattori (`PF`, `76–80 %` Bio/Quire 20 -osioissa; vähenee loppua kohti `16 % -> 3 %`, `p < 0.001`). Aloittaa uuden säännön tai prosessiyksikön.
* **`qo-` (`THEN / FLOW`):** Puhtaasti tekstinsisäinen jatkuvuusoperaattori (`12–25 %` `@P`:ssä, `0.2 %` `@L`:ssä). Sitoutuu edeltävään `-y`-päätteeseen (`72.6 %`) ja kytkee peräkkäiset tilat yhteen.
* **`ok- / ot-` (`MODE / PHASE`):** Tilan tai vaiheen valitsin (esiintyy sekä `@L`-tunnisteissa `36–56 %` että leipätekstissä `12–21 %`). Zodiakin puolivälissä `ot-` (Tila 1: alku/nouseva/raaka) vaihtuu `ok-`:ksi (Tila 2: loppu/laskeva/käsitelty, `p < 0.001`).
* **`d- / s-` (`STEP / SHIFT`):** Rivin alun kehysoperaattori (`LF`, esim. `dshedy` 90.6 %, `sor` 57.8 %; kasvaa kappaleen loppua kohti `3.7 % -> 8.8 %`). Merkitsee uuden alavaiheen tai syklin rivin reunassa.
* **`l-` (`L_PREFIX`: `lchedy, lshedy, lkaiin` → `LINK / MOD`):** Rivinsisäinen (`LL/LM = 0.89x`) rekisterimuunnin, joka on lähes olematon `Herbal A`:ssa (`0.4 %`), mutta yleistyy `Bio B`:ssä (`3.7 %`) ja `Quire 20`:ssä (`5.1 %`).

#### 2. Ydinmoduulit ja ortogonaaliset intensiteettiparametrit
* **`ch/sh + e` (`PROC`):** Aktiivinen prosessi- ja käsittelyydin (`Bio B` 34.6 %, `Quire 20` 26.4 %). Kuvaa käynnissä olevaa toimintoa tai tilamuutosta.
* **`ch/sh + o` (`OBJ / STRUCT`):** Kohde- ja rakenneydin (`Herbal A` 22.1 % vs. `Bio B` 3.1 %). Kuvaa käsiteltävää ainetta, rakenneosaa tai kiinteää yksikköä.
* **`ckh / cth / cph / cfh` (`BRIDGED` → `COMP_STRUCT`):** Silloitetut gallows-ligatuurit (`Herbal A` 9.1 % → `Stars` 3.4 %). Toimivat `Herbal`- ja `Scribe 1` -rekisterin rakenteellisina yhdistelmäytiminä rivin keskellä ja lopussa (`LM` 79.3 %, `LL` 18.6 %).
* **`oke / ote / qoke / qote` (`SOLO_KT` → `SUB_PROC`):** Yksinäisen `k/t`-ytimen sisältävät prosessimuodot (`Bio` 13.7 %, `Stars` 13.0 % vs. `Herbal` 4.0 %). Välttävät rivin loppua (`LL/LM = 0.39x`) ja toimivat rivin sisäisinä apuoperaatioina.
* **`e` → `ee` → `eee` (`DUR / INT`):** **Dynaaminen kesto- tai voimakkuusaste (`p < 0.0010`).** Kasvaa kappaleen avausriviltä (`25.9 %`) keskiriveille (`34.4 %`): `e` = perustaso (1x), `ee` = pidennetty/voimistettu (2x), `eee` = maksimaalinen (3x).
* **`i` → `ii` → `iii` (`MED / UNIT`):** **Staattinen osio- ja väliainerekisteri (`p = 0.9301` kappaleen sisällä).** Erottaa osioiden perusluonteen: `ii` hallitsee `Herbal/Pharma`-osioita (`3.4:1`), kun taas yksittäinen `i` hallitsee `Bio`-osiota (`0.8:1`).
* **`daiin / dain` (`REF / STATE`):** Perusviitetila ja yleisin palaava ankkurisana `A - X - A` -vertailusilmukoissa (`11.6 %` kaikista vuorottelutoistoista).
* **`ol / or / al / ar / qol` (`PARTICLES` → `REL / BRIDGE`):** Lyhyet rivinsisäiset (`LL/LM = 0.55x`) kytkentä- ja siltasanat (`Bio` 5.0 %), jotka rikastuvat `A - X - A` -silmukoiden keskipaikalle (`qol` `4.44x`, `okar` `12.99x`).

#### 3. Loppupäätteet (Tila-arvot ja yksikön sulku)
* **`-dy / -edy` (`STATE_ACT`):** Merkitsee tilan aktiiviseksi ja kytkee sen seuraavaan `qo-`-operaattoriin (`-y -> qo-`).
* **`-al / -ar` & `-ol / -or` (`PARAM_A / PARAM_B`):** Kaksi paradigmaattisesti korvattavaa (`r = 0.86`), kappaleen läpi vakiota tilaparametria (esim. sisään/ulos, lisäys/poisto, ylä/ala), jotka hallitsevat myös `@L`-nimilappuja (`55–79 %`).
* **`-am / -om` (`END / LOCK`):** Prosessiyksikön tai säännön lopullinen sulkupääte (`PAR_LAST`, `31.2 %` Quire 20; `olkam` `14.10x` kappaleen päätössanana).

---

### 5.3 Järjestelmän toimintaperiaate yhdellä kaavalla
Koko Voynichin käsikirjoituksen tuottava tilakone noudattaa yhtä yhtenäistä muotoa:

$$\text{[INIT: } p/t/k/f\text{]} \;\rightarrow\; \text{[MODE: } ok/ot\text{]} + \text{[CORE: } CH/k/t + \{o, e^{(1..3)}, a, i^{(1..2)}\}\text{]} + \text{[PARAM: } -dy / -al / -ar\text{]} \;\xrightarrow{qo\text{-}}\; \dots \;\rightarrow\; \text{[END: } -am / -y\text{]}$$

Tämä malli selittää yhtenäisesti ilman ristiriitoja:
1. Miksi 1-askeleen rajakytkentä on erittäin voimakas (`11.35x`, `+0.149` bittiä), mutta romahtaa `95.4 %` heti Etäisyydellä 2 (paikallinen tilasiirtymä), samalla kun `A - X - A` -silmukat (`Z = +4.82`) toteuttavat lyhyet vertailupaluut.
2. Miksi kuvien tunnisteet (`@L*`) ja teksti (`@P`) eivät jaa erisnimiä (`p = 0.902`), vaan muodostavat kaavion indeksin ja sen suorituskoodin.
3. Miksi `Quire 20` yhdistää `Bio`-osion prosessikieliopin ja kuvallisten osioiden `ok-/ot-` + `-al/-ar` -luokituskoodiston yhteen kuvattomaan suorituskoodiin.

---

## 6. Lähdekirjallisuus / References
* **Beinecke Rare Book & Manuscript Library, Yale University.** *The Voynich Manuscript*, MS 408.
* **Bowern, Claire L., and Luke Lindemann.** “The Linguistics of the Voynich Manuscript.” *Annual Review of Linguistics* 7 (2021): 285–308.
* **Currier, Prescott H.** “Some Important New Statistical Findings.” *New Research on the Voynich Manuscript*, 1976.
* **Davis, Lisa Fagin.** “How Many Glyphs and How Many Scribes? Digital Paleography and the Voynich Manuscript.” *Manuscript Studies* 5, no. 1 (2020): 164–180.
* **Reddy, Sravana, and Kevin Knight.** “What We Know About the Voynich Manuscript.” *ACL LaTeCH*, 2011.
* **Stolfi, Jorge.** “A Grammar for Voynichese Words.” (Morphological slot model.)
* **Voynich Lucidity (2026).** *Cross-Boundary Mutual Information (CBMI) in the Voynich Manuscript*.
* **Zandbergen, René.** *The Voynich Manuscript: Text Analysis and Transliteration* (`ZL3b-n.txt`).
* **Zattera, Massimo.** “A New Approach to Voynich Manuscript Text Structure” (Slot-based templates, 2022).