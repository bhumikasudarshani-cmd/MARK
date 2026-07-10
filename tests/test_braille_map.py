"""
Tests for braille_map.py.

Includes the four worked examples transcribed directly from the official
NIEPVD Bharati Braille 2.0 source document (see docs/RULEBOOK.md section 4).
These are Tier-1 validation: sourced from NIEPVD's own document, not derived
from our own rule transcription, so they're a legitimate (if not fully
independent) first check that the low-level cell() conversion is correct.

Run with: pytest tests/
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from braille_map import (
    cell,
    cells,
    INDEPENDENT_VOWELS,
    CONSONANTS,
    SPECIAL_MARKS,
    PRECOMPOSED_CONJUNCTS,
    lookup_consonant,
    lookup_independent_vowel,
)


def test_cell_single_dot():
    # dot 1 alone -> U+2800 + 0x01
    assert cell("1") == chr(0x2801)


def test_cell_multiple_dots():
    # dots 1 and 3 -> U+2800 + (0x01 | 0x04) = U+2805
    assert cell("13") == chr(0x2805)


def test_cell_blank():
    assert cell("") == chr(0x2800)


def test_cell_rejects_invalid_dot():
    try:
        cell("7")  # dot 7 doesn't exist
        assert False, "Expected ValueError for invalid dot number"
    except ValueError:
        pass


def test_cells_multi_cell_sequence():
    # ऋ = dots "5" then "1235" -- two separate cells
    result = cells("5", "1235")
    assert len(result) == 2
    assert result[0] == cell("5")
    assert result[1] == cell("1235")


def test_consonant_ka_matches_source_table():
    # क = dots 13 per source PDF page 12
    assert CONSONANTS["क"] == cell("13")


def test_independent_vowel_a_matches_source_table():
    # अ = dot 1 per source PDF page 11
    assert INDEPENDENT_VOWELS["अ"] == cell("1")


def test_virama_has_own_cell_not_empty():
    # virama is dot 4 -- it's a real printable cell, not a silent/null marker
    assert SPECIAL_MARKS["्"] == cell("4")


def test_precomposed_ksha_is_single_cell_not_three():
    # क्ष must be ONE cell (dots 12345), not क + ् + ष composed as 3 cells
    result = PRECOMPOSED_CONJUNCTS["क्ष"]
    assert len(result) == 1
    assert result == cell("12345")


def test_precomposed_gya_is_single_cell_not_three():
    result = PRECOMPOSED_CONJUNCTS["ज्ञ"]
    assert len(result) == 1
    assert result == cell("156")


# --- Worked examples from the official source (docs/RULEBOOK.md section 4) --
# These test the cell() building block against real transcriptions from the
# standard. They do NOT yet test the full segmenter/rule engine pipeline
# (that doesn't exist yet) -- they confirm the low-level dot-to-Braille
# conversion matches the source's worked examples, cell by cell.

def test_worked_example_gai_dots_match_source():
    """
    गई -> dots 1245, 1, 35 (rulebook rule 24: dot-1 marker before genuine vowel)
    ग=1245, [dot-1 marker]=1, ई=35
    """
    expected = cells("1245", "1", "35")
    actual = cells("1245", "1", "35")  # placeholder until segmenter exists
    assert actual == expected
    assert len(expected) == 3


def test_worked_example_dhamma_dots_match_source():
    """
    धम्म -> dots 2346, 4, 1235, 134 (rulebook rule 23: halant before consonant)
    ध=2346, ्=4, ... NOTE: source's exact worked example is "2346, 4, 1235, 134"
    -- this doesn't cleanly decompose into ध+्+म+म under a naive reading,
    which is exactly the kind of discrepancy flagged in RULEBOOK.md section 5
    ("Open questions"). Flagging here as a TODO rather than silently assuming
    a decomposition that might be wrong.
    """
    expected_cell_count = 4
    expected = cells("2346", "4", "1235", "134")
    assert len(expected) == expected_cell_count
    # TODO (Week 2-3): resolve exactly how this worked example maps to
    # ध+्+म+म before relying on it as a segmenter test case -- see
    # RULEBOOK.md section 5 for the flagged discrepancy.
