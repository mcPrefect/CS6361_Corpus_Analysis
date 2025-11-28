# Workload Declaration

[22336842] Michael:
I was responsible for keyboard development work, including character set identification, desktop and mobile keyboard design, frequency-optimised key placement, and implementation in Keyman Developer. I conducted character and digraph frequency analysis on the corpus. I also handled preprocessing steps including markup analysis, tokenisation, case normalisation. 

Darren:
I was responsible for lexical model development, including word frequency analysis, vocabulary selection and filtering, coverage analysis, and lexical model file generation. He handled blacklisting preprocessing and performed Zipf's Law validation and hapax legomena analysis. He researched advanced language modeling techniques including n-gram models and smoothing methods. 

Joint Responsibilities:
We both worked on corpus collection, project planning and methodology, presentation preparation, and final documentation.


# Kashubian Corpus Analysis

NLP pipeline for analysing the Kashubian Wikipedia corpus and generating language models for keyboard/predictive text development.

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