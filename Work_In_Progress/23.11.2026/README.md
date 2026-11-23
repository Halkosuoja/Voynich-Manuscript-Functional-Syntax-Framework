[![DOI](https://zenodo.org)](https://doi.org)

# Voynich Manuscript Functional Syntax Framework (VFSF)
### Black-Box Structural, Boundary, and Cross-Corpus Analysis (Updated Baseline v4.0)
**Author:** Juho Olavi Laakso (Paimio, Finland)  
**Status:** Experimental Black-Box Research & Statistical Verification (*Work in Progress / Pre-release*)  
**Documentation License:** [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE)  
**Source Code License:** [MIT License](LICENSE-CODE)  
[Suomeksi](README_FI.md)

---

## 1. Project Purpose and Methodology

This project investigates the surface syntax and functional architecture of the Voynich Manuscript (MS Beinecke 408, Zandbergen–Landini transliteration `ZL3b-n.txt`: `5,376` lines, `38,216` raw tokens / `35,358` words after merging uncertain `,` spaces) using a **black-box** approach without prior assumptions about whether the text encodes a spoken natural language or a formal notation system.

The foundational positional word template is:

`[ PREFIX ] + [ LIGATURE / CORE + INFIX ] + [ SUFFIX ]`

### Statistical Controls
All sequence, boundary, and repetition tests are evaluated against **page-, paragraph-, and exact line-position-locked (`PF`, `LF`, `LM`, `LL`, `S`)** Monte Carlo permutations (`150–1,000` iterations, fixed seed `1337`), and benchmarked identically against natural languages, synthetic generators, and C source code.
* **Empirical Significance Bounds:** Computed via `p = (k + 1) / (N + 1)`, yielding minimum empirical bounds of `p < 0.005 (0/200)` and `p < 0.001 (0/1000)`, reported as sample bounds rather than continuous extrapolations.
* **Connection to 2026 Literature:** Independent 2026 studies (*"A Glyph Is Not a Letter, a Token Is Not a Word, a Space Is Not a Space"*, arXiv 2026; *Voynich Lucidity* CBMI, 2026) report the same ~0.2-bit boundary mutual information, uncertain space behavior, and Distance-2 collapse. This repository reproduces these metrics on `ZL3b-n.txt` and extends them with a unified connector matrix, scribe comparison (Scribes 1–5), an 11-corpus benchmark, and a falsified VFSF structural codebook (`vfsf_decoder.py`).

---

## 2. Core Empirical Findings (`ZL3b-n.txt`)

### 2.1 Uncertain Spaces (`,`) vs. Clear Spaces (`.`)
Uncertain/narrow spaces (`,`) in EVA account for a substantial fraction of specific boundary pairs:
* `o -> r`: `50.5%` caused by `,`
* `o -> l`: `44.8%` caused by `,` (`ol` appears `5,507` times joined vs. `119` across a clear space)
* `s -> a`: `38.4%` caused by `,` (`s+ai` appears `376` times joined vs. `127` separated)
* `r -> a`: `27.9%` caused by `,` (`r+ai` appears `425` times joined vs. `304` separated)
* Conversely, `y + qo` (`98.2%` separated, `3,382` vs. `61`), `n + ch` (`98.0%` separated, `1,294` vs. `26`), and `y + lk` (`96.5%` separated, `246` vs. `9`) act as near-absolute word boundaries.

### 2.2 Immediate 1-Step Boundary Coupling (Distance 1 vs. Distance 2)
When `,` spaces are merged and paragraph/line positions are locked, adjacent word boundaries exhibit strong Mutual Information (MI) that collapses almost completely when skipping one word:
* **Clear word spaces (`,` merged):** Distance 1 = `MI 0.16327 vs. 0.01438` (`11.35x`, net `+0.1489` bits, `Z = +154.65`) $\rightarrow$ Distance 2 = `0.02252 vs. 0.01568` (`1.44x`, net `+0.0068` bits, `Z = +6.52`). **`95.4%`** of the signal disappears immediately at Distance 2.
* **Even when frequent intraword pairs (`o+l`, `r+ai`, `s+ai`) are also merged:** Distance 1 remains virtually intact (`MI 0.14035 vs. 0.01474`, `9.52x`, net `+0.1256` bits), and **`95.1%`** still vanishes at Distance 2 (`1.38x`).

### 2.3 Universal Connector Matrix (`Herbal` vs. `Bio + Recipes`)
Observed-to-expected boundary ratios partition word initials into four functional classes across both `Herbal` (Currier A) and `Bio + Recipes` (Currier B):
* **`q-` (`qo-`, `13.1%` of corpus):** `72.6%` follows `-y` (`1.72x` overall; `1.53x` Herbal / `1.66x` Bio+Recipes), strongly rejecting other endings (`0.25x–0.62x`).
* **Gallows (`k, t, p, f`):** Favor preceding `-o` (`1.66x–3.81x`), `-y` (`1.15x–1.56x`), and `-l` (`2.76x / 1.91x` in B), while rejecting `-s`, `-n`, and `-r` (`0.12x–0.52x`).
* **`a-` (`aiin, ain, al, ar...`):** Strongly favors `-s` (`4.68x` overall; `4.60x` Herbal / `6.28x` Bio+Recipes) and `-r` (`2.99x`), while rejecting `-y` (`0.20x`).
* **`c-`, `o-`, `s-`:** Moderately favor `-n` (`1.23x–1.39x`), `-r`, and `-l`, appearing less frequently after `-y` (`0.73x–0.86x`).

### 2.4 Labels (`@L`) vs. Running Text (`@P`) and Scribal Consistency
* **`qo-` disappears from labels:** `qo-` accounts for **12.1%** of running text (`@P`), but occurs only **once (0.2%)** in labels (`@L`, `N = 440`) and **2.7%** in circular diagrams (`@R/@C`), confirming `qo-` is strictly an intratextual sequence connector.
* **`ot-` and `ok-` dominate labels:** Together, `ot-` (`19.8%`) and `ok-` (`16.6%`) cover **36.4%** of all label tokens (`~6%` in `@P`), and **82.9%** (`319 / 385`) of unique label words never appear in running text.
* **Universal across Scribes 1–5:** The `y -> qo` boundary law holds across all five scribes identified by Lisa Fagin Davis (2020) (Scribe 1: `54.3%`, Scribe 2: `87.5%`, Scribe 3: `64.6%`, Scribe 4: `73.4%`, Scribe 5: `58.7%`).
* **Lexical Compression & Alternating Repetition (`A - X - A`):** Stripping affixes reduces `7,954` surface forms to `2,460` cores; the **Top-9 cores cover 50%** and the **Top-46 cores cover 80%** of all words. Unlike natural prose ($Z < 0$), Voynich exhibits positive alternating repetition $A - X - A$ (`0.78%`, `Z = +4.82`; `88.0%` within the same line).

---

## 3. Cross-Corpus Benchmark (11 Texts: Natural Languages, Generators & C Code)

All 11 corpora were evaluated using the identical language-agnostic metric (`universal_syntax_bench.py`) with paragraph- and line-position locking (`150` iterations, seed `1337`):

| Corpus | Words | Distance 1 (Net MI & Ratio) | Distance 2 (Net MI & Ratio) | Retention (D2 / D1) | Directional Asymmetry | Top Boundary-Coupled Initial (% Text) |
| :--- | :---: | :--- | :--- | :---: | :---: | :--- |
| **`control_slot.txt`** (Slot Gen.) | 35,002 | `-0.00001` (`0.99x`) | `+0.00032` (`1.34x`) | – | `0.94x` (`Z=-0.36`) | `'ck-'` (`+3.6%`, *noise*) |
| **`control_selfcite.txt`** (1-word copy) | 35,000 | `+0.00018` (`1.04x`) | `+0.00075` (`1.15x`) | – | `0.97x` (`Z=-0.21`) | `'sh-'` (`+1.7%`, *noise*) |
| **`plinius_ii.txt`** (Class. Latin) | 17,452 | `+0.0225` (`2.46x`) | `+0.0004` (`1.02x`) | ~1.6% | `3.04x` (`Z=+18.21`) | `'es-'` (`1.6%`, `+12.3%`) |
| **`latin_abbrev.txt`** (Abbrev. Latin) | 17,453 | `+0.0174` (`2.12x`) | `+0.0002` (`1.02x`) | ~1.4% | `2.90x` (`Z=+16.04`) | `'es-'` (`1.6%`, `+12.1%`) |
| **`Herbarum.txt`** (Herbal Latin) | 2,434 | `+0.2129` (`3.33x`) | `+0.0313` (`1.28x`) | **14.7%** | `1.68x` (`Z=+4.38`) | `'ui-'` (`2.0%`, `+32.2%`) |
| **`Matteus1548.txt`** (1548 Finnish) | 25,170 | `+0.0344` (`2.64x`) | `+0.0071` (`1.35x`) | **20.5%** | `5.96x` (`Z=+51.20`) | `'et-'` (`1.9%`, `+17.4%`) |
| **`kalevalaTesti.txt`** (Finnish) | 14,126 | `+0.0617` (`4.34x`) | `+0.0137` (`1.62x`) | **22.2%** | `2.31x` (`Z=+19.71`) | `'vä-'` (`1.6%`, `+35.7%`) |
| **`hamlet.txt`** (English Drama) | 32,878 | `+0.0668` (`5.64x`) | `+0.0217` (`2.32x`) | **32.5%** | `4.73x` (`Z=+83.10`) | `'lo-'` (`1.3%`, `+38.1%`) |
| **`LinuxTesti.txt`** (English Manual) | 5,774 | `+0.1429` (`2.70x`) | `+0.0548` (`1.65x`) | **38.3%** | `5.57x` (`Z=+33.18`) | `'ca-'` (`1.3%`, `+47.8%`) |
| **`sqlite3_35k.txt`** (Cleaned C Code) | 32,278 | `+0.2697` (`15.91x`) | `+0.2380` (`10.93x`) | **88.3%** | `4.45x` (`Z=+258.67`) | `'pr-'` (`4.3%`, `+56.8%`) |
| **`ZL3b-n.txt` (Voynich)** | 35,358 | **`+0.1489` (`11.35x`)** | **`+0.0068` (`1.44x`)** | **4.6%** | `3.80x` (`Z=+49.94`) | **`'qo-'` (`13.1%`, `+30.3%`)** |
---

## 4. Unverified and Falsified Hypotheses Excluded from Baseline (Methodological QA)

The following hypotheses from earlier iterations (`v1.5–v3.8.2`, `Digital Twin v2.0`) failed statistical null tests on `ZL3b-n.txt` and are **excluded from the verified empirical baseline**:

1. **Distillation Simulator (`Digital Twin v2.0`):** Under tested physical parameters (`1,000` shuffles), randomized word order achieved equal or higher yield and safety than the authentic text (`p = 0.52–0.72`).
2. **Interpreting `-ain` vs. `-aiin` specifically as pressure states:** Statistical tests (`Test A`, `F5`, `F6`) confirm `i` and `ii` forms are paradigmatically substitutable (`r = 0.90–0.94`) and invariant across paragraph lines (`63.3% -> 63.5%`, `p = 0.9301`), acting as a static section-level register constant (`Herbal/Pharma` `3.4:1` vs. `Bio` `0.8:1`), while their specific semantic interpretation as pressure states remains unverified.
3. **`-g` exclusively marking distillation/recipe pages:** In `ZL3b-n.txt`, `-g`-final words are densest in `Astro/Zodiac` (`6.9 / 1,000`) and `Herbal` (`4.9 / 1,000`), not `Recipes` (`1.3 / 1,000`).
4. **`oror` as a universal line terminator:** Standalone `oror` occurs `8` times (`50.0%` line-final) and `*oror*` forms (`N = 24`) show edge enrichment (`PF 20.8%`, `LL 20.8%`), but `34%` occur mid-line and sample size is too small to confirm a universal stop command.
5. **Individual word translations and interpreting botanical drawings as plumbing:** While the structural role of `e/ee/eee` lengths as a syntax-independent (`F1`: MI retention `104.3%`) dynamic duration/intensity gradient across paragraphs is now statistically verified (`F6`: `25.9% -> 34.4%`, `p < 0.0010`), individual semantic translations and interpreting plant or vessel illustrations as distillation apparatus remain unverified.
6. **Page-specific plant proper nouns (`Herbal` ↔ `Pharma` pairs & `@Lc/@Lf` labels):** Rare-word Jaccard similarity between botanically matched `Herbal–Pharma` page pairs (`N = 14`) does not exceed chance (`0.0083` vs. `0.0150`, `p = 0.9590`), and Pharma jar/root labels (`@Lc/@Lf`) do not repeat in the immediately following `@P0` paragraph above chance (`1.36%`, `p = 0.9021`).
7. **`daiin / dain` as uniform sentence delimiters:** Inter-token distances (`mean 13.07 words`, `N = 465`) exhibit higher relative dispersion than randomized word order (`CV = 1.389` vs. `1.212`, `p = 0.9820`), indicating clustered parallelisms rather than regular punctuation.
8. **Marginal star shapes encoding paragraph vocabulary (`Quire 20`, `f103r–f116r`):** Across `322` star-marked paragraphs (`9,523` words, `1,000` permutations), visual star attributes show no significant effect on lexical profiles: dark vs. light (`p = 0.1898`), dotted vs. plain (`p = 0.2178`), or point count `7` vs. `8` (`p = 0.2787`).
9. **Long-range start-to-end paragraph coupling (`PAR_FIRST` → `PAR_LAST`):** Stratified permutation tests (`N = 668` multi-line paragraphs, `1,000` shuffles) show paragraph opening type does not predict paragraph-final word (`p = 0.3337`) or final-line dominant suffix (`p = 0.1738`).

---

## 5. Reverse-Decoding Model (VFSF v4.0), Falsification Suite (`F1–F7`), and Structural Codebook

Based on section-level analyses (`Herbal`, `Zodiac`, `Pharma`, `Bio`, `Quire 20`), paradigmatic substitutability (`Test A`), and seven null-tested falsification experiments (`F1–F7`), the Voynich Manuscript operates as a **modular, state-and-operator formal notation system (ideographic/structural code)** describing cyclical and multi-stage processes.

### 5.1 Summary of Falsification & Verification Tests (`F1–F7`)

| Test | Hypothesis / Mechanism | Empirical Result (`ZL3b-n.txt`) | Statistical Outcome | Conclusion |
| :--- | :--- | :--- | :--- | :--- |
| **Test A** | Paradigmatic substitutability (`w1 ___ w2`) | `daiin=dain` (`r=0.938`), `chedy=shedy` (`r=0.918`), `qokeedy=qokedy` (`r=0.915`) | Cosine similarity `0.85–0.94` | EVA doublets (`ii/i`, `ee/e`, `ch/sh`) occupy identical syntactic slots. |
| **Test B & C1** | Zodiac rings (`@Lz` vs. `@Cc`, `f70v2–f73v`) | `@Lz` flips at `f72v3`: `ot+a` (`79.1%`) → `ok+e` (`53.5%`); `@Cc` stays invariant | `@Lz`: **`p < 0.001`**; `@Cc`: `p = 0.21–0.93` | `@Cc` is a constant operation frame; `@Lz` tags encode phase/state shift. Inner vs. outer rings are equivalent (`p = 0.289`). |
| **Test D & F2** | Pharma labels (`@Lc` vs. `@Lf` vs. `@P0`) | `@L` tokens repeat in underlying `@P0` at `1.36%`; intra-page `@Lc-@Lf` diff `+0.45` chars | Test D: `p = 0.902`; F2: `p = 0.206` | **Falsified:** Labels are neither text proper nouns nor a stripping hierarchy, but an independent diagram index. |
| **Test F1** | Reduced state machine (`ii=i`, `ee=e`, `ch=sh`) | Raw `MI 0.16812` → Normalized `MI 0.17541` (`104.3%`), vocab `-16.7%` | MI retention **`104.3%`** | Core atoms govern syntax; merging doublets removes noise without information loss. |
| **Test F3** | Content-core directional order (`PF` vs. `LM`) | Non-Top-46 content cores enrich at paragraph opening (`PF/LM = 2.11x`) | **`p < 0.0020`** (`0/500`) | Paragraphs follow an algorithmic order: target/input at opening (`PF`), standard operations mid-line (`LM`). |
| **Test F4** | Currier A → Currier B cross-prediction | Currier A boundary transitions predict Currier B (`-5.47868` bits/boundary) | **`p < 0.0050`** (`0/200`) | Currier A and B are two vocalic/functional registers of a single formal system. |
| **Test F5 & F6** | Length parameters (`e/ee/eee` vs. `i/ii/iii`) | `ee/(e+ee)` rises `Line 1: 25.9%` → `Mid: 34.4%`; `ii/(i+ii)` stays constant (`63.3–65.0%`) | `ee`: **`p < 0.0010`**; `ii`: `p = 0.9301` | **`ee/eee` = dynamic duration/intensity** within paragraphs; **`ii/i` = static section register** (`Herbal` `3.4:1` vs. `Bio` `0.8:1`). |
| **Test F7** | Extended atoms (`BRIDGED`, `L_PREFIX`, `SOLO_KT`, `PARTICLES`) | `BRIDGED` (`Herbal` `9.1%` → `Stars` `3.4%`); `L_PREFIX` (`Herbal` `0.4%` → `Stars` `5.1%`); `SOLO_KT` (`LL/LM = 0.39x`) | Section & line-position specialization | Bridged gallows and `l-` prefixes are inverse section registers; `oke/ote` is strictly line-internal. |

### 5.2 Extended VFSF Structural Codebook (`vfsf_decoder.py`)

* **Prefix Operators (Syntactic Position & Coupling):**
  * `p- / t- / k- / f-` (`INIT / RULE`): Paragraph-opening operator (`PF`, `76–80%` in Bio/Quire 20). Initiates a rule or process unit.
  * `qo-` (`FLOW`): Strictly intratextual sequence connector (`12–25%` in `@P`, `0.2%` in `@L`), bound to preceding `-y` (`72.6%`).
  * `ok- / ot-` (`MODE2 / MODE1`): State/phase selector (`36–56%` in `@L`, `12–21%` in `@P`). Switches from `MODE1(ot)` to `MODE2(ok)` at the midpoint of the Zodiac sequence (`p < 0.001`).
  * `d- / s- / y-` (`SHIFT`): Line-initial framing operator (`LF`), marking sub-steps or cycle transitions.
  * `l-` (`MOD(l)`): Line-internal modifier (`0.4%` Herbal → `5.1%` Stars/Quire 20).
* **Core Modules & Orthogonal Parameters:**
  * `ch/sh + e` (`PROC`): Active process/action core (`Bio` `34.6%`, `Quire 20` `26.4%`).
  * `ch/sh + o` (`OBJ`): Object/structure core (`Herbal A` `22.1%` vs. `Bio B` `3.1%`).
  * `ckh / cth / cph / cfh` (`COMP_STRUCT`): Bridged gallows ligatures (`Herbal` `9.1%` → `Stars` `3.4%`).
  * `e -> ee -> eee` (`DUR:1x / 2x / 3x`): Dynamic duration/intensity scale (`p < 0.0010`), rising from Line 1 (`25.9%`) to middle lines (`34.4%`).
  * `i -> ii -> iii` (`MED:1 / 2 / 3`): Static section/medium register (`p = 0.9301` within paragraphs).
  * `daiin / dain` (`REF`): Baseline reference state and primary anchor in `A - X - A` comparison loops (`11.6%` of all alternating repetitions).
  * `ol / or / al / ar / qol` (`BRIDGE`): Short line-internal relational particles (`LL/LM = 0.55x`).
* **Suffixes (State Values & Closure):**
  * `-dy / -edy / -y` (`STATE_ACT`): Marks active state and enables `qo-` chaining.
  * `-al / -ol` (`PARAM_A`) vs. `-ar / -or` (`PARAM_B`): Complementary, paradigmatically substitutable (`r = 0.86`) state parameters dominating `@L` labels (`55–79%`).
  * `-am / -om` (`END_LOCK`): Paragraph-final closure suffix (`PAR_LAST`, `31.2%` in Quire 20).

### 5.3 Running the Structural Decoder (`vfsf_decoder.py`)

Place `ZL3b-n.txt` in the repository root and run:

```bash
# Decode a specific folio (automatically saves decoded_f75r.txt)
python vfsf_decoder.py f75r

# Or launch interactive mode
python vfsf_decoder.py
```

---

## 6. References
* **Beinecke Rare Book & Manuscript Library, Yale University.** *The Voynich Manuscript*, MS 408.
* **Bowern, Claire L., and Luke Lindemann.** “The Linguistics of the Voynich Manuscript.” *Annual Review of Linguistics* 7 (2021): 285–308.
* **Currier, Prescott H.** “Some Important New Statistical Findings.” *New Research on the Voynich Manuscript*, 1976.
* **Davis, Lisa Fagin.** “How Many Glyphs and How Many Scribes? Digital Paleography and the Voynich Manuscript.” *Manuscript Studies* 5, no. 1 (2020): 164–180.
* **Rozanova, Julia, and Artem Temerev.** “A Glyph Is Not a Letter, a Token Is Not a Word, a Space Is Not a Space: What the Units of Voynichese Are Not.” *arXiv:2608.17096* (August 2026).
* **Stolfi, Jorge.** “A Grammar for Voynichese Words.” (Morphological slot model.)
* **Zandbergen, René.** *The Voynich Manuscript: Text Analysis and Transliteration* (`ZL3b-n.txt`).
* **Zattera, Massimo.** “A New Approach to Voynich Manuscript Text Structure” (2022).
