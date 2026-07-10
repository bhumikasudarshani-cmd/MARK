"""
braille_map.py

The core lookup table mapping Devanagari units (consonants, vowels, matras,
digits, punctuation, precomposed conjuncts) to their corresponding Bharati
Braille 2.0 Unicode cell(s).

SOURCE: NIEPVD "Standard Bharati Braille Codes with Unicode Mapped Chart",
released 4 January 2025 (Bharati Braille 2.0). See docs/RULEBOOK.md for the
full transcribed rulebook and the exact page references this data comes from.

Every entry here should be traceable to a row in docs/RULEBOOK.md section 2.
Do not add entries "by inference" from English Braille or other assumptions —
if it's not in the official chart, it doesn't go in this file without a
documented reason.
"""

# --- Dot-string to Unicode Braille cell conversion -------------------------

_DOT_BITS = {
    "1": 0x01,
    "2": 0x02,
    "3": 0x04,
    "4": 0x08,
    "5": 0x10,
    "6": 0x20,
}


def cell(dots: str) -> str:
    """
    Convert a dot-string like "1235" into a single Unicode Braille Patterns
    character (U+2800 block).

    Example: cell("13") -> the Braille cell for dots 1 and 3 raised.
    """
    if dots == "":
        return "\u2800"  # blank cell
    bitmask = 0
    for d in dots:
        if d not in _DOT_BITS:
            raise ValueError(f"Invalid dot number '{d}' in dot-string '{dots}'")
        bitmask |= _DOT_BITS[d]
    return chr(0x2800 + bitmask)


def cells(*dot_strings: str) -> str:
    """
    Convert a sequence of dot-strings (each representing one cell) into a
    string of Unicode Braille characters, one per cell, in order.

    Example: cells("5", "1235") -> two-cell sequence for ऋ.
    """
    return "".join(cell(d) for d in dot_strings)


# --- Independent vowels (स्वर) -----------------------------------------------
# Source: docs/RULEBOOK.md section 2, "Independent vowels"

INDEPENDENT_VOWELS = {
    "अ": cells("1"),
    "आ": cells("345"),
    "इ": cells("24"),
    "ई": cells("35"),
    "उ": cells("136"),
    "ऊ": cells("1256"),
    "ऋ": cells("5", "1235"),
    "ऌ": cells("5", "123"),
    "ए": cells("15"),
    "ऐ": cells("34"),
    "ऑ": cells("1346"),
    "ओ": cells("135"),
    "औ": cells("246"),
}

# --- Consonants (व्यंजन) -----------------------------------------------------

CONSONANTS = {
    "क": cells("13"),
    "ख": cells("46"),
    "ग": cells("1245"),
    "घ": cells("126"),
    "ङ": cells("346"),
    "च": cells("14"),
    "छ": cells("16"),
    "ज": cells("245"),
    "झ": cells("356"),
    "ञ": cells("25"),
    "ट": cells("23456"),
    "ठ": cells("2456"),
    "ड": cells("1246"),
    "ढ": cells("123456"),
    "ण": cells("3456"),
    "त": cells("2345"),
    "थ": cells("1456"),
    "द": cells("145"),
    "ध": cells("2346"),
    "न": cells("1345"),
    "प": cells("1234"),
    "फ": cells("124"),
    "ब": cells("12"),
    "भ": cells("45"),
    "म": cells("134"),
    "य": cells("13456"),
    "र": cells("1235"),
    "ल": cells("123"),
    "ळ": cells("456"),
    "व": cells("1236"),
    "श": cells("146"),
    "ष": cells("12346"),
    "स": cells("234"),
    "ह": cells("125"),
}

# --- Dependent vowel signs / matras -----------------------------------------
# IMPORTANT: these share the SAME Braille cell as the corresponding independent
# vowel (see docs/RULEBOOK.md section 3, rules 19-24). Whether a given input
# character should be treated as a vowel or a matra is a CONTEXTUAL decision
# made by the segmenter, not something this lookup table can encode alone.
# This table exists for completeness / documentation; the segmenter should
# route matra-context lookups through here explicitly so the distinction stays
# visible in the code, even though the resulting cell value is identical to
# the vowel table above.

MATRAS = {
    "ा": cells("345"),   # aa matra -- same cell as आ
    "ि": cells("24"),    # i matra -- same cell as इ
    "ी": cells("35"),    # ii matra -- same cell as ई
    "ु": cells("136"),   # u matra -- same cell as उ
    "ू": cells("1256"),  # uu matra -- same cell as ऊ
    "ृ": cells("5", "1235"),  # vocalic r matra
    "ॄ": cells("6", "1235"),  # vocalic rr matra
    "ॅ": cells("1346"),  # chandra e matra
    "े": cells("15"),    # e matra -- same cell as ए
    "ै": cells("34"),    # ai matra -- same cell as ऐ
    "ॉ": cells("1346"),  # chandra o matra
    "ो": cells("135"),   # o matra -- same cell as ओ
    "ौ": cells("246"),   # au matra -- same cell as औ
}

