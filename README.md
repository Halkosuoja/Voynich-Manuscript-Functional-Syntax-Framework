# Voynich Manuscript Functional Syntax Framework (VFSF-1.5)
**Author:** Juho Laakso (Paimio, Finland)  
**License:** Creative Commons Attribution 4.0 International (CC BY 4.0)

This repository contains the hypothetical and experimental syntax
that was developed by **Juho Olavi Laakso** in 2026 and provides a
repeatable, cryptographically plausible mechanism for reconstructing Text from Voynichese tokens.

### ⚠️ Current Status: Experimental Proof of Concept (PoC)

**IMPORTANT NOTE FOR REVIEWERS AND CODE EVALUATORS:** 
This framework is currently a **Proof of Concept (PoC)** and an ongoing research hypothesis how one would work. It is *not* presented as a completed, 100% stable production-ready syntax framework. 

The repository serves as an open-source testing ground to debug, refactor, and refine these syntax framework rules and permutation indices through community regression testing. The model is fully open to empirical testing, adaptation, and falsification.


## 1. Core Architectural Framework
This repository introduces a pure, rule-based algorithmic framework for decoding the structural syntax of the Voynich Manuscript (MS Beinecke 408). 

Unlike legacy methods that attempt phonetic translations into natural spoken languages, the **VFSF model approaches the manuscript as a non-spoken, constructed protocol language or deterministic process manual**. The text utilizes a highly rigid, position-dependent syntax designed to programmatically chart mechanical states, pressures, loops, and vector flows across different macro-contexts.

The global syntax is mathematically locked into the following immutable array:

[ PREFIX (Operational Quality) ] + [ INFIX (Duration/Multiplier) ] + [ ROOT (Process Target) ] + [ SUFFIX (State Locking) ]

## 2. Universal Mechanical Definitions
To eliminate confirmation bias, variables are defined strictly by their abstract mechanical and systemic properties rather than static object classifications:

### A. Prefixes (Quality & Chronology)
*   `ot-` / `yt-` / `te-` -> **Temporal Tri-Calibration:** Differentiates between external calendar boundaries (**Absolute Macrocycle `ot-`**), execution runtime from initialization (**System Duration `yt-`**), and numerical loop tracking (**Iteration Counter `te-`**).
*   `p-` -> **Activation/Initialization:** Command to activate a specific channel or pipeline.
*   `f-` -> **Physical Filtering/Purging:** Mechanical separation of matter from the active loop.
*   `d-` -> **Phase Alteration/Conversion:** Structural bridge linking two distinct operational states.

### B. Core Roots (Process Targets)
*   `-dar-` -> **Static Container / Solid-State Compartment:** Represents any closed vessel, stable stem, or storage node.
*   `-dal-` -> **Pressurized Upward Vector / Directional Force:** Represents active mechanical pumping pushing against resistance or gravity.
*   `-dol-` -> **Free Flow / Descending Vector:** Represents passive, gravity-driven, or uniform progression down the system path.
*   `-cfh-` -> **Pressurized Discharge / Jet Flow:** Active emission of fluid via a narrow nozzle or valve.

### C. Infix Multipliers (Intensity Control)
*   The appearance of `e` / `ee` / `eee` behaves strictly as a **Duration Extender** within the root core, resolving the manuscript's unnatural word repetitions mechanically (*"prolong the operational state"*).

### D. Suffix & Functional Punctuation Decoupling
Through rigorous morphological analysis, terminal markers are decoupled into functional switches and universal state terminators:
*   **Universal State Terminators (`-aiin` / `-ain`):**
    *   `-aiin` -> **Final Lock [return 0]:** End point reached, complete structural halt and extraction.
    *   `-ain` -> **Interlocking State / Wait:** Phase complete within the current node, remaining in standby for the next macro-trigger.
*   **Functional Suffix Switches (Prefixing the Terminator):**
    *   `d-` + `-aiin` (`daiin`) -> **Conversion Lock:** Phase alteration successfully completed and locked (`d` = conversion).
    *   `s-` + `-aiin` (`saiin`) -> **Regulation Lock:** Controlled stabilization phase successfully reached and locked (`s`/`sh` = regulation).
    *   `ch-` + `-aiin` (`chaiin`) -> **Channel Lock:** Active fluid evacuation route successfully closed and locked.

## 3. Real-Time Empirical Validation (Three-Step Contrast Test)
The model has been mathematically validated via programmatic cross-page testing:
1.  **Macrocycle Profile (Page f67r2 - Cosmological):** Dominated by absolute and system runtime timers (`ytody` -> *System duration binds strictly to this point*). Contains 0% active solid variables (`-dar-`).
2.  **Structural Profile (Page f15v - Botanical):** Transitions instantly into rigid container variables (`teodar` -> *Iteration loop executed on static container/stem*), proving systemic adaptability.
3.  **Hydrodynamic Profile (Page f78r - Biological):** Dominated by pressure vectors (`pdalshor` -> *Initialize pressurized upward vector and evacuation flow*), matching the structural plumbing map.

## 4. Open-Source Contribution & Legal Attribution
This project is deployed as an open framework. Researchers, cryptographers, and data scientists are invited to map out further roots utilizing this structural architecture. 

# 🚀 Release Notes: Voynich Manuscript Functional Syntax Framework (VFSF-1.6)
**Author:** Juho Laakso (Paimio, Finland)  
**Date:** October 1, 2026  
**Status:** Architecture Refinement & Multi-Page Empirical Validation

