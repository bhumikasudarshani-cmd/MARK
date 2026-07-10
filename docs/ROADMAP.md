# Bharati Braille Digital Toolkit — Roadmap (Revised)

**Type:** Solo CS Engineering Capstone
**Duration:** ~16 weeks (revised up from 12–14 after risk review — see Changelog)
**Core deliverable:** A working text-to-Bharati-Braille converter (Hindi/Devanagari), targeting the **ratified Bharati Braille 2.0 standard**.

---

## Changelog from v1

This revision responds to a structured critique of the original plan. Key changes:
- Added an explicit **go/no-go checkpoint** at the end of Week 1 (previously: risks were listed but had no decision trigger)
- Extended segmentation (2→3 weeks) and rule engine (3→5 weeks) phases; compressed the web interface (1 week → 2-3 days) to absorb the extra time
- Added an explicit **test-set sourcing task in Week 1-2** (previously assumed available in Week 9 with no sourcing plan)
- Added an explicit **version decision** (Bharati Braille 2.0 vs. draft 2.1) as a Week 1 deliverable
- Split **numbers/punctuation** into its own sub-milestone instead of one bullet buried in the rule engine week
- Made the **validation circularity risk** explicit and addressed it with a two-tier ground-truth strategy
- Protected the **documentation/report week** from schedule slippage by treating it as non-negotiable, separate from buffer

---

## 1. Project Objective

Build a tool that converts digital Hindi (Devanagari) text into correct **Bharati Braille**, following the officially ratified **Bharati Braille 2.0** standard (NIEPVD, released January 4, 2025) — not a naive character-by-character substitution.

**Note on versioning (locked in Week 1):** NIEPVD has a **draft 2.1** revision in public consultation as of early 2026. This project targets **2.0** (the ratified standard) as its baseline. Any 2.1 changes are explicitly out of scope and noted as a "future revision" risk in the final report — don't chase a moving draft standard mid-build.

---

## 2. Scope Decisions (Week 1 deliverables — not optional)

| Decision | Default | Status |
|---|---|---|
| Which language? | Hindi (Devanagari) | Locked |
| Which standard version? | **Bharati Braille 2.0** (ratified Jan 2025), not draft 2.1 | Locked — document why in report |
| Input method | Typed/pasted Unicode text | OCR is stretch goal |
| Output format | Unicode Braille (screen) + `.brf` file (embosser) | Locked |
| Contractions (Grade 2-style) | Out of scope for MVP | Documented limitation |
| Direction | One-way (text → Braille) | Reverse is stretch goal |
| **Virama/halant representation** | Has its own Braille cell (dot 4), inserted before the following consonant in a conjunct — NOT a silent/unprintable marker (corrected from v1) | Locked |

### Week 1 Go/No-Go Checkpoint

By the end of Week 1, you must be able to answer **yes** to all of the following, or the scope shrinks explicitly (documented, not silently absorbed into schedule slip):

1. Can I obtain the official Bharati Braille 2.0 standard document with its Unicode mapping chart?
2. Does it cover, unambiguously, all Hindi consonants, independent vowels, matras, common conjuncts, numbers, and core punctuation?
3. Are there worked examples (word/sentence-level transcriptions) in the source document I can use as semi-independent test data?

If any answer is "no" for a specific subset (e.g., rare conjuncts are underdocumented), **explicitly narrow scope** to what is well-documented, and list the excluded cases as a known limitation — don't guess/invent rules for gaps in the standard.

---

## 3. Required Background Knowledge (Week 1–2)

1. **Get the official source.** Locate NIEPVD's "Standard Bharati Braille Codes with Unicode Mapping Chart" (Jan 2025) — this is a real, publicly available government document, not something you have to reverse-engineer from scratch.
2. **Devanagari Unicode structure** — consonants, independent vowels, matras, virama/halant (U+0900–U+097F block), and how conjuncts are formed.
3. **6-dot Braille cell representation** — Unicode Braille Patterns block (U+2800–U+28FF).
4. **Test-data sourcing (new — was missing in v1):** identify and extract worked transcription examples from the official standard itself. These are your first tier of ground truth — written by NIEPVD, not derived from your own code, so checking against them isn't circular in the way testing only against your own rule transcription would be. Second tier (start reaching out now, not in Week 9): contact a Braille resource center, special-education teacher, or NIEPVD directly for informal review of sample output later in the project — this has long lead time, so the ask goes out early even if the actual review happens much later.

**Deliverable:** A written rulebook (your own reference table) covering consonants, vowels, matras, virama/conjunct rules, numbers, and punctuation, sourced from the 2.0 standard, plus a small set of official worked examples set aside untouched as test data.

---

## 4. System Architecture

```
Input text (Devanagari, Unicode)
        │
        ▼
┌─────────────────────────┐
│ Text Normalizer          │  → clean input, isolate numbers/punctuation
│                          │     for special indicator handling
└─────────────────────────┘
        │
        ▼
┌─────────────────────────┐
│ Syllable/Grapheme        │  → split into orthographic units; handle
│ Segmenter                │     stacked conjuncts (multiple viramas),
│                          │     vowel vs. matra disambiguation via
│                          │     contextual lookahead/lookbehind
└─────────────────────────┘
        │
        ▼
┌─────────────────────────┐
│ Rule Engine              │  → map each unit to Bharati Braille cell(s);
│ (core, budget 5 weeks)   │     numbers/punctuation as its own sub-phase
└─────────────────────────┘
        │
        ▼
┌─────────────────────────┐
│ Output Formatter         │  → Unicode Braille + .brf file
└─────────────────────────┘
```

