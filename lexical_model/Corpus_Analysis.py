#!/usr/bin/env python3
"""
Kashubian Corpus Analysis - Complete Script
============================================

This script analyzes the Kashubian Wikipedia corpus and creates:
1. Lexical Model (Unigram) - Word frequencies
2. Language Model (Bigram) - Word pair frequencies with conditional probabilities
3. Language Model (Trigram) - Three-word sequence frequencies

CS6361 NLP Project
"""

import re
import sys
import json
import os
from collections import Counter, defaultdict
from datetime import datetime

from Blacklist import FINAL_BLACKLIST, WHITELIST, clean_corpus

# ============================================================================
# CONFIGURATION
# ============================================================================

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# Input file
CORPUS_FILE = os.path.join(PROJECT_ROOT, 'results', 'tokens_preprocessed.txt')

# Output files (in lexical_model/results/)
OUTPUT_DIR = os.path.join(SCRIPT_DIR, 'results')
os.makedirs(OUTPUT_DIR, exist_ok=True)

LEXICAL_MODEL_JSON = os.path.join(OUTPUT_DIR, 'kashubian_lexical_model.json')
LEXICAL_MODEL_TXT = os.path.join(OUTPUT_DIR, 'kashubian_lexical_model.txt')
WORD_FREQUENCIES_TXT = os.path.join(OUTPUT_DIR, 'kashubian_word_frequencies.txt')

BIGRAM_MODEL_JSON = os.path.join(OUTPUT_DIR, 'kashubian_language_model_bigrams.json')
BIGRAM_MODEL_TXT = os.path.join(OUTPUT_DIR, 'kashubian_language_model_bigrams.txt')

TRIGRAM_MODEL_TXT = os.path.join(OUTPUT_DIR, 'kashubian_language_model_trigrams.txt')

# Regex pattern for Kashubian words (includes diacritics and compound words)
WORD_PATTERN = r"[a-ząãéëłńòóôùżA-ZĄÃÉËŁŃÒÓÔÙŻ]+(?:['-][a-ząãéëłńòóôùżA-ZĄÃÉËŁŃÒÓÔÙŻ]+)*"

# ============================================================================
# QUALITY METRICS
# ============================================================================