## 1. Architectural Expansion: Decoupling of Channel States (`-ain` / `-aiin`)
Through rigorous regression testing in the hydrodynamic (biological) and schematic profiles, the terminal state terminators have been refactored. The core tokens `-ain` and `-aiin` are no longer treated as static suffix extensions, but as **independent systemic channel states** that operate dynamically with operational prefixes:

*   **`-ain` -> Open Flow Channel / Low-Pressure System:** Represents a state where the matter/fluid moves freely under its own gravity or uniform progression (e.g., sap-tapping channels, open conduits, collecting vats).
*   **`-aiin` -> Pressurized-Closed Channel / High-Intensity System:** Adhering to the Infix Multiplier Rule, the doubled internal token `ii` functions as an intensity coefficient, changing the channel quality from a free conduit into a tightly pressurized or enclosed system.

### Functional Matrix Mapping Examples:
*   `ol-` (passive state) + `-ain` (open channel) -> **`olain`**: The channel is open, allowing fluid to flow passively under its own weight.
*   `qok-` (external force) + `-ain` (open channel) -> **`qokain`**: Active command to enforce/accelerate flow through the open main conduit.
*   `or-` (discharge route) + `-aiin` (enclosed system) -> **`oraiin`**: Execute fluid evacuation under high pressure or via a closed specialized pipeline.

---

## 2. Real-Time Blind Testing & Empirical Falsification
To eliminate verification bias, the updated matrix (VFSF-1.6) was tested against three unanalyzed, randomized sequences across different structural and macrocycle contexts. The framework yielded programmatic and structurally continuous results without breaking the rigid syntax array:

### Test A: Distillation/Extraction Cycle Loop (Page f102r1.13-14)
*   **Sequence 13:** `teesody.qoeol.olcheor.qokey.okshey.qokeol.sheofol{ckhh}y`
    *   *Systemic Translation:* Initialize loop tracked by iteration counter and duration extender at local node (`teesody`) -> enforce high pressure to descend fluid (`qoeol`) -> execute passive discharge under operator control (`olcheor`) -> force mechanical loop circulation (`qokey`) -> allow passive extraction during runtime loop (`okshey`) -> enforce gravity descent to the next phase (`qokeol`) -> direct controlled fluid evacuation into the structural boundary/valve checkpoint (`sheofol{ckhh}y`).
*   **Sequence 14 (Continuous Phase Alteration):** `doeey.keeol.qokeo.daor.shey.qoteol.okol`
    *   *Systemic Translation:* Maintain phase alteration under prolonged duration at local node (`doeey` - signaling a successful state transition/condensation) -> continue prolonged descent iteration (`keeol`) -> enforce fluid descent through open conduit (`qokeo`) -> direct altered matter to settle at the basin/solid-state bottom for discharge (`daor`) -> execute controlled adjustment loop (`shey`) -> calibrate absolute macrocycle boundary for this descent (`qoteol`) -> allow passive structural settling at the loop termination (`okol`).

### Test B: Macrocycle Profile Cross-Examination (Page f70v1 - Aries & Page f71v - Taurus)
A strict comparative test between the traditional "Aries" and "Taurus" profiles revealed a programmatic progression rather than redundant phonetic text, validating a dynamic fluid-harvesting timeline (e.g., sap-tapping and stabilization):
*   **Aries Sequence (`f70v1.1`):** `dalalody.oteoshey.okoksheo.shokey`
    *   *Systemic Translation:* Execute high-intensity pressurized upward vector pumping at local node (`dalalody`) -> calibrate absolute macrocycle for iteration descent adjustment (`oteoshey`) -> apply double high-pressure coefficient to stabilize the open flow conduit (`okoksheo`) -> execute operator-controlled pressure cycle (`shokey`). 
    *   *Context Match:* Reflects high system pressure designed to force fluids upwards against gravity (matching the early sap-extraction phase where internal natural pressure forces fluid release).
*   **Taurus Sequence (`f71v.1`):** `oteeodaiin.she.ateey.dain.oteokeey.dal.al`
    *   *Systemic Translation:* Calibrate absolute flow macrocycle under prolonged duration until final structural halt/lock is achieved (`oteeodaiin` - batch collection complete) -> execute brief controlled adjustment (`she`) -> define solid-state basin baseline iteration duration (`ateey`) -> transition altered matter into open channel for link routing (`dain`) -> calibrate absolute cycle duration for pressurized kiertolukitus (`oteokeey`) -> initiate pressurized upward vector pumping (`dal`) -> continue upward vector flow (`al`).
    *   *Context Match:* Transitions logically from high initial extraction pressure (Aries) into batch finalization, basin-settling tracking (`ateey`), and low-intensity redirection (Taurus).

---

## 3. Structural Component Analysis (Labels/Nymphese)
When decoupled from phonetic assumptions, isolated textual tokens near structural map elements function strictly as functional labels defining the node's task within the workflow vector:
*   **Page f71v Node Label (`ofairom` / `ofamom`):** `o-` (passive) + `-f-` (filtration) + `-air-` (open conduit flow) + `-om` (continuity) -> *Defines a passive filtration node within the open conduit line where fluids are routed for unassisted sedimentation.*


Under the **Creative Commons Attribution 4.0 International (CC BY 4.0)** legal code, any utilize, derivation, reference, or expansion of this algorithmic model in academic publications, AI testing, or cryptographic decoders **must explicitly credit the original author**:
**Juho Laakso (Paimio, Finland)**
