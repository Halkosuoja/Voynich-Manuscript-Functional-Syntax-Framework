[![DOI](https://zenodo.org/badge/1398740941.svg)](https://doi.org/10.5281/zenodo.23916072)

# Voynich Manuscript Functional Syntax Framework (VFSF)
### Black-Box Structural, Boundary & Cross-Corpus Analysis
**Author:** Juho Olavi Laakso (Paimio, Finland)  
**Status:** Experimental black-box research & statistical verification (*Work in Progress / Pre-release*)  
**Documentation License:** [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE)  
**Code License:** [MIT License](LICENSE-CODE)  
[Suomeksi / In Finnish](README_FI.md)

---

## 1. Purpose and Methodology

This project investigates the surface text structure of the Voynich Manuscript (MS Beinecke 408, Zandbergen–Landini transcription `ZL3b-n.txt`: `5,376` lines, `38,216` raw tokens / `35,358` tokens after joining uncertain `,` spaces) using a **black-box** empirical approach, without assuming in advance whether the text represents a spoken natural language or a formal protocol.

The starting structural hypothesis models Voynich tokens as position-dependent modular strings:

`[ PREFIX ] + [ LIGATURE / CORE + INFIX ] + [ SUFFIX ]`

### Statistical Controls
All sequence, boundary, and repetition tests were evaluated against **folio-, paragraph-, and line-position-preserving (`PF`, `LF`, `LM`, `LL`, `S`)** Monte Carlo permutations (`150–200` iterations, fixed RNG seed `1337`), and benchmarked with the exact same script against natural-language, synthetic, and real software-code corpora.
* **Empirical p-value floor:** Using `p = (k + 1) / (N + 1)`, the lowest attainable values for `N = 200` and `N = 150` permutations are `p < 0.005 (0/200)` and `p < 0.007 (0/150)` respectively. These are reported honestly as permutation bounds rather than continuous probabilities.
* **Relation to 2026 literature:** Independent findings in 2026 (*"A Glyph Is Not a Letter, a Token Is Not a Word, a Space Is Not a Space"*, arXiv 2026; *Voynich Lucidity* CBMI, 2026) have converged on the same ~0.2-bit edge-glyph mutual information, uncertain-space behavior, and rapid Distance-2 collapse reported here. This repository independently reproduces those measurements on `ZL3b-n.txt` and expands them with a unified gallows/connector matrix, `-y`-subtype isolation, generative mechanism tests, repetition X-rays, and an 11-corpus cross-domain benchmark.

---

## 2. Key Empirical Findings (`ZL3b-n.txt`)

### 2.1 Uncertain Spaces (`,`) vs. Clear Spaces (`.`) in EVA
Transcribed uncertain/narrow spaces (`,`) account for a substantial fraction of specific character pairs across boundaries:
* `o -> r`: `50.5%` occur across `,`
* `o -> l`: `44.8%` occur across `,` (`ol` appears `5,507` times joined vs. `119` times across clear `.` spaces)
* `s -> a`: `38.4%` occur across `,` (`s+ai` appears `376` times joined vs. `127` across `.`)
* `r -> a`: `27.9%` occur across `,` (`r+ai` appears `425` times joined vs. `304` across `.`)
* By contrast, `y + qo` (`98.2%` space-separated, `3,382` vs. `61`), `n + ch` (`98.0%` separated, `1,294` vs. `26`), and `y + lk` (`96.5%` separated, `246` vs. `9`) act as near-strict word boundaries.

### 2.2 Immediate 1-Step Boundary Coupling (Distance 1 vs. Distance 2)
Even after joining `,` spaces and locking paragraph and line positions, adjacent tokens share strong edge-glyph mutual information (`MI`) that collapses almost completely at Distance 2:
* **Clear spaces (`,` joined):** Distance 1 = `MI 0.16327 vs. 0.01438` (`11.35x`, net `+0.1489` bits, `Z = +154.65`) $\rightarrow$ Distance 2 = `0.02252 vs. 0.01568` (`1.44x`, net `+0.0068` bits, `Z = +6.52`). **`95.4%`** of the net boundary signal disappears by Distance 2.
* **Even after also merging word-internal pairs (`o+l`, `r+ai`, `s+ai`):** Distance 1 remains `MI 0.14035 vs. 0.01474` (`9.52x`, net `+0.1256` bits), and **`95.1%`** still disappears at Distance 2 (`1.38x`).
* **Concentration at the boundary interface (global test within fixed prefixes):** Once the initial prefix of the next word is held constant (`ch-`, `sh-`, `ok-`, `ot-`), the preceding word's ending no longer shows statistically significant global predictive power over the full table of next-word endings (`p = 0.055–0.124`). Only within `qo-` words does a modest suffix-harmony residue remain (`Z = +2.66`, `p = 0.010`, e.g. `-ey -> qok+ey` `Z = +3.70`, `-dy -> qok+dy` `Z = +2.88`).

### 2.3 The Unified "Connector Matrix" (`Herbal` vs. `Bio + Recipes`)
Observed-to-expected ratios between `word_i[-1]` and `word_{i+1}[0]` divide initial glyphs into four distinct boundary classes, and **the same compatibility matrix operates in both `Herbal` (Currier A) and `Bio + Recipes` (Currier B)**:

* **`q-` (`qo-`, `13.1%` of the corpus):** `72.6%` follow `-y` (`1.72x` overall; `1.53x` Herbal / `1.66x` Bio+Recipes), while avoiding other endings (`0.25x–0.62x`).
* **Gallows (`k, t, p, f`):** Favor following `-o` (`1.66x–3.81x`, primarily `-sho/-cho/-sheo` words such as `sho -> koeam`, `cho -> cthy`), `-y` (`1.15x–1.56x`), and `-l` (`k/t` especially in Currier B at `2.76x / 1.91x`), while strongly avoiding `-s`, `-n`, and `-r` (`0.12x–0.52x`).
* **`a-` (`aiin, ain, al, ar...`):** Strongly favors following `-s` (`4.68x` overall; `4.60x` Herbal / `6.28x` Bio+Recipes, e.g. `ches -> aiin`) and `-r` (`2.99x`; e.g. `or -> aiin`, `ar -> al`), while strongly avoiding `-y` (`0.20x`).
* **`c-`, `o-`, `s-`:** Moderately favor `-n` (`1.23x–1.39x`), `-r`, and `-l`, and occur less often after `-y` (`0.73x–0.86x`).

### 2.4 Three Distinct Gallows Roles (`BARE_GAL` vs. `BRIDGED_GAL` vs. `QO_GAL`)
Although bare `k, t, p, f` share a common boundary profile, attaching a `ch`-bench (`ckh/cth/cph/cfh`) or `qo-` prefix transforms the token's positional and boundary behavior completely:

| Group | Count (`N`) | `PF` (Par. First) | `LF` (Line First) | `LM` (Line Mid) | `LL` (Line Last) | Preceding Ending Profile |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **`BARE_GAL`** (`k/t/p/f-`) | 2,504 | **24.3%** | 12.3% | 53.8% | 8.3% | `-o: 2.47x`, `-l: 1.37x`, `-y: 1.36x` (avoids `-s/-n/-r`) |
| **`BRIDGED_GAL`** (`ckh/cth/cph/cfh-`) | 763 | 0.5% | 1.2% | 79.3% | **18.6%** | `-o: 1.60x`, `-n: 1.49x`, `-s: 1.24x`, `-y: 0.75x` |
| **`PLAIN_CH`** (`ch-`, no gallows) | 5,660 | 0.1% | 2.6% | 85.4% | 11.1% | `-n: 1.38x`, `-l: 1.24x`, `-r: 1.16x`, `-o: 0.70x` |
| **`QO_GAL`** (`qok/qot/qop/qof-`) | 4,379 | 0.4% | 9.4% | 82.6% | 7.4% | `-y: 1.75x` (avoids all others: `0.18x–0.55x`) |

*Legend: `PF` = paragraph-initial token (`PAR_FIRST`), `LF` = line-initial token (`LINE_FIRST`), `LM` = mid-line token (`LINE_MID`), `LL` = line-final token (`LINE_LAST`), `S` = single-token label.*

All four bridged gallows forms (`ckh`, `cth`, `cph`, `cfh`) behave consistently (`77–85%` mid-line, `15–21%` line-final), forming a true syntactic hybrid between bare gallows (`-o: 2.47x`) and plain `ch` (`-n: 1.38x`).

### 2.5 `-y` Subtype Differentiation, Specific Suffix Echoing & Directed Cycle
* **Within-`-y` differentiation (`Z = +15.39`, `p < 0.005 [0/200]`):** With paragraph, line position, and final `-y` held constant (`N = 12,613`), preceding subtypes differ sharply: `-ey` (`4.5%` line-final), `-dy` (`10.4%` line-final, `32.9%` followed by `qo-`), `-hy` (`9.7%` line-final), `-ky/-ty` (`18.3–19.0%` line-final), and `-ly` (**`36.1%`** line-final).
* **Specific identical-suffix echoing (`w1 != w2`):** While global next-ending prediction vanishes inside fixed prefixes (Section 2.2), specifically testing whether **different adjacent tokens share the exact same ending (`w1_end == w2_end`)** yields elevated rates at both Distance 1 (`21.75% vs. 19.44%`, `Z = +8.66`) and Distance 2 (`21.31% vs. 19.41%`, `Z = +6.25`). This is driven by prefix-alternation on `-dy` (`Z = +9.63`, e.g. `shedy -> qokedy`), `-ey` (`Z = +6.20`, `okeey -> qokeey`), and `-ol` (`Z = +5.18`, `otol -> chol -> shol`), whereas `-aiin` avoids echoing (`Z = -1.76`).
* **Productive directed cycle:** Adjacent tokens exhibit strong one-way asymmetry (`BARE_OLR -> CH_DY -> QO_DY/EY -> QO_OTH -> BARE_OLR`) that persists even when all high-frequency words (`freq > 50`) are removed (`10,883` remaining pairs: `Z = +10.09`, `p < 0.007 [0/150]`), arising largely from the boundary connector rules above.

### 2.6 Generative Mechanism Tests & Repetition X-Ray (`d1: A-A`, `d2: A-X-A`)
To test *how* the observed profile can be generated, we tested both a forward transformation of natural prose and a reverse 1-step Markov boundary generator (`vfsf_mechanism_test.py`, `vfsf_repeat_xray.py`):

* **1-Step Boundary Generator (`35,358` tokens trained solely on `w_i[-1]`):** Reproduces Distance-1 coupling (`MI 0.17008 vs. 0.00756`, net `+0.1625` bits) and Distance-2 collapse (`2.1%` retention), **but fails** to reproduce Voynich's suffix echoing (`15.51% / 13.92%` vs. real `21.73% / 21.34%`) or its exact-word repetition (`d1 = 0.33%`, `d2 = 0.28%` vs. real `0.86%`, `0.96%`).
* **Mechanical Re-segmentation of Natural Language (`plinius_ii.txt` & `Matteus1548.txt`):**
  * A 1-character boundary shift (`A1`) overshoots massively (`+1.06–1.23` bits, `47x–63x`); a 2-character bigram substitution (`A3`) collapses vocabulary size (`388–612` unique words vs. `9,340` in `ZL3b-n.txt`).
  * Splitting continuous natural prose deterministically before stop/prefix glyphs `c/k/p/t/q` (`A2`) closely reproduces Voynich's Distance-1 net MI (`+0.132–0.162` bits) and Distance-2 collapse (`1.8–3.9%` retention), **but** produces almost zero identical-word repetition (`d1 = 0.01%`, `d2 = 0.09–0.10%`).
* **Opposite Repetition Signature (`d1` and `d2` vs. Prose):**
  Under paragraph- and line-position-locked shuffles, natural prose strongly *avoids* immediate and alternating word repetition:
  * `Matteus1548.txt` (1548 Finnish): `d1 = 0.11% vs. 1.15%` (`Z = -15.78`), `d2 = 0.62% vs. 1.15%` (`Z = -7.96`; only `42%` `>= 4` chars).
  * `plinius_ii.txt` (Classical Latin): `d1 = 0.01% vs. 0.49%` (`Z = -9.02`), `d2 = 0.37% vs. 0.50%` (`Z = -2.43`; `45%` `>= 4` chars).
  * `3DBenchy.txt` (3D STL geometry stream): `d1 = 0.00%` (`Z = -417.21`), `d2 = 0.00%` (`Z = -208.21`).
  * **`ZL3b-n.txt` (Voynich):** exhibits the *reverse* pattern: `d1 = 0.86% vs. 0.74%` (`Z = +2.49`, `105` unique words, `87% >= 4` chars) and **`d2 (A - X - A) = 0.96% vs. 0.71%` (`Z = +5.00`, `94` unique words, `83% >= 4` chars)**, driven by rhythmic near-variant alternation (`qokedy - qokeedy - qokedy`, `shedy - qokedy - shedy`) and bridged repeats (`chol - daiin - chol`).
  * While stripped C source code (`sqlite3_puhdas_prosessikoodi.txt`) also shows positive `d1/d2` (`Z = +63.15 / +235.65`), C code behaves completely differently from Voynich at Distance 2 (Section 3).
  * `kalevala_test_source.txt` (full Kalevala epic verse): `d1 = 0.19% vs. 0.47%` (`Z = -11.44`, `100% >= 4` chars), but `d2 (A - X - A) = 1.09% vs. 0.45%` (`Z = +21.19`, `97% >= 4` chars) due to formulaic poetic parallelism (*"vieri kyynel, vieri toinen"*).
  * **Preliminary Finnish folklore controls (uncleaned Gutenberg editions — `Arwoituksia.txt` 26,922 words, `Loitsurunoja.txt` 81,517 words, `vanhatRunot.txt` 176,652 words):** All three likewise showed positive `d2` (`Z = +6.15` to `+15.18`) alongside strongly negative `d1` (`Z = -6.17` to `-23.49`, even with rhyme refrains like *"lennä lennä"*), and high Distance-2 boundary retention (`38.0%`, `61.3%`, and `90.3%`, vs. `4.6%` in Voynich). *(Exact figures are tentative pending removal of editorial footnotes and variant markers.)*

---

## 3. Cross-Domain Benchmark (11 Corpora: Natural Languages, Generators & C Code)

All eleven corpora were evaluated identically using `universal_syntax_bench.py` under paragraph- and line-position-locked permutations (`150` iterations, seed `1337`):

| Text | Words | Dist. 1 (net MI & ratio) | Dist. 2 (net MI & ratio) | Retention (D2 / D1) | Directional Asym. | Top Bound Prefix (% of corpus) |
| :--- | :---: | :--- | :--- | :---: | :---: | :--- |
| **`control_slot.txt`** (Slot gen.) | 35,002 | `-0.00001` (`0.99x`) | `+0.00032` (`1.34x`) | – | `0.94x` (`Z=-0.36`) | `'ck-'` (`+3.6%`, *noise*) |
| **`control_selfcite.txt`** (1-word copy) | 35,000 | `+0.00018` (`1.04x`) | `+0.00075` (`1.15x`) | – | `0.97x` (`Z=-0.21`) | `'sh-'` (`+1.7%`, *noise*) |
| **`plinius_ii.txt`** (Classical Latin) | 17,452 | `+0.0225` (`2.46x`) | `+0.0004` (`1.02x`) | ~1.6% | `3.04x` (`Z=+18.21`) | `'es-'` (`1.6%`, `+12.3%`) |
| **`latin_abbrev.txt`** (Abbrev. Latin) | 17,453 | `+0.0174` (`2.12x`) | `+0.0002` (`1.02x`) | ~1.4% | `2.90x` (`Z=+16.04`) | `'es-'` (`1.6%`, `+12.1%`) |
| **`Herbarum.txt`** (Medieval Herbal Latin) | 2,434 | `+0.2129` (`3.33x`) | `+0.0313` (`1.28x`) | **14.7%** | `1.68x` (`Z=+4.38`) | `'ui-'` (`2.0%`, `+32.2%`) |
| **`Matteus1548.txt`** (1548 Old Finnish) | 25,170 | `+0.0344` (`2.64x`) | `+0.0071` (`1.35x`) | **20.5%** | `5.96x` (`Z=+51.20`) | `'et-'` (`1.9%`, `+17.4%`) |
| **`kalevalaTesti.txt`** (Finnish poetry) | 14,126 | `+0.0617` (`4.34x`) | `+0.0137` (`1.62x`) | **22.2%** | `2.31x` (`Z=+19.71`) | `'vä-'` (`1.6%`, `+35.7%`) |
| **`hamlet.txt`** (English drama) | 32,878 | `+0.0668` (`5.64x`) | `+0.0217` (`2.32x`) | **32.5%** | `4.73x` (`Z=+83.10`) | `'lo-'` (`1.3%`, `+38.1%`) |
| **`LinuxTesti.txt`** (English manual) | 5,774 | `+0.1429` (`2.70x`) | `+0.0548` (`1.65x`) | **38.3%** | `5.57x` (`Z=+33.18`) | `'ca-'` (`1.3%`, `+47.8%`) |
| **`sqlite3_35k.txt`** (Stripped C code) | 32,278 | `+0.2697` (`15.91x`) | `+0.2380` (`10.93x`) | **88.3%** | `4.45x` (`Z=+258.67`) | `'pr-'` (`4.3%`, `+56.8%`) |
| **`ZL3b-n.txt` (Voynich)** | 35,358 | **`+0.1489` (`11.35x`)** | **`+0.0068` (`1.44x`)** | **4.6%** | `3.80x` (`Z=+49.94`) | **`'qo-'` (`13.1%`, `+30.3%`)** |

### Benchmark Conclusions
1. **Directional asymmetry alone does not separate Voynich from prose or code:** 1548 Old Finnish (`5.96x`), English (`4.73x–5.57x`), C code (`4.45x`), and Latin (`3.04x`) exhibit comparable or higher directional asymmetry than Voynich (`3.80x`).
2. **Simple generators fail to reproduce boundary coupling:** Neither an independent slot-table generator (`0.99x`) nor a simple 1-word copy-and-mutate generator (`1.04x`) produces measurable cross-boundary coupling.
3. **Voynich occupies a distinct regime from both natural prose and real C source code:** C code (`sqlite3_35k.txt`) retains **`88.3%`** of its boundary mutual information at Distance 2 (multi-word type/expression chains) and loses directional asymmetry on rare words (`<=20`: `Z = +0.16`, `p = 0.404`). English and Finnish retain `20–38%` at Distance 2, while Latin shows weak Distance-1 coupling (`2.12x–2.46x`). Voynich uniquely combines strong Distance-1 coupling (`11.35x`, `+0.1489` bits), **`95.4%` loss at Distance 2**, positive `d1/d2` content-word repetition (`Z = +2.49 / +5.00`), and a single boundary-bound prefix (`qo-` after `-y`) spanning **`13.1%`** of the corpus.

---

## 4. Currently Unconfirmed & Excluded Hypotheses (Methodological QA)

The following exploratory hypotheses from earlier stages (`v1.5–v3.8.2`, `Digital Twin v2.0`) did not receive statistical support under the current null controls on `ZL3b-n.txt` and are therefore **held out of the verified empirical baseline**. Note that failing a specific test on the current EVA transcription does not permanently rule out every possible formulation of an idea—especially given known EVA limitations (ligature splitting, uncertain spaces, rare-glyph ambiguity) and the currently limited set of historical visual references—but it shows that these models cannot yet be demonstrated with the present evidence:

1. **Thermodynamic Distillation Simulator (`Digital Twin v2.0`):** Under the tested physics parameters (`1,000` within-folio permutations), random word orders achieved equal or higher yield and safety scores (`p = 0.52–0.72`). Thus, the current parameter set does not distinguish real word order from noise.
2. **`-ain` vs. `-aiin` pressure-state split:** When tested for next-word prediction within paragraphs, `-ain`, `-aiin`, and `-iin` behave nearly identically (`Z = +1.30`, `p = 0.090`). Whether they differ along other dimensions (such as folio context or non-EVA glyph grouping) remains unconfirmed.
3. **`-g` as a distillation/recipe-exclusive stop flag:** In raw `ZL3b-n.txt`, tokens ending in `-g` occur at highest density in `Astro/Zodiac` (`6.9 / 1,000`) and `Herbal` (`4.9 / 1,000`), rather than in `Recipes` (`1.3 / 1,000`), which does not support recipe exclusivity under current transcription rules.
4. **`oror` as a universal line terminator:** As an exact standalone token (with `,` spaces joined), `oror` appears `8` times (`4` line-final `50.0%`, `1` label, `1` line-initial on `f116v`, `2` mid-line). Longer `*oror*`-containing forms (`N = 24`) also appear more often at structural edges (`PF 20.8%`, `LL 20.8%`, `S 12.5%`, vs. `6.0%` `LL` for ordinary `-or` words), including paragraph endings (`okorory`, `okchedyoror`). However, `PF` occurrences largely reflect `p-/t-` initial positioning, `34%` (`11/32`) still occur mid-line, and the sample (`N = 32`) is small—so while `oror`-forms show a real boundary tendency, a universal shutdown-command role remains unconfirmed.
5. **Semantic glosses, `e/ee/eee` duration claims, and plant-as-piping interpretations:** While `e/ee/eee` counts show non-random local clustering (`Z = +13.37`) and historical distillation/herbal parallels remain worthwhile context to investigate further, these specific semantic readings and visual hardware mappings are not yet empirically demonstrated and are kept separate from the statistical baseline.

---

## 5. References
* **Beinecke Rare Book & Manuscript Library, Yale University.** *The Voynich Manuscript*, MS 408.
* **Bowern, Claire L., and Luke Lindemann.** “The Linguistics of the Voynich Manuscript.” *Annual Review of Linguistics* 7 (2021): 285–308.
* **Currier, Prescott H.** “Some Important New Statistical Findings.” *New Research on the Voynich Manuscript*, 1976.
* **Reddy, Sravana, and Kevin Knight.** “What We Know About the Voynich Manuscript.” *ACL LaTeCH*, 2011.
* **Stolfi, Jorge.** “A Grammar for Voynichese Words.” (Morphological slot model.)
* **Voynich Lucidity (2026).** *Cross-Boundary Mutual Information (CBMI) in the Voynich Manuscript*.
* **Zandbergen, René.** *The Voynich Manuscript: Text Analysis and Transliteration* (`ZL3b-n.txt`).
* **Zattera, Massimo.** “A New Approach to Voynich Manuscript Text Structure” (Slot-based templates, 2022).
* *A Glyph Is Not a Letter, a Token Is Not a Word, a Space Is Not a Space: What the Units of Voynichese Are Not* (arXiv preprint, August 2026).