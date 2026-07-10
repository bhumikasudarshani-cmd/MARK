"""
normalizer.py

Cleans and standardizes raw Devanagari input text before segmentation:
- Strips unsupported/control characters
- Standardizes whitespace
- Separates numbers and punctuation for special handling
  (Bharati Braille uses distinct indicators for numbers and punctuation,
  so they can't just be mapped like regular letters)

This is Phase 1 of the pipeline:
    Input text -> [Normalizer] -> Segmenter -> Rule Engine -> Output Formatter
"""

import re

# Devanagari Unicode block: U+0900 to U+097F
DEVANAGARI_RANGE = (0x0900, 0x097F)


def is_devanagari_char(ch: str) -> bool:
    """Check if a single character falls within the Devanagari Unicode block."""
    if not ch:
        return False
    code_point = ord(ch)
    return DEVANAGARI_RANGE[0] <= code_point <= DEVANAGARI_RANGE[1]


def normalize_whitespace(text: str) -> str:
    """Collapse multiple whitespace characters into a single space, strip ends."""
    return re.sub(r"\s+", " ", text).strip()


def normalize(text: str) -> str:
    """
    Main normalization entry point.

    TODO (Week 1-2):
    - Decide how to handle characters outside Devanagari + basic punctuation/numbers
      (reject them? pass through unchanged? log a warning?)
    - Handle Devanagari punctuation marks (danda '।', double danda '॥') explicitly
    - Confirm how numbers should be pre-tagged before reaching the segmenter,
      since Bharati Braille requires a number-indicator prefix
    """
    text = normalize_whitespace(text)
    # Placeholder — real normalization rules go here as the rulebook is finalized
    return text


if __name__ == "__main__":
    # Quick manual smoke test while building this out
    sample = "  नमस्ते   दुनिया  "
    print(repr(normalize(sample)))