def compute_corpus_quality(words, lexical_model):
    """
    Compute comprehensive corpus quality metrics.
    
    Args:
        words (list): List of words from corpus
        lexical_model (dict): Lexical model with word frequencies
        
    Returns:
        dict: Dictionary of quality metrics
    """
    unique_words = set(words)
    total_words = len(words)
    vocab_size = len(unique_words)
    
    # Type-Token Ratio (TTR) - Lexical diversity
    # Higher = more diverse vocabulary
    ttr = vocab_size / total_words if total_words > 0 else 0
    
    # Hapax Legomena - Words appearing only once
    # Indicator of vocabulary richness
    hapax = sum(1 for w, d in lexical_model.items() if d['count'] == 1)
    hapax_percentage = (hapax / vocab_size * 100) if vocab_size > 0 else 0
    
    # Dis Legomena - Words appearing exactly twice
    dis_legomena = sum(1 for w, d in lexical_model.items() if d['count'] == 2)
    dis_percentage = (dis_legomena / vocab_size * 100) if vocab_size > 0 else 0
    
    # Average word length
    avg_length = sum(len(w) for w in words) / total_words if total_words > 0 else 0
    
    # Coverage statistics - How many words needed to cover X% of corpus
    sorted_words = sorted(lexical_model.items(), 
                         key=lambda x: x[1]['count'], 
                         reverse=True)
    
    top_10_coverage = sum(d['count'] for w, d in sorted_words[:10]) / total_words * 100 if total_words > 0 else 0
    top_100_coverage = sum(d['count'] for w, d in sorted_words[:100]) / total_words * 100 if total_words > 0 else 0
    top_1000_coverage = sum(d['count'] for w, d in sorted_words[:1000]) / total_words * 100 if total_words > 0 else 0
    
    # Vocabulary growth rate (estimated)
    # How many new words per 1000 tokens
    if total_words >= 1000:
        sample_size = min(1000, total_words // 10)
        sample_unique = len(set(words[:sample_size]))
        vocab_growth_rate = (sample_unique / sample_size) * 1000
    else:
        vocab_growth_rate = ttr * 1000
    
    return {
        'type_token_ratio': ttr,
        'hapax_legomena': hapax,
        'hapax_percentage': hapax_percentage,
        'dis_legomena': dis_legomena,
        'dis_percentage': dis_percentage,
        'avg_word_length': avg_length,
        'top_10_coverage': top_10_coverage,
        'top_100_coverage': top_100_coverage,
        'top_1000_coverage': top_1000_coverage,
        'vocab_growth_rate': vocab_growth_rate,
    }


# ============================================================================
# SMOOTHING FUNCTIONS FOR LANGUAGE MODELS
# ============================================================================

def add_one_smoothed_prob(w1, w2, bigram_freq, word_freq):
    """
    Compute add-one (Laplace) smoothed probability for a specific bigram.
    Avoids materializing the full |V|x|V| matrix (which is too large).
    """
    vocab_size = len(word_freq)
    bigram_count = bigram_freq.get((w1, w2), 0)
    w1_count = word_freq.get(w1, 0)
    smoothed_count = bigram_count + 1
    return smoothed_count / (w1_count + vocab_size) if w1_count > 0 else 0


def good_turing_smoothing(freq_of_freqs):
    """
    Good-Turing smoothing - adjusts probability mass based on frequency of frequencies.
    
    Args:
        freq_of_freqs (dict): Frequency of each frequency (e.g., how many words appear exactly 1 time, 2 times, etc.)
        
    Returns:
        dict: Adjusted frequencies
    """
    adjusted = {}
    for freq, count in freq_of_freqs.items():
        if freq + 1 in freq_of_freqs:
            adjusted[freq] = ((freq + 1) * freq_of_freqs[freq + 1]) / count
        else:
            adjusted[freq] = freq
    return adjusted


# ============================================================================
# MAIN SCRIPT
# ============================================================================

def main():
    # Ensure console output can handle corpus characters without crashing
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    print("=" * 70)
    print("KASHUBIAN CORPUS ANALYSIS")
    print("=" * 70)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # ------------------------------------------------------------------------
    # STEP 1: Read the corpus
    # ------------------------------------------------------------------------
    print("Step 1: Reading corpus...")
    try:
        with open(CORPUS_FILE, 'r', encoding='utf-8') as f:
            text = f.read()
        print(f"- Corpus loaded: {len(text):,} characters")
    except FileNotFoundError:
        print(f"ERROR: Could not find '{CORPUS_FILE}'")
        print("Please ensure the corpus file is in the same directory as this script.")
        return
    
    # ------------------------------------------------------------------------
    # STEP 2: Tokenize - Extract all words
    # ------------------------------------------------------------------------
    print("\nStep 2: Tokenizing words...")
    # Preserve original case for analysis
    raw_words_original_case = re.findall(WORD_PATTERN, text)
    # Normalize to lowercase for cleaning (blacklist matching)
    raw_words = [w.lower() for w in raw_words_original_case]
    original_total_words = len(raw_words)
    
    # Clean the corpus using the verified blacklist/whitelist
    words, cleaning_stats = clean_corpus(raw_words)
    cleaning_stats['blacklist_size'] = len(FINAL_BLACKLIST)
    cleaning_stats['whitelist_size'] = len(WHITELIST)
    
    total_words = len(words)
    unique_words_count = len(set(words))
    
    print(f"- Total words (raw): {original_total_words:,}")
    print(f"- Removed by blacklist: {cleaning_stats['removed_words']:,} ({cleaning_stats['percentage_removed']:.2f}%)")
    print(f"- Total words (clean): {total_words:,}")
    print(f"- Unique words: {unique_words_count:,}")
    
    # ------------------------------------------------------------------------
    # STEP 3: Create LEXICAL MODEL (Unigram)
    # ------------------------------------------------------------------------
    print("\nStep 3: Creating lexical model (unigram)...")
    word_freq = Counter(words)
    
    # Calculate probabilities
    lexical_model = {}
    for word, count in word_freq.items():
        lexical_model[word] = {
            'count': count,
            'probability': count / total_words,
            'percentage': (count / total_words) * 100
        }
    
    # Compute corpus quality metrics once for reuse
    quality_metrics = compute_corpus_quality(words, lexical_model)

    # Save complete model as JSON
    print(f"  -> Saving to {LEXICAL_MODEL_JSON}...")
    with open(LEXICAL_MODEL_JSON, 'w', encoding='utf-8') as f:
        json.dump({
            'metadata': {
                'created': datetime.now().isoformat(),
                'source': CORPUS_FILE,
                'model_type': 'lexical_model_unigram',
                'cleaning': cleaning_stats
            },
            'statistics': {
                'total_words': total_words,
                'unique_words': len(lexical_model)
            },
            'quality_metrics': quality_metrics,
            'words': lexical_model
        }, f, ensure_ascii=False, indent=2)
    
    # Save top 1000 words as human-readable text
    print(f"  -> Saving to {LEXICAL_MODEL_TXT}...")
    with open(LEXICAL_MODEL_TXT, 'w', encoding='utf-8') as f:
        f.write("KASHUBIAN LEXICAL MODEL (TOP 1000 WORDS)\n")
        f.write("=" * 70 + "\n")
        f.write(f"Total words: {total_words:,}\n")
        f.write(f"Unique words: {len(lexical_model):,}\n")
        f.write(f"Cleaned with blacklist: removed {cleaning_stats['removed_words']:,} words "
                f"({cleaning_stats['percentage_removed']:.2f}%)\n")
        f.write(f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"{'Rank':<6} {'Word':<20} {'Count':<10} {'Probability':<15} {'Percentage'}\n")
        f.write("-" * 70 + "\n")
        
        sorted_words = sorted(lexical_model.items(), 
                             key=lambda x: x[1]['count'], 
                             reverse=True)
        
        for i, (word, data) in enumerate(sorted_words[:1000], 1):
            f.write(f"{i:<6} {word:<20} {data['count']:<10} "
                   f"{data['probability']:<15.8f} {data['percentage']:.4f}%\n")
    
    # Save simple word frequency list
    print(f"  -> Saving to {WORD_FREQUENCIES_TXT}...")
    with open(WORD_FREQUENCIES_TXT, 'w', encoding='utf-8') as f:
        f.write("KASHUBIAN WORD FREQUENCIES\n")
        f.write("=" * 70 + "\n\n")
        for word, count in word_freq.most_common():
            f.write(f"{word}\t{count}\n")
    
    print(f"- Lexical model created: {len(lexical_model):,} words")
    
    # Print top 10 words
    print("\n  Top 10 words:")
    for i, (word, data) in enumerate(sorted_words[:10], 1):
        print(f"    {i}. {word:<15} {data['count']:>8,} times ({data['percentage']:.2f}%)")
    
    # ------------------------------------------------------------------------
    # STEP 3.5: Calculate corpus quality metrics
    # ------------------------------------------------------------------------
    print("\nStep 3.5: Computing corpus quality metrics...")
    print(f"  - Type-Token Ratio: {quality_metrics['type_token_ratio']:.4f}")
    print(f"  - Hapax Legomena: {quality_metrics['hapax_legomena']:,} words ({quality_metrics['hapax_percentage']:.2f}%)")
    print(f"  - Average word length: {quality_metrics['avg_word_length']:.2f} characters")
    print(f"  - Top 100 words cover: {quality_metrics['top_100_coverage']:.2f}% of corpus")
    
    # ------------------------------------------------------------------------
    # STEP 4: Create LANGUAGE MODEL (Bigram)
    # ------------------------------------------------------------------------
    print("\nStep 4: Creating bigram language model...")
    
    # Create all word bigrams
    word_bigrams = []
    for i in range(len(words) - 1):
        word_bigrams.append((words[i], words[i+1]))
    
    bigram_freq = Counter(word_bigrams)
    total_bigrams = sum(bigram_freq.values())
    
    print(f"- Total bigrams: {total_bigrams:,}")
    print(f"- Unique bigrams: {len(bigram_freq):,}")
    
    # Calculate conditional probabilities
    # P(word2|word1) = Count(word1, word2) / Count(word1)
    bigram_model = defaultdict(dict)
    
    for (w1, w2), count in bigram_freq.items():
        w1_count = word_freq[w1]
        
        # Conditional probability: P(w2|w1)
        conditional_prob = count / w1_count
        
        # Joint probability: P(w1, w2)
        joint_prob = count / total_bigrams
        
        bigram_model[w1][w2] = {
            'count': count,
            'conditional_probability': conditional_prob,
            'joint_probability': joint_prob
        }
    
    # Save complete bigram model as JSON
    print(f"  -> Saving to {BIGRAM_MODEL_JSON}...")
    with open(BIGRAM_MODEL_JSON, 'w', encoding='utf-8') as f:
        json.dump({
            'metadata': {
                'created': datetime.now().isoformat(),
                'source': CORPUS_FILE,
                'model_type': 'language_model_bigram',
                'cleaning': cleaning_stats
            },
            'statistics': {
                'total_bigrams': total_bigrams,
                'unique_bigrams': len(bigram_freq)
            },
            'bigrams': dict(bigram_model)
        }, f, ensure_ascii=False, indent=2)
    
    # Save top 100 bigrams as human-readable text
    print(f"  -> Saving to {BIGRAM_MODEL_TXT}...")
    with open(BIGRAM_MODEL_TXT, 'w', encoding='utf-8') as f:
        f.write("KASHUBIAN BIGRAM LANGUAGE MODEL (TOP 100)\n")
        f.write("=" * 70 + "\n")
        f.write(f"Total bigrams: {total_bigrams:,}\n")
        f.write(f"Unique bigrams: {len(bigram_freq):,}\n")
        f.write(f"Cleaned with blacklist: removed {cleaning_stats['removed_words']:,} words "
                f"({cleaning_stats['percentage_removed']:.2f}%)\n")
        f.write(f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"{'Rank':<6} {'Bigram':<35} {'Count':<10} {'Probability'}\n")
        f.write("-" * 70 + "\n")
        
        for i, ((w1, w2), count) in enumerate(bigram_freq.most_common(100), 1):
            prob = count / total_bigrams
            bigram_str = f"{w1} {w2}"
            f.write(f"{i:<6} {bigram_str:<35} {count:<10} {prob:.6f}\n")
    
    print(f"- Bigram model created: {len(bigram_freq):,} word pairs")
    
    # Print top 10 bigrams
    print("\n  Top 10 bigrams:")
    for i, ((w1, w2), count) in enumerate(bigram_freq.most_common(10), 1):
        conditional = bigram_model[w1][w2]['conditional_probability']
        print(f"    {i}. {w1} {w2:<15} {count:>6,} times (P({w2}|{w1})={conditional:.3f})")
    
    # ------------------------------------------------------------------------
    # STEP 4.5: Create smoothed bigram model (optional)
    # ------------------------------------------------------------------------
    print("\nStep 4.5: Creating smoothed bigram model...")
    print("  Note: Smoothing helps handle unseen word pairs")
    
    # Example: show difference for a few bigrams without materializing full matrix
    vocab_size = len(word_freq)
    print("\n  Example smoothing effects (first 3 bigrams):")
    for i, ((w1, w2), count) in enumerate(bigram_freq.most_common(3), 1):
        original_prob = bigram_model[w1][w2]['conditional_probability']
        smoothed_prob = add_one_smoothed_prob(w1, w2, bigram_freq, word_freq)
        print(f"    {w1} -> {w2}: Original P={original_prob:.6f}, Smoothed P={smoothed_prob:.6f}")
    
    print(f"\n  Note: Full smoothed matrix is skipped to avoid excessive memory use; sample shown above.")
    
    # ------------------------------------------------------------------------
    # STEP 5: Create LANGUAGE MODEL (Trigram)
    # ------------------------------------------------------------------------
    print("\nStep 5: Creating trigram language model...")
    
    # Create all word trigrams
    word_trigrams = []
    for i in range(len(words) - 2):
        word_trigrams.append((words[i], words[i+1], words[i+2]))
    
    trigram_freq = Counter(word_trigrams)
    total_trigrams = sum(trigram_freq.values())
    
    print(f"- Total trigrams: {total_trigrams:,}")
    print(f"- Unique trigrams: {len(trigram_freq):,}")
    
    # Save top 100 trigrams as text (full model would be ~38 MB)
    print(f"  -> Saving to {TRIGRAM_MODEL_TXT}...")
    with open(TRIGRAM_MODEL_TXT, 'w', encoding='utf-8') as f:
        f.write("KASHUBIAN TRIGRAM LANGUAGE MODEL (TOP 100)\n")
        f.write("=" * 70 + "\n")
        f.write(f"Total trigrams: {total_trigrams:,}\n")
        f.write(f"Unique trigrams: {len(trigram_freq):,}\n")
        f.write(f"Cleaned with blacklist: removed {cleaning_stats['removed_words']:,} words "
                f"({cleaning_stats['percentage_removed']:.2f}%)\n")
        f.write(f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Note: Only top 100 saved (full model would be ~38 MB)\n\n")
        f.write(f"{'Rank':<6} {'Trigram':<45} {'Count':<10} {'Probability'}\n")
        f.write("-" * 70 + "\n")
        
        for i, ((w1, w2, w3), count) in enumerate(trigram_freq.most_common(100), 1):
            prob = count / total_trigrams
            trigram_str = f"{w1} {w2} {w3}"
            f.write(f"{i:<6} {trigram_str:<45} {count:<10} {prob:.6f}\n")
    
    print(f"- Trigram model created: {len(trigram_freq):,} sequences")
    
    # Print top 5 trigrams
    print("\n  Top 5 trigrams:")
    for i, ((w1, w2, w3), count) in enumerate(trigram_freq.most_common(5), 1):
        print(f"    {i}. {w1} {w2} {w3:<20} {count:>4,} times")
    
    # ------------------------------------------------------------------------
    # STEP 6: Summary
    # ------------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"\nCorpus cleaning: removed {cleaning_stats['removed_words']:,} of {cleaning_stats['original_words']:,} words "
          f"({cleaning_stats['percentage_removed']:.2f}%) using blacklist {cleaning_stats['blacklist_size']} "
          f"and whitelist {cleaning_stats['whitelist_size']}")
    
    print(f"\nCorpus Quality Metrics:")
    print(f"   - Type-Token Ratio: {quality_metrics['type_token_ratio']:.4f} (lexical diversity)")
    print(f"   - Hapax Legomena: {quality_metrics['hapax_legomena']:,} ({quality_metrics['hapax_percentage']:.2f}%)")
    print(f"   - Dis Legomena: {quality_metrics['dis_legomena']:,} ({quality_metrics['dis_percentage']:.2f}%)")
    print(f"   - Average word length: {quality_metrics['avg_word_length']:.2f} chars")
    print(f"   - Top 10 coverage: {quality_metrics['top_10_coverage']:.2f}%")
    print(f"   - Top 100 coverage: {quality_metrics['top_100_coverage']:.2f}%")
    print(f"   - Top 1000 coverage: {quality_metrics['top_1000_coverage']:.2f}%")
    
    print(f"\nLexical Model (Unigram):")
    print(f"   - {len(lexical_model):,} unique words")
    print(f"   - {total_words:,} total word occurrences")
    print(f"   - Top word: '{sorted_words[0][0]}' ({sorted_words[0][1]['count']:,} times)")
    
    print(f"\nLanguage Model (Bigram):")
    print(f"   - {len(bigram_freq):,} unique word pairs")
    print(f"   - {total_bigrams:,} total bigram occurrences")
    top_bigram = bigram_freq.most_common(1)[0]
    print(f"   - Top bigram: '{top_bigram[0][0]} {top_bigram[0][1]}' ({top_bigram[1]:,} times)")
    
    print(f"\nLanguage Model (Trigram):")
    print(f"   - {len(trigram_freq):,} unique sequences")
    print(f"   - {total_trigrams:,} total trigram occurrences")
    top_trigram = trigram_freq.most_common(1)[0]
    print(f"   - Top trigram: '{top_trigram[0][0]} {top_trigram[0][1]} {top_trigram[0][2]}' ({top_trigram[1]:,} times)")
    
    print(f"\nFiles Created:")
    print(f"   1. {LEXICAL_MODEL_JSON} (lexical model - complete)")
    print(f"   2. {LEXICAL_MODEL_TXT} (lexical model - top 1000)")
    print(f"   3. {WORD_FREQUENCIES_TXT} (simple word list)")
    print(f"   4. {BIGRAM_MODEL_JSON} (bigram model - complete)")
    print(f"   5. {BIGRAM_MODEL_TXT} (bigram model - top 100)")
    print(f"   6. {TRIGRAM_MODEL_TXT} (trigram model - top 100)")
    
    print(f"\nAnalysis complete!")
    print(f"Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)


# ============================================================================
# EXAMPLE USAGE FUNCTIONS
# ============================================================================

def example_word_prediction(lexical_model_file, prefix, top_n=5):
    """
    Example: Predict words starting with a given prefix
    
    Usage:
        example_word_prediction('kashubian_lexical_model.json', 'k', 5)
    """
    with open(lexical_model_file, 'r', encoding='utf-8') as f:
        model = json.load(f)
    
    words = model['words']
    matches = {word: data['count'] 
               for word, data in words.items() 
               if word.startswith(prefix.lower())}
    
    sorted_matches = sorted(matches.items(), key=lambda x: x[1], reverse=True)
    
    print(f"\nTop {top_n} words starting with '{prefix}':")
    for i, (word, count) in enumerate(sorted_matches[:top_n], 1):
        print(f"  {i}. {word} ({count:,} times)")
    
    return [word for word, _ in sorted_matches[:top_n]]


def example_next_word_prediction(bigram_model_file, previous_word, top_n=5):
    """
    Example: Predict next word given previous word
    
    Usage:
        example_next_word_prediction('kashubian_language_model_bigrams.json', 'to', 5)
    """
    with open(bigram_model_file, 'r', encoding='utf-8') as f:
        model = json.load(f)
    
    bigrams = model['bigrams']
    
    if previous_word.lower() not in bigrams:
        print(f"\nWord '{previous_word}' not found in bigram model")
        return []
    
    following_words = bigrams[previous_word.lower()]
    sorted_words = sorted(following_words.items(), 
                         key=lambda x: x[1]['conditional_probability'], 
                         reverse=True)
    
    print(f"\nTop {top_n} words after '{previous_word}':")
    for i, (word, data) in enumerate(sorted_words[:top_n], 1):
        prob = data['conditional_probability']
        count = data['count']
        print(f"  {i}. {word:<15} (P={prob:.3f}, count={count:,})")
    
    return [word for word, _ in sorted_words[:top_n]]


# ============================================================================
# RUN SCRIPT
# ============================================================================

if __name__ == "__main__":
    main()
    
    # Uncomment to test prediction functions:
    # print("\n" + "=" * 70)
    # print("TESTING PREDICTION FUNCTIONS")
    # print("=" * 70)
    # example_word_prediction('kashubian_lexical_model.json', 'k', 5)
    # example_next_word_prediction('kashubian_language_model_bigrams.json', 'to', 5)
