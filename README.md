# Kashubian Corpus Analysis

NLP pipeline for analyzing the Kashubian Wikipedia corpus and generating language models for keyboard/predictive text development.

## Setup

```bash
pip install matplotlib numpy
```

## Usage

### Run Preprocessing Pipeline
```bash
python preprocessing/run_full_pipeline.py data/csbwiki-latest-pages-articles.xml.bz2
```

### Run Blacklist Script & Generate Language Models
```bash
python lexical_model/Corpus_Analysis.py
```

## Output

**Preprocessing** (`results/`):
- `tokens_preprocessed.txt` - Tokenized words
- `characters_preprocessed.txt` - Character sequence
- Zipf's law validation and coverage analysis charts (PNG)

**Language Models** (`lexical_model/results/`):
- `kashubian_lexical_model.json` - Unigram word frequencies
- `kashubian_language_model_bigrams.json` - Bigram probabilities
- `kashubian_language_model_trigrams.txt` - Trigram frequencies
- `kashubian_word_frequencies.txt` - Simple word list for Keyman

## Project Structure

```
├── preprocessing/          # Wikipedia XML processing
│   ├── kashubian_preprocessing.py
│   ├── kashubian_character_frequency.py
│   └── kashubian_word_frequency.py
├── lexical_model/          # Language model generation
│   ├── Corpus_Analysis.py
│   └── Blacklist.py
├── data/                   # Input Wikipedia dump
└── results/                # Output files
```