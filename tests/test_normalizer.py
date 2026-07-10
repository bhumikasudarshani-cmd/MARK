"""
Starter tests for normalizer.py.
Run with: pytest tests/
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from normalizer import normalize, normalize_whitespace, is_devanagari_char


def test_normalize_whitespace_collapses_spaces():
    assert normalize_whitespace("नमस्ते    दुनिया") == "नमस्ते दुनिया"


def test_normalize_whitespace_strips_ends():
    assert normalize_whitespace("  नमस्ते  ") == "नमस्ते"


def test_is_devanagari_char_true_for_devanagari():
    assert is_devanagari_char("न") is True


def test_is_devanagari_char_false_for_latin():
    assert is_devanagari_char("a") is False


def test_is_devanagari_char_false_for_empty():
    assert is_devanagari_char("") is False


def test_normalize_basic_smoke_test():
    result = normalize("  नमस्ते   दुनिया  ")
    assert result == "नमस्ते दुनिया"