# --- Special marks -----------------------------------------------------------

SPECIAL_MARKS = {
    "ं": cells("56"),   # anusvara
    "ः": cells("6"),    # visarga
    "ँ": cells("3"),    # chandrabindu
    "्": cells("4"),    # virama/halant -- NOTE: has its own printable Braille
                         # cell (dot 4). Per rulebook rule 18/23, this cell is
                         # inserted BEFORE the consonant it affects, not after
                         # -- this is a real reordering the segmenter/rule
                         # engine must perform, not a passthrough mapping.
    "़": cells("5"),    # nukta -- prefix cell, inserted before the base
                         # consonant (rulebook rule 25)
    "ऽ": cells("2"),    # avagraha
}

# --- Precomposed conjuncts ---------------------------------------------------
# These two conjuncts have their OWN dedicated Braille cell and must NOT be
# decomposed into consonant + virama + consonant. The rule engine must check
# for these sequences FIRST, before falling through to generic virama
# composition, or these two extremely common conjuncts will be transcribed
# incorrectly (as 3 cells instead of 1).
#
# All OTHER conjuncts (e.g. त्र, श्र) are formed by normal composition:
# consonant + virama + consonant, per the general rule -- they are NOT listed
# here because they don't need special-casing.

PRECOMPOSED_CONJUNCTS = {
    "क्ष": cells("12345"),  # Ksha -- single cell, NOT क + ् + ष composed
    "ज्ञ": cells("156"),    # Gya -- single cell, NOT ज + ् + ञ composed
}

# --- Digits -------------------------------------------------------------------
# NOTE: per docs/RULEBOOK.md section 2, the number-sign (dots 3456) is only
# needed ONCE at the start of a digit sequence, not repeated per digit. This
# table gives the digit-letter cell only; the rule engine is responsible for
# prefixing the number-sign at the correct point in a sequence, not this
# lookup table.

NUMBER_SIGN = cells("3456")

DIGITS = {
    "०": cells("245"),
    "१": cells("1"),
    "२": cells("12"),
    "३": cells("14"),
    "४": cells("145"),
    "५": cells("15"),
    "६": cells("124"),
    "७": cells("1245"),
    "८": cells("125"),
    "९": cells("24"),
}

# --- Punctuation --------------------------------------------------------------
# Bharati Braille reuses the general Braille punctuation codes rather than
# defining separate per-language punctuation. Danda (।) is the one
# Devanagari-specific punctuation mark with its own dedicated code, confirmed
# directly in the Devanagari table (source PDF page 15).
#
# CAUTION: the source PDF's general (non-Devanagari) punctuation table, on
# page 4, gives a "Braille Dots" column that is NOT reliably the numeric dot
# list -- it appears in several rows to actually be a Braille-ASCII (BRF)
# shorthand character instead (the same shorthand system used elsewhere in
# the document for the "Braille Code (Dots)" column). Comma and period have
# an explicit numeric confirmation elsewhere in the prose rules ("comma...
# represented by Dot 2", "decimal point... represented by...Dot 46"), so
# those two are trustworthy. Question mark and exclamation mark do NOT have
# an equivalent explicit numeric confirmation in the prose -- do not guess.
# Resolve these properly in Week 1-2 by cross-referencing the standard
# Braille-ASCII (BRF) table before filling them in.

PUNCTUATION = {
    "।": cells("256"),   # danda (Devanagari full stop / purna viram) --
                          # confirmed directly in the Devanagari-specific table
    ",": cells("2"),      # comma -- confirmed via prose rule ("Dot 2")
    # "?" and "!" deliberately left unmapped -- see caution note above.
    # Do not fill these with guessed values; resolve via BRF ASCII
    # cross-reference or the Tier-2 external review before use.
}


def lookup_independent_vowel(unit: str) -> str:
    """Look up a Devanagari unit as an INDEPENDENT VOWEL (word-initial or
    after another vowel/matra -- see rulebook rules 19, 21)."""
    if unit not in INDEPENDENT_VOWELS:
        raise KeyError(f"'{unit}' is not a recognized independent vowel")
    return INDEPENDENT_VOWELS[unit]


def lookup_matra(unit: str) -> str:
    """Look up a Devanagari vowel unit as a MATRA (immediately follows a
    consonant, no explicit dot-1/अ marker -- see rulebook rule 20)."""
    if unit not in MATRAS:
        raise KeyError(f"'{unit}' is not a recognized matra")
    return MATRAS[unit]


def lookup_consonant(unit: str) -> str:
    if unit not in CONSONANTS:
        raise KeyError(f"'{unit}' is not a recognized consonant")
    return CONSONANTS[unit]


def lookup_precomposed_conjunct(unit: str) -> str:
    """Check the precomposed-conjunct table FIRST in the rule engine, before
    falling through to consonant+virama+consonant composition."""
    if unit not in PRECOMPOSED_CONJUNCTS:
        raise KeyError(f"'{unit}' is not a precomposed conjunct")
    return PRECOMPOSED_CONJUNCTS[unit]
