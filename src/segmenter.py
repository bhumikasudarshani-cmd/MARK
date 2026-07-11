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
    PRECOMPOSED_CONJUNCTS,
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

def show_characters(text):
    for i in range(len(text)):
        print(i, text[i])   
def show_character_types(text):
    for i in range(len(text)):
        ch = text[i]
        if ch in CONSONANTS:
            print(i, ch, "-> consonant")
        else:
            print(i, ch, "-> not a consonant")

def find_conjuncts(text):
    units = []          # <- new: empty list to collect results
    i = 0
    while i < len(text):
        if i + 2 < len(text):
            conjunct = text[i:i+3]
            first = text[i]
            middle = text[i + 1]
            second = text[i + 2]

            if conjunct in PRECOMPOSED_CONJUNCTS:
                units.append(("precomposed", conjunct))
                i = i + 3
                continue

            if first in CONSONANTS and middle == "्" and second in CONSONANTS:
                units.append(("conjunct", first, second))   # <- was print(), now append
                i = i + 3
                continue
        

        units.append(("plain", text[i]))    # <- was print(), now append
        i = i + 1
    return units    # <- new: hand the list back

def units_to_braille(units):
    output = []

    

    for unit in units:
        unit_type = unit[0]

        if unit_type == "plain":
            char = unit[1]

            if char in CONSONANTS:
                output.append(CONSONANTS[char])
            elif char in INDEPENDENT_VOWELS:
                output.append(INDEPENDENT_VOWELS[char])
            elif char in MATRAS:
                output.append(MATRAS[char])
            elif char in SPECIAL_MARKS:
                output.append(SPECIAL_MARKS[char])
            elif char in DIGITS:
                output.append(DIGITS[char])
            elif char in PUNCTUATION:
                output.append(PUNCTUATION[char])
            else:
                output.append(char)  # whitespace, unknown chars pass through

        elif unit_type == "precomposed":
            conjunct_string = unit[1]
            output.append(PRECOMPOSED_CONJUNCTS[conjunct_string])

        elif unit_type == "conjunct":
            first = unit[1]
            second = unit[2]

            virama_cell = SPECIAL_MARKS["्"]
            first_cell = CONSONANTS[first]
            second_cell = CONSONANTS[second]

            output.append(virama_cell + first_cell + second_cell)

    return "".join(output)

if __name__ == "__main__":

        units = find_conjuncts("रक्षा")
        print(units)
        units2 = find_conjuncts("धर्म")
        print(units2)
        braille_output2 = units_to_braille(units2)
        print(f"धर्म -> {braille_output2!r} ({len(braille_output2)} cells)")
        braille_output = units_to_braille(units)
        print(f"रक्षा -> {braille_output!r}")
        sample = "पानी"
        result = convert(sample)
        print(f"{sample} -> {result!r} ({len(result)} Braille cells + 0 other chars)")
        print(f"रक्षा -> {braille_output!r} ({len(braille_output)} cells)")