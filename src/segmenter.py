"""
segmenter.py

Phase 1 + Phase 2: tokenizes Devanagari text into units (plain characters,
general conjuncts, precomposed conjuncts) and converts to Bharati Braille.

Pipeline: find_conjuncts() splits text into units -> units_to_braille()
converts units into actual Braille cells -> convert() ties both together
as the main entry point.
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
    units = []
    i = 0
    while i < len(text):
        if i + 2 < len(text):
            conjunct = text[i:i + 3]
            first = text[i]
            middle = text[i + 1]
            second = text[i + 2]

            if conjunct in PRECOMPOSED_CONJUNCTS:
                units.append(("precomposed", conjunct))
                i = i + 3
                continue

            if first in CONSONANTS and middle == "्" and second in CONSONANTS:
                units.append(("conjunct", first, second))
                i = i + 3
                continue

        units.append(("plain", text[i]))
        i = i + 1
    return units


def units_to_braille(units):
    output = []
    in_digit_run = False

    for unit in units:
        unit_type = unit[0]

        if unit_type == "plain":
            char = unit[1]

            if char in DIGITS:
                if not in_digit_run:
                    output.append(NUMBER_SIGN)
                    in_digit_run = True
                output.append(DIGITS[char])
                continue
            else:
                in_digit_run = False

            if char in CONSONANTS:
                output.append(CONSONANTS[char])
            elif char in INDEPENDENT_VOWELS:
                output.append(INDEPENDENT_VOWELS[char])
            elif char in MATRAS:
                output.append(MATRAS[char])
            elif char in SPECIAL_MARKS:
                output.append(SPECIAL_MARKS[char])
            elif char in PUNCTUATION:
                output.append(PUNCTUATION[char])
            else:
                output.append(char)

        elif unit_type == "precomposed":
            in_digit_run = False
            conjunct_string = unit[1]
            output.append(PRECOMPOSED_CONJUNCTS[conjunct_string])

        elif unit_type == "conjunct":
            in_digit_run = False
            first = unit[1]
            second = unit[2]

            virama_cell = SPECIAL_MARKS["्"]
            first_cell = CONSONANTS[first]
            second_cell = CONSONANTS[second]

            output.append(virama_cell + first_cell + second_cell)

    return "".join(output)


def convert(text):
    units = find_conjuncts(text)
    return units_to_braille(units)


if __name__ == "__main__":
    units = find_conjuncts("रक्षा")
    print(units)
    braille_output = units_to_braille(units)
    print(f"रक्षा -> {braille_output!r} ({len(braille_output)} cells)")

    units2 = find_conjuncts("धर्म")
    print(units2)
    braille_output2 = units_to_braille(units2)
    print(f"धर्म -> {braille_output2!r} ({len(braille_output2)} cells)")

    sample = "पानी"
    result = convert(sample)
    print(f"{sample} -> {result!r} ({len(result)} Braille cells + 0 other chars)")