---

## 5. Revised Week-by-Week Plan

### Week 1: Source Acquisition, Version Lock, Go/No-Go
- Obtain the official Bharati Braille 2.0 standard document
- Lock version decision (2.0, not draft 2.1) — document rationale
- Confirm coverage of Hindi consonants/vowels/matras/conjuncts/numbers/punctuation
- Extract a set of official worked examples to set aside as test data
- **Checkpoint:** go/no-go decision — narrow scope now if documentation gaps exist, don't defer

### Week 2: Rulebook Documentation
- Build your own reference table (consonant/vowel/matra/conjunct/number/punctuation → Braille cell), sourced directly from the 2.0 standard
- Explicitly document the virama/halant rule (dot 4, inserted before the following consonant)
- Set up dev environment

### Weeks 3–5: Normalizer + Segmenter (extended from 2→3 weeks)
- Normalizer: numbers/punctuation isolation, whitespace handling
- Segmenter: handle **stacked conjuncts** (e.g., multi-consonant clusters with sequential viramas), and **vowel/matra ambiguity** using contextual lookahead/lookbehind — this is genuinely hard, budget real time here, don't assume regex alone solves it
- Build a dedicated test set of tricky segmentation cases *before* moving to the rule engine, so you know your segmenter is solid before building on top of it

### Weeks 6–10: Rule Engine (extended from 3→5 weeks)
- Weeks 6–8: Core mapping — consonants, vowels, matras, conjuncts
- Week 9: **Numbers and punctuation as their own explicit sub-milestone** (not squeezed into the same week as conjunct handling) — number-indicator prefixing and context-dependent punctuation rules are a nontrivial rule set on their own
- Week 10: Integration — full pipeline running end-to-end on real sentences

### Week 11: Output Formatting
- Unicode Braille rendering + `.brf` file export

### Week 12: Testing & Validation (two-tier ground truth)
- **Tier 1:** Validate against the official standard's own worked examples (semi-independent — NIEPVD-authored, not self-derived)
- **Tier 2:** Pursue external review (Braille resource center, special-ed teacher, NIEPVD contact) — the ask should have gone out back in Week 1-2; this week is when you'd ideally get a response, though it may land later
- Report accuracy with an honest breakdown by rule category (which conjunct types failed, etc.)

### Week 13: Minimal Web Interface (compressed from 1 week → 2-3 days)
- Bare-bones paste-text-get-Braille form; don't over-invest here now that the hard phases have more room

### Week 14: Documentation & Report (protected — not buffer)
- Rulebook, architecture, test results, honest limitations section (version scope, uncovered conjuncts, contractions out of scope, etc.)
- Prepare demo examples covering: simple word, conjunct-heavy word, numbers, full sentence

### Weeks 15–16: Buffer / Stretch Goals
- First priority if time allows: closing any gaps flagged during Tier 2 external review
- Second priority: OCR front-end, reverse conversion, additional language

---

## 6. Tech Stack

| Component | Tool | Why |
|---|---|---|
| Core logic | Python | Strong Unicode handling |
| Segmentation | Custom logic with lookahead/lookbehind (not naive regex) | Conjunct stacking and matra ambiguity need context, not pattern matching alone |
| Web interface | Flask + basic HTML/JS | Lightweight, matches backend |
| OCR (stretch) | Tesseract with Devanagari (`hin`) data | Free, offline-capable |
| Testing | `pytest` | Standard, demonstrable coverage |

---

## 7. Validation Strategy (revised — addresses circularity risk)

**The problem with v1:** if your only ground truth is your own transcription of the same standard you coded against, "testing against known-correct output" partly just re-checks your own reading comprehension, not independent correctness.

**Two-tier fix:**
1. **Tier 1 (available from Week 1):** Worked examples embedded in the official 2.0 standard document itself — authored by NIEPVD, not you. Better than nothing, still somewhat close to the source you coded from.
2. **Tier 2 (start the ask in Week 1-2, land the response whenever it comes):** A human Braille reader, special-education teacher, or NIEPVD contact reviewing actual output. This is the only tier that meaningfully escapes circularity, and it has a long lead time — which is exactly why the outreach can't wait until Week 9.

Report both tiers separately in your results — don't blend them into one accuracy number, since they carry different evidentiary weight.

---

## 8. Risks & Mitigations (updated)

| Risk | Mitigation |
|---|---|
| Standard documentation has gaps/contradictions for some cases | Week 1 go/no-go checkpoint — narrow scope explicitly rather than guess |
| Segmentation ambiguity (stacked conjuncts, vowel/matra) worse than expected | Already budgeted an extra week (3 total); if still insufficient, this is the first place to pull from Week 15-16 buffer |
| Rule engine overruns 5 weeks | Numbers/punctuation sub-milestone can be descoped to "common cases only" if needed, documented as a limitation |
| Tier 2 external review doesn't materialize in time | Tier 1 (official worked examples) still gives a defensible, non-zero validation story on its own |
| Draft 2.1 gets ratified mid-project, creating pressure to "keep up" | Explicitly out of scope by design (see Section 1) — note it as future work, don't chase it |

---

## 9. What Makes This a Strong Submission

- Explicit version targeting against a real, named, government-ratified standard (Bharati Braille 2.0, NIEPVD, Jan 2025)
- A checkable correctness criterion with an honest two-tier validation methodology, not a single hand-wavy accuracy claim
- A go/no-go checkpoint that shows engineering maturity — you scoped based on real documentation constraints, not wishful planning
- Solo-feasible, no GPU/large dataset dependency
- Real accessibility impact with a credible path to external validation
