[![DOI](https://zenodo.org/badge/1398740941.svg)](https://doi.org/10.5281/zenodo.23916072)

# Voynich Manuscript Functional Syntax Framework (VFSF)
### Black-Box Structural & Sequence Analysis (Verified Baseline Summary)
**Tekijä:** Juho Olavi Laakso (Paimio, Finland)  
**Tila:** Kokeellinen tutkimus ja empiirinen dataverifiointi (*Work in Progress / Pre-release*)  
**Dokumentaatiolisenssi:** [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE)  
**Lähdekoodilisenssi:** [MIT License](LICENSE-CODE)

---

## 1. Projektin tarkoitus ja menetelmä

Tämä projekti tutkii Voynichin käsikirjoituksen (MS Beinecke 408, ZL-transkriptio `ZL3b-n.txt`: `5 376` riviä, `38 216` sanaa) tekstirakennetta *black-box*-lähestymistavalla ilman ennakko-oletuksia siitä, edustaako teksti tunnettua puhekieltä.

Tutkimuksessa testataan hypoteesia, jonka mukaan sanasto toimii paikkasidonnaisena, modulaarisena rakenteena:

`[ PREFIX ] + [ LIGATUURI / YDIN + INFIKSI ] + [ SUFFIX ]`

Aiemmissa kehitysvaiheissa kokeiltuja semanttisia tulkintoja (kuten tislausprosessisimulaatiota ja yksittäisten merkkien merkitysoletuksia) on testattu tiukoilla nollatesteillä. Alla esitetään selkeä erottelu siitä, mitkä löydökset kestivät kovat tilastolliset kontrollit ja mitkä varhaiset oletukset karsittiin pois.

---

## 2. Empiirisesti varmistetut rakennelöydökset (`ZL3b-n.txt`)

Kaikki alla olevat testit on suoritettu **sivun, kappaleen ja riviaseman (`PAR_FIRST`, `LINE_FIRST`, `LINE_MID`, `LINE_LAST`) lukitsevilla** Monte Carlo -permutaatioilla (`100–200` iteraatiota, siemen `1337`).

### 2.1 EVA-transkription epävarmat välit (`,`) ja todelliset sanarajat
EVA-transkriptiossa esiintyvät epävarmat/kapeat välit (`,`) selittävät huomattavan osan tietyistä rajapareista:
* `o -> r`: `50.5 %` tapauksista johtuu `,`-välistä
* `o -> l`: `44.8 %` johtuu `,`-välistä
* `s -> a`: `38.4 %` johtuu `,`-välistä
* `r -> a`: `27.9 %` johtuu `,`-välistä
* Sen sijaan `y -> q` (`1.0 %` pilkkuja) ja `n -> c` (`0.5 %` pilkkuja) esiintyvät lähes yksinomaan selvien `.`-sanavälien yli.

### 2.2 Välitön sananrajariippuvuus (`Etäisyys 1` vs. `Etäisyys 2`)
Kappaleen ja riviaseman lukitsemisen jälkeen vierekkäisten sanojen välillä on voimakas keskinäinen informaatio (*Mutual Information*), joka katoaa lähes kokonaan jo yhden sanan yli hypättäessä:
* `Suffix(i) -> Prefix(i+1)` (Etäisyys 1): `MI = 0.16752` vs. sekoitus `0.02236` (`Z = +140.25`)
* `Suffix(i) -> Prefix(i+2)` (Etäisyys 2): `MI = 0.03080` vs. sekoitus `0.02414` (`Z = +5.51`)
* `Vika merkki -> Eka merkki` (Etäisyys 1): `MI = 0.19596` vs. sekoitus `0.01338` (`Z = +220.88`)
* `Vika merkki -> Eka merkki` (Etäisyys 2): `MI = 0.02210` vs. sekoitus `0.01453` (`Z = +8.55`)

Kun epävarmat `,`-välit yhdistetään ja tutkitaan vain selviä `.`-välejä:
* **Suositut rajasiirtymät:** `'y' -> 'q'` (`Z = +47.79`), `'r' -> 'a'` (`Z = +33.73`), `'s' -> 'a'` (`Z = +22.59`), `'o' -> 'l'` (`Z = +17.74`), `'n' -> 'c'` (`Z = +16.35`), `'n' -> 'o'` (`Z = +12.92`).
* **Vältellyt rajasiirtymät:** `'y' -> 'a'` (`Z = -24.95`), `'n' -> 'q'` (`Z = -18.79`), `'r' -> 'q'` (`Z = -18.16`), `'y' -> 'c'` (`Z = -17.22`), `'y' -> 's'` (`Z = -15.92`).
* Kaikista `qo-`-alkuisista sanoista (`N = 4 661`) **72.6 %** seuraa `-y`-loppuista sanaa (pohjatason yleisyys `42.2 %`).

### 2.3 `-y`-päätteiden toiminnallinen jakautuminen (`Z = +15.39`, `p = 0.0050`)
Vaikka `,`-välit yhdistetään ja **sekä kappale, riviasema että loppukirjain `-y` lukitaan**, eri `-y`-loppuryhmät (`N = 12 613`) ennustavat seuraavan sanan alkua eri tavoin (`MI = 0.06193` vs. `0.03341`, `Z = +15.39`, `p = 0.0050`):
* **`-dy`** (`N = 6 570`): rivin lopussa `10.4 %`; seuraava sana alkaa `qo-`:lla `32.9 %` ajasta.
* **`-ey`** (`N = 3 891`): välttelee rivin loppua (`4.5 %` lopussa, `82.4 %` keskellä); seuraava sana alkaa `qo-`:lla `24.3 %` ja `l-`:llä `8.7 %`.
* **`-hy`** (`N = 1 992`): `9.7 %` lopussa; oma alku `ch-` (`30 %`), `sh-` (`16 %`).
* **`-ky` / `-ty`** (`N = 687` / `406`): `18.3–19.0 %` rivin lopussa; seuraava sana alkaa useammin `ch-`:lla (`18.7–19.2 %`) kuin `qo-`:lla (`13.5–13.6 %`).
* **`-ly`** (`N = 499`): vahvasti rivin loppuun painottuva (**`36.1 %`** rivin lopussa).

### 2.4 Suunnattu siirtymäketju rivien sisällä (`Z = +73.57`, `p = 0.0050`)
Sanojen välinen järjestys rivien sisällä on vahvasti yksisuuntaista (asymmetriaindeksi `1290.5` vs. sekoituksen keskiarvo `236.9`, `Z = +73.57`, `p = 0.0050`). Vahvimmat yksisuuntaiset siirtymät muodostavat toistuvan ketjun:

`BARE_OLR (ol/or/al/ar)` $\rightarrow$ `CH_DY (chedy/shedy)` $\rightarrow$ `QO_DY / QO_EY (qokedy/qokeey)` $\rightarrow$ `QO_OTH (qokal/qokain/...)` $\rightarrow$ `BARE_OLR / END_N`

Keskeisiä suunnattuja havaintoja (eteenpäin vs. taaksepäin):
* `QO_DY -> QO_OTH`: `217` vs. `49` (`Z = 11.71`)
* `CH_DY -> QO_DY`: `187` vs. `84` (`Z = 8.85`)
* `QO_OTH -> BARE_OLR`: `279` vs. `127` (`Z = 8.51`)
* `BARE_OLR -> CH_DY`: `251` vs. `95` (`Z = 7.70`)

### 2.5 Osioiden väliset rakenteelliset erot
* **Jatkuva teksti vs. kaaviolaput:** `Suffix -> Next Prefix` -kytkentä on selvästi voimakkain juoksevissa tekstiosioissa (`Recipes` x5.66, `Biological` x5.14, `Herbal` x3.32) verrattuna kaavio- ja purkkilappuosioihin (`Cosmo/Rosettes` x1.96, `Astro/Zodiac` x1.92, `Pharmaceutical` x1.64).
* **Ligatuurijakaumat:** `cth`-ligatuuri painottuu voimakkaasti `Herbal`-osioon (`530 / 11 376` sanaa eli `46.6 / 1 000`), mikä on yli 4.5-kertainen tiheys `Recipes`-osioon (`10.1 / 1 000`) verrattuna.

---

## 3. Avoimet kysymykset jatkotutkimukseen

Nyt varmistettu suunnattu sykli (`BARE_OLR -> CH_DY -> QO_DY/EY -> QO_OTH`) ja `-y`-luokkien eriävät asemat osoittavat, että käsikirjoituksen rivien sisällä on vahva, ei-satunnainen syntaksi. Seuraavat avoimet kysymykset ovat:
1. Selittyykö tämä suunnattu ketju parhaiten luonnollisen kielen lausekerakenteella (esim. partikkeli/prepositio + verbi/substantiivi + määre) vai rakenteellisella ohjekoodilla?
2. Muuttuuko ketjun sisäinen suhde systemaattisesti käsikirjoituksen kuvatyyppien tai Currier A / B -kielten välillä, kun `,`-välit pidetään yhdistettyinä?

---

## Lähdekirjallisuus / References
* **Beinecke Rare Book & Manuscript Library, Yale University.** *The Voynich Manuscript*, MS 408.
* **Bowern, Claire L., and Luke Lindemann.** “The Linguistics of the Voynich Manuscript.” *Annual Review of Linguistics* 7 (2021): 285–308.
* **Brunschwig, Hieronymus.** *Liber de arte distillandi de simplicibus*. Strasbourg, 1500. (Historiallinen konteksti eläinradan merkkien käytöstä prosessiajoituksissa.)
* **Currier, Prescott H.** “Some Important New Statistical Findings.” *New Research on the Voynich Manuscript*, 1976.
* **Stolfi, Jorge.** “A Grammar for Voynichese Words.” (Slot/crust-mantle-core -morfologiamalli.)
* **Zandbergen, René.** *The Voynich Manuscript: Text Analysis and Transliteration* (`ZL3b-n.txt`).
* **Zattera, Massimo.** “A New Approach to Voynich Manuscript Text Structure” (Slot-based morphological templates, 2022).