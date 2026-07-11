"""
Tests for segmenter.py — Phase 2 (conjunct detection + Braille conversion).

These automate the manual terminal checks we already did by hand for:
- रक्षा (precomposed conjunct: क्ष)
- धर्म (general conjunct: र + ् + म, with virama reordering per rule 18)

Run with: pytest tests/
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from segmenter import find_conjuncts, units_to_braille
from braille_map import cell, CONSONANTS, SPECIAL_MARKS, PRECOMPOSED_CONJUNCTS


# --- Tests for find_conjuncts() ---------------------------------------------

def test_find_conjuncts_precomposed_case():
    result = find_conjuncts("रक्षा")
    expected = [("plain", "र"), ("precomposed", "क्ष"), ("plain", "ा")]
    assert result == expected


def test_find_conjuncts_general_conjunct_case():
    result = find_conjuncts("धर्म")
    expected = [("plain", "ध"), ("conjunct", "र", "म")]
    assert result == expected


def test_find_conjuncts_no_conjunct_word():
    result = find_conjuncts("पानी")
    expected = [("plain", "प"), ("plain", "ा"), ("plain", "न"), ("plain", "ी")]
    assert result == expected


def test_find_conjuncts_word_ending_right_after_a_consonant():
    result = find_conjuncts("क")
    expected = [("plain", "क")]
    assert result == expected


# --- Tests for units_to_braille() -------------------------------------------

def test_units_to_braille_precomposed_is_single_cell():
    units = [("precomposed", "क्ष")]
    result = units_to_braille(units)
    assert len(result) == 1
    assert result == PRECOMPOSED_CONJUNCTS["क्ष"]


def test_units_to_braille_general_conjunct_cell_count():
    units = [("conjunct", "र", "म")]
    result = units_to_braille(units)
    assert len(result) == 3


def test_units_to_braille_general_conjunct_cell_order():
    units = [("conjunct", "र", "म")]
    result = units_to_braille(units)

    expected_virama_cell = SPECIAL_MARKS["्"]
    expected_first_cell = CONSONANTS["र"]
    expected_second_cell = CONSONANTS["म"]

    assert result[0] == expected_virama_cell
    assert result[1] == expected_first_cell
    assert result[2] == expected_second_cell


def test_full_pipeline_dharma_four_cells():
    units = find_conjuncts("धर्म")
    result = units_to_braille(units)
    assert len(result) == 4


def test_full_pipeline_raksha_three_cells():
    units = find_conjuncts("रक्षा")
    result = units_to_braille(units)
    assert len(result) == 3