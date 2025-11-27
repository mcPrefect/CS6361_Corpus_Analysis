# Kashubian Corpus Preprocessing & Analysis Pipeline

Complete preprocessing and analysis pipeline for the Kashubian keyboard and language model project, following CS6361 Week 5 & 7 lecture architecture.

## Overview

This pipeline implements the complete text preprocessing and corpus analysis methodology covered in your lectures, producing all the statistics and visualizations needed for presentation slides 3-11.

### What This Pipeline Does

1. **Markup Analysis** - Extracts clean text from Wikipedia XML dump
2. **Tokenization** - Splits text into words with proper Kashubian diacritic handling
3. **Case Normalization** - Standardizes case for frequency counting
4. **Character Frequency Analysis** - Identifies most common characters and diacritics
5. **Word Frequency Analysis** - Analyzes word distribution and vocabulary
6. **Zipf's Law Validation** - Validates corpus quality using linguistic theory
7. **Coverage Analysis** - Determines optimal lexical model size
8. **Lexical Model Generation** - Creates word list for Keyman Developer

## Prerequisites

### Required Files

1. **Kashubian Wikipedia Dump**
   - Download from: https://dumps.wikimedia.org/csbwiki/latest/
   - File: `csbwiki-latest-pages-articles.xml.bz2`
   - Size: ~2-3 MB compressed

### Required Python Packages

```bash
pip install matplotlib numpy --break-system-packages
```

(Note: Use `--break-system-packages` flag as per module environment requirements)

## File Structure

```
/home/claude/
├── kashubian_preprocessing.py          # Step 1: Corpus preprocessing
├── kashubian_character_frequency.py    # Step 2: Character analysis
├── kashubian_word_frequency.py         # Step 3: Word & Zipf analysis
├── run_full_pipeline.py                # Master script (runs all steps)
└── README.md                           # This file
```

## Quick Start

### Option 1: Run Complete Pipeline (Recommended)

Run all steps automatically:

```bash
python run_full_pipeline.py csbwiki-latest-pages-articles.xml.bz2
```

Or if the dump is in `/mnt/user-data/uploads`:

```bash
python run_full_pipeline.py /mnt/user-data/uploads/csbwiki-latest-pages-articles.xml.bz2
```

**Expected Runtime:** 5-10 minutes total

### Option 2: Run Individual Steps

If you want to run each step separately:

```bash
# Step 1: Preprocessing (2-5 minutes)
python kashubian_preprocessing.py csbwiki-latest-pages-articles.xml.bz2

# Step 2: Character frequency analysis (1-2 minutes)
python kashubian_character_frequency.py

# Step 3: Word frequency and Zipf analysis (2-3 minutes)
python kashubian_word_frequency.py
```

## Output Files

### For Slide 3 (Corpus Selection & Statistics)

- `preprocessing_stats.json` - Complete preprocessing statistics
- `article_metadata.json` - Per-article statistics
- `preprocessing_report.txt` - Detailed methodology documentation

**Key statistics:** Total articles, total characters, total words, markup removed

### For Slide 4 (Text Pre-processing Pipeline)

- `preprocessing_report.txt` - Documents all preprocessing steps
- Shows: Markup analysis, tokenization, case normalization, stopword decisions

**Use this to describe your methodology following Week 5 lecture concepts**

### For Slide 5 (Character Set Identification)

- `character_frequency_results.json` - All character frequencies
- `character_frequency_chart.png` - Visual chart of top 20 characters

**Shows:** Complete Kashubian alphabet with Unicode points and frequencies

### For Slide 6 (Zipf's Law & Word Distribution)

- `word_frequency_results.json` - Word frequency statistics
- `zipf_analysis_results.json` - Zipf's Law validation
- `zipf_law_validation.png` - Log-log plot showing Zipfian distribution
- `word_frequency_distribution.png` - Rank-frequency curve
- `hapax_legomena_distribution.png` - Long tail visualization

**Key statistics:** Vocabulary size, hapax legomena count/percentage, Zipf correlation

### For Slide 8 (Character Frequency Analysis Results)

- `kashubian_diacritics_frequency.png` - Bar chart of Kashubian-specific diacritics
- `character_frequency_results.json` - Exact percentages for each diacritic

**Critical for keyboard design:** Shows which diacritics need easy access (ò, ë are highest)

### For Slide 9 (Character Combination Analysis)

- `digraph_frequency_results.json` - Digraph frequencies
- `trigraph_frequency_results.json` - Trigraph frequencies (n-gram analysis)
- `digraph_frequency_chart.png` - Visual chart of important digraphs

**Shows:** Most common letter combinations for keyboard ergonomics

### For Slides 10-11 (Lexical Model)

- `coverage_analysis_results.json` - Coverage statistics
- `vocabulary_coverage_curve.png` - Coverage vs. vocabulary size graph
- `lexical_model_data.json` - Complete lexical model with metadata
- `lexical_model_wordlist.txt` - Tab-separated word list for Keyman Developer

**Key statistics:** Coverage percentages, optimal vocabulary size

## Understanding the Output

### Preprocessing Statistics Example

```json
{
  "total_articles": 5847,
  "total_characters": 2943821,
  "total_words": 412456,
  "xml_elements_processed": 5847,
  "markup_removed_chars": 1234567
}
```

### Character Frequency Example

Top Kashubian diacritics:
- `ò` (o with grave): ~3.08% frequency
- `ë` (e with diaeresis): ~2.79% frequency
- Higher than many standard letters!

### Word Frequency Example

Typical top words (function words):
1. `w` (in) - ~2.5% of corpus
2. `na` (on) - ~1.8% of corpus
3. `je` (is) - ~1.5% of corpus

