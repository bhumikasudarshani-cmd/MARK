"""
segmenter.py

Phase 1: tokenizes Devanagari text into units (consonant, independent vowel,
matra, special mark, digit, punctuation, other) and converts each to its
Bharati Braille cell.

SCOPE NOTE (important, read this before extending): this phase deliberately
does NOT handle conjuncts (consonant + virama + consonant clusters, including
the precomposed क्ष/ज्ञ exceptions). Virama characters are passed through
using their own cell for now, in their input position -- this is almost
certainly NOT the correct final behavior (see docs/RULEBOOK.md rule 18 on
virama reordering), but it means the pipeline runs end-to-end on non-conjunct
words while conjunct handling is built separately as Phase 2.

Why vowel/matra context-tracking (rulebook rules 19-24) is NOT implemented
here: those rules resolve an ambiguity specific to Braille -> text conversion
(both an independent vowel and its matching matra share the same Braille
cell, so going FROM Braille you need context to know which Devanagari
character to produce). Going Devanagari text -> Braille (this project's
scope), the input text already disambiguates vowel vs. matra via distinct
Unicode code points -- so a straightforward per-character table lookup is
correct for this direction. See conversation/design notes for the full
reasoning. If reverse conversion is ever added as a stretch goal, rules
19-24 will need to be implemented properly at that point.
"""

from braille_map import (
    INDEPENDENT_VOWELS,
    CONSONANTS,
    MATRAS,
    SPECIAL_MARKS,
    DIGITS,
    NUMBER_SIGN,
    PUNCTUATION,
)

# Token categories
CONSONANT = "consonant"
VOWEL = "vowel"
MATRA = "matra"
SPECIAL = "special"
DIGIT = "digit"
PUNCT = "punct"
OTHER = "other"


def classify(ch: str) -> str:
    """Classify a single Devanagari character by which table it belongs to."""
    if ch in CONSONANTS:
        return CONSONANT
    if ch in INDEPENDENT_VOWELS:
        return VOWEL
    if ch in MATRAS:
        return MATRA
    if ch in SPECIAL_MARKS:
        return SPECIAL
    if ch in DIGITS:
        return DIGIT
    if ch in PUNCTUATION:
        return PUNCT
    return OTHER


def tokenize(text: str):
    """
    Split text into a list of (char, category) tuples.

    Phase 1: one Devanagari character = one token. No conjunct/multi-character
    grouping yet -- that's Phase 2 (virama-triggered clustering).
    """
    return [(ch, classify(ch)) for ch in text]


def convert(text: str) -> str:
    """
    Convert Devanagari text to Bharati Braille (Phase 1: no conjunct
    handling). Whitespace and unrecognized characters are passed through
    unchanged; recognized units are replaced with their Braille cell.

    Digits: a single leading number-sign is inserted before a run of
    consecutive digits, per the "number sign not repeated per digit" rule
    (docs/RULEBOOK.md section 2). Multi-digit numbers are handled correctly;
    this does not yet handle decimal points or digit runs interrupted by
    other characters beyond the simple contiguous case.
    """
    tokens = tokenize(text)
    output = []
    in_digit_run = False

    for ch, category in tokens:
        if category == DIGIT:
            if not in_digit_run:
                output.append(NUMBER_SIGN)
                in_digit_run = True
            output.append(DIGITS[ch])
            continue
        else:
            in_digit_run = False

        if category == CONSONANT:
            output.append(CONSONANTS[ch])
        elif category == VOWEL:
            output.append(INDEPENDENT_VOWELS[ch])
        elif category == MATRA:
            output.append(MATRAS[ch])
        elif category == SPECIAL:
            # NOTE: virama passed through naively in input position for now.
            # Phase 2 must implement correct conjunct reordering (rule 18).
            output.append(SPECIAL_MARKS[ch])
        elif category == PUNCT:
            output.append(PUNCTUATION[ch])
        else:
            # whitespace, Latin characters, etc. -- pass through unchanged
            output.append(ch)

    return "".join(output)


if __name__ == "__main__":
    # Manual smoke test with a conjunct-free word: पानी (water) = प + ा + न + ी
    sample = "पानी"
    result = convert(sample)
    print(f"{sample} -> {result!r} ({len(result)} Braille cells + 0 other chars)")
