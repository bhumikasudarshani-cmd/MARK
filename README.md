# Bharati Braille Digital Toolkit

A rule-based converter that translates Devanagari (Hindi) text into **Bharati Braille** — the unified Braille standard used across Indian languages.

## Why this project exists

Digital tools for English Braille (Duxbury, Braille2000, etc.) are mature and widely available. Equivalent tools for **Bharati Braille** — used for Hindi, Marathi, Bengali, and other Indian languages — are scarce, outdated, or entirely manual. This creates a real bottleneck: producing Braille textbooks and materials for blind students in regional-language education is slow and expensive, handled by only a handful of specialized centers in India.

This project aims to build an open, checkable, rule-based converter that anyone (a teacher, NGO, or student) can use to convert Devanagari text into correct Bharati Braille — starting with Hindi.

## Status

🚧 Early development — currently building the core rule engine (Weeks 1–7 of the roadmap in `docs/ROADMAP.md`).

## How it works (planned architecture)

```
Input text (Devanagari)
    → Text Normalizer
    → Syllable/Grapheme Segmenter (handles conjuncts via virama detection)
    → Rule Engine (Devanagari unit → Bharati Braille cell)
    → Output Formatter (Unicode Braille / .brf embosser file)
```

See `docs/ROADMAP.md` for the full week-by-week plan and `docs/RULEBOOK.md` for the Devanagari-to-Braille mapping rules as they're documented.

## Project structure

```
bharati-braille-toolkit/
├── src/            # core converter logic
├── tests/          # unit tests validating conversion correctness
├── docs/           # roadmap, rulebook, research notes
├── data/           # test cases, reference mappings
├── requirements.txt
└── README.md
```

## Setup

```bash
git clone https://github.com/<your-username>/bharati-braille-toolkit.git
cd bharati-braille-toolkit
pip install -r requirements.txt
```

## Scope (current MVP)

- [x] Project scaffolding
- [ ] Devanagari-to-Bharati-Braille rulebook documented
- [ ] Text normalizer
- [ ] Syllable segmenter (conjunct handling via virama detection)
- [ ] Rule engine (core mapping logic)
- [ ] Unicode Braille + `.brf` output
- [ ] Test suite against known-correct examples
- [ ] Simple web interface

**Out of scope for MVP** (potential future work): OCR input, reverse conversion (Braille → text), Grade 2 contractions, additional languages beyond Hindi.

## Disclaimer

This tool is intended to assist in generating Braille materials and should be reviewed by a qualified Braille transcriber or educator before use in official educational materials, especially during early development.

## License

MIT — see `LICENSE`.