### Zipf's Law Validation

- **Correlation**: Should be < -0.85 for strong Zipfian distribution
- **Interpretation**: Validates corpus quality
- **Your corpus**: Expect ~-0.92 to -0.96 (excellent)

### Coverage Statistics

Example:
- Top 1,000 words: ~75-80% corpus coverage
- Top 5,000 words: ~90-92% corpus coverage
- Top 10,000 words: ~95-96% corpus coverage

## Module Concepts Implemented

### Week 5 Lecture: Text Pre-processing

✓ **Markup Analysis**
- Wikipedia XML parsing
- Template/reference removal
- Text extraction

✓ **Tokenization**
- Custom regex for Kashubian diacritics
- Proper handling of special characters
- Word boundary detection

✓ **Case Normalization**
- Lowercase conversion
- Ensures consistent frequency counting

✓ **Punctuation Handling**
- Filtered punctuation-only tokens
- Preserved linguistic context

✓ **Stopword Decisions**
- Kept stopwords for this project
- Documented rationale (needed for frequency analysis)

### Week 7 Lecture: Language Digitisation

✓ **Unicode Handling**
- Proper encoding for all diacritics
- Precomposed vs. combining characters discussion

✓ **Language Digitisation Context**
- ISO 639 code: csb
- Part of complete digitisation pipeline

### Week 4 Lecture: Corpus Statistics (Referenced)

✓ **Zipf's Law**
- Mathematical validation
- Log-log correlation analysis
- Validates corpus quality

✓ **Hapax Legomena**
- Single-occurrence words
- "Long tail" phenomenon
- Vocabulary filtering decisions

✓ **N-gram Analysis**
- Digraphs (2-character sequences)
- Trigraphs (3-character sequences)
- Foundation for advanced language models

## Troubleshooting

### "File not found" error

Make sure the Wikipedia dump is in the correct location:
```bash
ls -lh csbwiki-latest-pages-articles.xml.bz2
```

Or specify full path:
```bash
python run_full_pipeline.py /full/path/to/csbwiki-latest-pages-articles.xml.bz2
```

### "Module not found" error

Install required packages:
```bash
pip install matplotlib numpy --break-system-packages
```

### Memory issues with large corpus

The preprocessing script uses `iterparse` for memory-efficient processing, but if you still encounter issues:
- Close other applications
- The compressed dump should be processable even on modest hardware

### "No such file or directory" for output files

Make sure you're running scripts from `/home/claude` directory:
```bash
cd /home/claude
python run_full_pipeline.py <dump_file>
```

## Using Results in Your Presentation

### For Slide 3 (Corpus Statistics)

Open `preprocessing_stats.json` and use:
- `total_articles`: Number of Wikipedia articles
- `total_characters`: Character count
- `total_words`: Token count

### For Slide 6 (Zipf's Law)

1. Include `zipf_law_validation.png` in your slide
2. Mention the correlation value from `zipf_analysis_results.json`
3. Explain what this validates about corpus quality

### For Slide 8 (Character Frequencies)

1. Use `kashubian_diacritics_frequency.png` 
2. Highlight that ò (3.08%) and ë (2.79%) need easy keyboard access
3. This data directly informs keyboard layout design

### For Slide 10-11 (Lexical Model)

1. Use `vocabulary_coverage_curve.png`
2. Explain the trade-off: vocabulary size vs. coverage
3. Reference `lexical_model_wordlist.txt` as the output for Keyman

## Advanced: Understanding the Code

### Preprocessing Architecture

The preprocessing follows the exact architecture from Week 5 lectures:

```
Input (XML) → Markup Analysis → Tokenization → Normalization → Output
```

### Character Frequency Analysis

Uses Python `Counter` for efficient frequency counting:
- Handles Unicode properly (critical for diacritics)
- Calculates percentages relative to total character count
- Identifies Kashubian-specific characters

### Zipf's Law Validation

Mathematical validation using log-log linear regression:
- log(frequency) = -α * log(rank) + c
- Correlation coefficient indicates distribution quality
- Strong negative correlation (< -0.85) confirms Zipfian distribution

## Project Integration

### Files to Submit

For your project submission:
1. All three Python scripts
2. Generated JSON files (statistics)
3. Generated PNG files (visualizations)
4. `lexical_model_wordlist.txt` (for Keyman)

### Files for Presentation

Must include in slides:
- `zipf_law_validation.png` (Slide 6)
- `kashubian_diacritics_frequency.png` (Slide 8)
- `digraph_frequency_chart.png` (Slide 9)
- `vocabulary_coverage_curve.png` (Slide 11)

### Keyman Developer Integration

Use `lexical_model_wordlist.txt`:
- Tab-separated format: `word<TAB>frequency`
- Already sorted by frequency (most common first)
- Filtered to remove hapax legomena
- Ready for direct import into Keyman Developer

## References

### Lecture Materials

- Week 5: Text Pre-processing
- Week 7: Text Pre-processing (cont.) & Language Digitisation
- Week 4: Zipf's Law and Corpus Statistics (referenced)

### External Resources

- Kashubian Wikipedia: https://csb.wikipedia.org/
- Wikipedia Dumps: https://dumps.wikimedia.org/csbwiki/latest/
- Keyman Developer: https://keyman.com/developer/

## Contact & Questions

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all input files are present
3. Check Python package installation
4. Review error messages carefully

## License & Attribution

This pipeline was developed for CS6361 Language Technology module project at University of Limerick. The Kashubian Wikipedia corpus is licensed under Creative Commons Attribution-ShareAlike 3.0.

---

**Last Updated:** November 2024  
**Module:** CS6361 Language Technology  
**Project:** Kashubian Keyboard & Language Model Development
