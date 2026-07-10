# Bharati Braille 2.0 — Extracted Rulebook (Hindi / Devanagari)

**Source:** "Standard Bharati Braille Codes with Unicode Mapped Chart", National Institute
for the Empowerment of Persons with Visual Disabilities (NIEPVD), Dehradun.
**Release date:** 4 January 2025 (Bharati Braille 2.0 — the ratified standard, not the
draft 2.1 revision that entered consultation Jan 2026).
**Official PDF:** https://cdnbbsr.s3waas.gov.in/s36ee69d3769e832ec77c9584e0b7ba112/uploads/2025/01/20250104954295710.pdf

This is the Week 1-2 deliverable: the actual rulebook, sourced directly from the
standard, that `src/braille_map.py` implements. Every mapping in the code should be
traceable back to a line in this document.

---

## 1. Braille cell basics

- 6-dot cell, 2 columns × 3 rows. Dots numbered 1,2,3 (top-to-bottom, left column),
  4,5,6 (top-to-bottom, right column).
- 63 possible dot combinations (2^6 - 1, excluding the blank cell).
- Represented digitally via Unicode Braille Patterns block (U+2800–U+28FF). Each dot
  combination maps to `U+2800 + bitmask`, where dot1=bit0, dot2=bit1, dot3=bit2,
  dot4=bit3, dot5=bit4, dot6=bit5.

---

## 2. Devanagari → Bharati Braille mapping (Hindi/Sanskrit/Marathi/Nepali section)

Full table transcribed from pages 11–16 of the source PDF. "Dots" column uses the
official numbering (e.g. "13" = dots 1 and 3 raised in one cell). A comma separates
multiple cells (e.g. "5, 1235" = dot 5 alone in one cell, followed by a second cell
with dots 1,2,3,5).

### Various signs
| Devanagari | Unicode | Dots |
|---|---|---|
| ँ (chandrabindu) | 0901 | 3 |
| ं (anusvara) | 0902 | 56 |
| ः (visarga) | 0903 | 6 |

### Independent vowels
| Devanagari | Dots |
|---|---|
| अ | 1 |
| आ | 345 |
| इ | 24 |
| ई | 35 |
| उ | 136 |
| ऊ | 1256 |
| ऋ | 5, 1235 |
| ऌ | 5, 123 |
| ए | 15 |
| ऐ | 34 |
| ऑ | 1346 |
| ओ | 135 |
| औ | 246 |

### Consonants
| Devanagari | Dots | | Devanagari | Dots |
|---|---|---|---|---|
| क | 13 | | प | 1234 |
| ख | 46 | | फ | 124 |
| ग | 1245 | | ब | 12 |
| घ | 126 | | भ | 45 |
| ङ | 346 | | म | 134 |
| च | 14 | | य | 13456 |
| छ | 16 | | र | 1235 |
| ज | 245 | | ल | 123 |
| झ | 356 | | ळ | 456 |
| ञ | 25 | | व | 1236 |
| ट | 23456 | | श | 146 |
| ठ | 2456 | | ष | 12346 |
| ड | 1246 | | स | 234 |
| ढ | 123456 | | ह | 125 |
| ण | 3456 | | | |
| त | 2345 | | | |
| थ | 1456 | | | |
| द | 145 | | | |
| ध | 2346 | | | |
| न | 1345 | | | |

### Nukta / Avagraha
| Devanagari | Dots |
|---|---|
| ़ (nukta) | 5 (prefix cell, precedes the base consonant) |
| ऽ (avagraha) | 2 |

### Dependent vowel signs (matras) — same Braille cell as the independent vowel
| Devanagari | Dots |
|---|---|
| ा | 345 |
| ि | 24 |
| ी | 35 |
| ु | 136 |
| ू | 1256 |
| ृ | 5, 1235 |
| ॄ | 6, 1235 |
| ॅ | 1346 |
| े | 15 |
| ै | 34 |
| ॉ | 1346 |
| ो | 135 |
| ौ | 246 |

**Important — matras and independent vowels share identical Braille cells.**
Bharati Braille does not use a separate "matra" glyph the way print Devanagari does.
Disambiguation between "this is an independent vowel" vs "this is a matra attached to
the previous consonant" is a **contextual rule**, not a different code point (see §3).

### Virama
| Devanagari | Dots |
|---|---|
| ् (virama/halant) | 4 |

### Digits
Digits are written as the number-sign (dots 3456, `#`) followed by the Braille
letter-equivalent of a,b,c...j (mirroring English Braille number convention):
| Devanagari | Dots |
|---|---|
| ० | 3456, 245 |
| १ | 3456, 1 |
| २ | 3456, 12 |
| ३ | 3456, 14 |
| ४ | 3456, 145 |
| ५ | 3456, 15 |
| ६ | 3456, 124 |
| ७ | 3456, 1245 |
| ८ | 3456, 125 |
| ९ | 3456, 24 |

**Rule (from source, §"Numbers in Braille"):** the number sign is not repeated for
every digit in a multi-digit number — it's only needed once at the start of a digit
sequence. E.g. "107" is `#` + a + j + g (i.e. number-sign once, then three digit-letters
back to back), not `#a#j#g`. This is a real rule engine detail, not just a lookup.

### Danda (Devanagari full stop)
| Devanagari | Dots |
|---|---|
| । (purna viram) | 256 |

### Precomposed conjuncts (own dedicated Braille cells — NOT virama+consonant composition)
| Devanagari | Dots | Note |
|---|---|---|
| क्ष (Ksha) | 12345 | Single cell, not क+्+ष composed |
| ज्ञ (Gya) | 156 | Single cell, not ज+्+ञ composed |

**This matters a lot for the segmenter/rule engine:** most conjuncts ARE built by
composing consonant + virama + consonant (see §3), but क्ष and ज्ञ are two named
exceptions with their own single dedicated Braille cell. The rule engine must check
for these two sequences first, before falling through to generic virama-composition
logic, or it will produce wrong (three-cell) output for these two very common
conjuncts.

Other conjunct examples in the source (त्र, श्र) are NOT special-cased — they are
formed by normal virama composition: त्र = त (2345) + ् (4) + र (1235), written as
three cells "4, 2345, 1235" per the source table (virama cell comes first in the
source's notation here, matching the general "virama precedes the consonant it
affects" rule in §3, rule 18 — but note the practical worked examples in the rules
section put the virama cell in-sequence with the consonants, so validate cell order
carefully against the worked examples in §4, not just this table's column order).

---

## 3. Segmentation & disambiguation rules (verbatim from source, rules 18–27)

These are the exact rules needed to build the segmenter — this is the hardest part
of the whole project, and having the primary source's own wording removes a lot of
the guesswork the original roadmap risk-flagged.

18. **Halant (्) should be inserted prior to the consonant which it is affecting.**
    (i.e., in Braille output, the virama cell comes *before* the consonant cell it
    modifies — this is different from print Devanagari's left-to-right visual order
    and is a genuine transformation the segmenter/rule engine must perform, not a
    passthrough.)

19. **If a word starts with a vowel, treat the entered Braille symbol as a vowel, not
    a matra.** Example: आई, इकाइयां, इलेक्ट्रॉन.

20. **If a vowel comes immediately after a consonant, it represents a matra, not a
    vowel** (even though the Braille cell is identical — see §2). Example: बाइबल,
    भालू, पानी, नीति, रूई.

21. **If the previous character entry was a vowel or a matra, the current entry is
    also treated as a vowel.** Example: आई, इकाइयां, बुआ, बहनोई, जमाई.

22. **Insertion ambiguity (लखनऊ vs भालू, "नऊ" vs "लू"):** whether a vowel-like segment
    following a consonant should be inserted as a vowel or a matra depends on this
    context chain, not on the character alone. If a vowel (not matra) is intended
    after a consonant, dot 1 (अ marker) must be explicitly inserted between the
    consonant and the vowel symbol; otherwise, the same symbol is read as a matra.

23. **हलंत (virama) — dot 4 — is always added *before* the consonant it affects.**
    Worked example: धम्म → dots **2346, 4, 1235, 134**
    (ध=2346, ्=4 [preceding the next consonant], म=1235... — note the source's own
    worked example is the authoritative reference; use it as a direct test case,
    see §4).

24. **Dot 1 (अ) is inserted whenever a स्वर अक्षर (vowel letter) immediately follows a
    consonant** (i.e., to signal "this is a genuine vowel, not a matra" per rule 20's
    default assumption). Worked example: गई → dots **1245, 1, 35**
    (ग=1245, अ-marker=1, ई=35).

25. **Nukta (़):** whichever character has a nukta, insert dot 5 *before* the base
    consonant. Example: ज़ → dots **5, 245**.

26. **When both halant and nukta occur in a word, halant (dot 4) is placed before the
    nukta.** Worked example: ज़यादा → dots **4, 5, 245, 13456, 345, 145, 345**.

27. **To denote different phonetic symbols of a phoneme** (dialectal/loanword sounds),
    the respective vowel/consonant should be preceded by dot 5 in each language.

### Practical implication for the segmenter

Rules 19–24 describe a **stateful, context-dependent** parse — you cannot decide
"vowel or matra" by looking at a single character in isolation. You need to track:
(a) whether the current position is word-initial, (b) what the immediately preceding
token was (consonant / vowel / matra), and (c) whether an explicit dot-1 marker is
present. This confirms the original critique's point #2: this is not a regex
substitution problem, it's a small stateful parser.

---

## 4. Worked examples (use these as Tier-1 validation test cases — §7 of ROADMAP.md)

These are sourced directly from the official standard document, not derived from
your own code — making them legitimate (if not fully independent) ground truth.

| Word | Expected Braille (dots, cell by cell) | Rule(s) demonstrated |
|---|---|---|
| धम्म | 2346, 4, 1235, 134 | 23 (halant before consonant) |
| गई | 1245, 1, 35 | 24 (dot 1 / अ marker before genuine vowel) |
| ज़ | 5, 245 | 25 (nukta marker) |
| ज़यादा | 4, 5, 245, 13456, 345, 145, 345 | 26 (halant + nukta ordering) |

**Action item:** add these four as the first entries in your test suite
(`tests/test_rule_engine.py`, once the rule engine exists) — they are your earliest
non-circular-ish validation, available from Week 1, no need to wait for external
review.

---

## 5. Open questions to resolve before/during the Rule Engine phase

- The source table's own column ordering for multi-cell entries (e.g. त्र listed as
  "4, 2345, 1235") vs. the prose rule ("halant precedes the consonant it affects")
  need to be cross-checked against more worked examples — don't assume the table
  formatting and the prose rule always agree on presentation order without checking
  a few more cases as you go.
- Punctuation and numbers each have their own contextual rules (number-sign not
  repeated per digit; punctuation dot-codes are the *English* Braille punctuation
  codes reused, per the general Braille punctuation table on page 4 of the source —
  Bharati Braille does not redefine punctuation separately per language).
- Version note: this document target Bharati Braille **2.0**. A draft 2.1 revision
  was in public consultation as of Jan 2026 — out of scope by design (see
  ROADMAP.md §1).
