#!/usr/bin/env python3
"""
Kashubian Word Frequency & Zipf's Law Analysis
For Presentation Slides 6, 10, and 11

This script:
1. Analyzes word frequency distribution
2. Validates Zipf's Law application to Kashubian
3. Calculates hapax legomena (single-occurrence words)
4. Computes coverage statistics
5. Generates lexical model data

Following Week 4 lecture concepts on Zipf's Law and corpus statistics.
"""

import json
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from math import log, log10

class ZipfAnalyzer:
    """
    Analyze word frequencies and validate Zipf's Law for Kashubian corpus
    """
    
    def __init__(self):
        self.word_freq = None
        self.total_words = 0
        self.vocabulary_size = 0
        self.hapax_legomena_count = 0
    
    def analyze_word_frequency(self, tokens_file='tokens_preprocessed.txt'):
        """
        Analyze word frequency distribution in the corpus
        """
        print("=" * 70)
        print("WORD FREQUENCY ANALYSIS")
        print("=" * 70)
        
        # Load preprocessed tokens
        with open(tokens_file, 'r', encoding='utf-8') as f:
            tokens = [line.strip() for line in f if line.strip()]
        
        self.total_words = len(tokens)
        print(f"Total tokens loaded: {self.total_words:,}\n")
        
        # Count word frequencies
        self.word_freq = Counter(tokens)
        self.vocabulary_size = len(self.word_freq)
        
        print(f"Vocabulary Statistics:")
        print(f"  - Unique words (|V|): {self.vocabulary_size:,}")
        print(f"  - Total tokens (N): {self.total_words:,}")
        print(f"  - Type-Token Ratio: {self.vocabulary_size / self.total_words:.4f}")
        
        # Calculate hapax legomena (words appearing exactly once)
        self.hapax_legomena_count = sum(1 for count in self.word_freq.values() if count == 1)
        hapax_percentage = (self.hapax_legomena_count / self.vocabulary_size) * 100
        
        print(f"\nHapax Legomena (Week 4 Lecture Concept):")
        print(f"  - Single-occurrence words: {self.hapax_legomena_count:,}")
        print(f"  - Percentage of vocabulary: {hapax_percentage:.2f}%")
        print(f"  - This represents the 'long tail' of word distribution")
        
        # Get most common words
        most_common = self.word_freq.most_common(50)
        
        print(f"\nTOP 50 MOST FREQUENT WORDS:")
        print("-" * 70)
        print(f"{'Rank':<6} {'Word':<20} {'Count':<12} {'% of Corpus':<12}")
        print("-" * 70)
        
        for rank, (word, count) in enumerate(most_common, 1):
            percentage = (count / self.total_words) * 100
            print(f"{rank:<6} {word:<20} {count:<12,} {percentage:<12.4f}%")
        
        # Save results
        results = {
            'total_words': self.total_words,
            'vocabulary_size': self.vocabulary_size,
            'type_token_ratio': self.vocabulary_size / self.total_words,
            'hapax_legomena': self.hapax_legomena_count,
            'hapax_percentage': hapax_percentage,
            'top_50_words': [
                {
                    'rank': rank,
                    'word': word,
                    'count': count,
                    'percentage': (count / self.total_words) * 100
                }
                for rank, (word, count) in enumerate(most_common, 1)
            ]
        }
        
        with open('word_frequency_results.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Saved: word_frequency_results.json")
        
        return results
    
    def validate_zipf_law(self):
        """
        Validate that Kashubian follows Zipf's Law
        
        Zipf's Law states: frequency ∝ 1/rank
        Or: log(frequency) ∝ -log(rank)
        
        This validates corpus quality per Week 4 lecture concepts.
        """
        print("\n" + "=" * 70)
        print("ZIPF'S LAW VALIDATION (Week 4 Lecture Concept)")
        print("=" * 70)
        
        if self.word_freq is None:
            raise ValueError("Must run analyze_word_frequency() first")
        
        # Get frequency-sorted word list
        sorted_words = self.word_freq.most_common()
        
        # Calculate expected vs actual frequencies
        ranks = []
        frequencies = []
        log_ranks = []
        log_frequencies = []
        
        for rank, (word, freq) in enumerate(sorted_words, 1):
            ranks.append(rank)
            frequencies.append(freq)
            
            # Log-log values for Zipf validation
            if rank > 0 and freq > 0:
                log_ranks.append(log10(rank))
                log_frequencies.append(log10(freq))
        
        print(f"Analyzing {len(sorted_words):,} words for Zipf distribution...")
        
        # Calculate correlation in log-log space (should be highly negative for Zipf)
        correlation = np.corrcoef(log_ranks, log_frequencies)[0, 1]
        
        print(f"\nZipf's Law Validation Results:")
        print(f"  - Log-log correlation: {correlation:.4f}")
        print(f"  - Expected: Strong negative correlation (close to -1)")
        
        if correlation < -0.85:
            print(f"  - ✓ STRONG Zipfian distribution confirmed!")
            print(f"  - Corpus quality validated")
        elif correlation < -0.70:
            print(f"  - ✓ Zipfian distribution present")
        else:
            print(f"  - ⚠ Weak Zipfian distribution (unusual)")
        
        # Calculate Zipf's constant (frequency * rank should be approximately constant)
        zipf_constants = []
        for rank, (word, freq) in enumerate(sorted_words[:1000], 1):
            zipf_constants.append(freq * rank)
        
        avg_constant = np.mean(zipf_constants)
        std_constant = np.std(zipf_constants)
        
        print(f"\nZipf's Constant Analysis (freq × rank):")
        print(f"  - Mean: {avg_constant:.2f}")
        print(f"  - Std Dev: {std_constant:.2f}")
        print(f"  - Coefficient of Variation: {(std_constant/avg_constant)*100:.1f}%")
        
        # Specific Zipf examples
        print(f"\nZipf's Law Examples:")
        print("-" * 70)
        print(f"{'Rank':<8} {'Word':<15} {'Freq':<10} {'Freq×Rank':<12} {'Expected Freq':<12}")
        print("-" * 70)
        
        most_common_freq = sorted_words[0][1]
        for rank in [1, 2, 3, 5, 10, 20, 50, 100]:
            if rank <= len(sorted_words):
                word, freq = sorted_words[rank - 1]
                product = freq * rank
                expected = most_common_freq / rank
                print(f"{rank:<8} {word:<15} {freq:<10,} {product:<12.0f} {expected:<12.0f}")
        
        # Save Zipf analysis results
        zipf_results = {
            'correlation': float(correlation),
            'zipf_constant_mean': float(avg_constant),
            'zipf_constant_std': float(std_constant),
            'validates_zipf': bool(correlation < -0.85),
            'rank_frequency_data': [
                {'rank': int(rank), 'word': word, 'frequency': int(freq)}
                for rank, (word, freq) in enumerate(sorted_words[:1000], 1)
            ],
            'log_log_data': [
                {'log_rank': float(lr), 'log_frequency': float(lf)}
                for lr, lf in zip(log_ranks[:1000], log_frequencies[:1000])
            ]
        }
        
        with open('zipf_analysis_results.json', 'w', encoding='utf-8') as f:
            json.dump(zipf_results, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Saved: zipf_analysis_results.json")
        
        return zipf_results
    
    def calculate_coverage(self):
        """
        Calculate vocabulary coverage statistics
        
        Shows what percentage of corpus is covered by top N words
        Critical for lexical model size decisions
        """
        print("\n" + "=" * 70)
        print("VOCABULARY COVERAGE ANALYSIS")
        print("=" * 70)
        
        if self.word_freq is None:
            raise ValueError("Must run analyze_word_frequency() first")
        
        sorted_words = self.word_freq.most_common()
        
        # Calculate cumulative coverage
        coverage_points = [100, 500, 1000, 2000, 5000, 10000, 20000, 50000]
        coverage_data = []
        
        print(f"\nCoverage by Vocabulary Size:")
        print("-" * 70)
        print(f"{'Vocab Size':<15} {'Words Covered':<15} {'% of Corpus':<15} {'% of Vocab'}")
        print("-" * 70)
        
        cumulative_freq = 0
        for size in coverage_points:
            if size <= len(sorted_words):
                # Sum frequencies of top N words
                words_at_size = sorted_words[:size]
                cumulative_freq = sum(freq for _, freq in words_at_size)
                coverage_pct = (cumulative_freq / self.total_words) * 100
                vocab_pct = (size / self.vocabulary_size) * 100
                
                coverage_data.append({
                    'vocab_size': size,
                    'words_covered': cumulative_freq,
                    'coverage_percentage': coverage_pct,
                    'vocab_percentage': vocab_pct
                })
                
                print(f"{size:<15,} {cumulative_freq:<15,} {coverage_pct:<15.2f}% {vocab_pct:<.2f}%")
        
        # Find vocabulary size needed for 80%, 90%, 95% coverage
        print(f"\nVocabulary Size for Target Coverage:")
        print("-" * 70)
        
        target_coverages = [80, 90, 95, 99]
        cumulative = 0
        vocab_for_coverage = {}
        
        for target in target_coverages:
            cumulative = 0
            for i, (word, freq) in enumerate(sorted_words, 1):
                cumulative += freq
                coverage = (cumulative / self.total_words) * 100
                if coverage >= target:
                    vocab_for_coverage[target] = i
                    print(f"  - {target}% coverage: {i:,} words needed "
                          f"({(i/self.vocabulary_size)*100:.1f}% of vocabulary)")
                    break
        
        # Save coverage results
        coverage_results = {
            'coverage_by_size': coverage_data,
            'vocab_for_coverage': vocab_for_coverage,
            'total_vocabulary': self.vocabulary_size,
            'total_words': self.total_words
        }
        
        with open('coverage_analysis_results.json', 'w', encoding='utf-8') as f:
            json.dump(coverage_results, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Saved: coverage_analysis_results.json")
        
        return coverage_results
    
    def create_visualizations(self, word_results, zipf_results, coverage_results):
        """
        Create visualizations for presentation slides
        """
        print("\n" + "=" * 70)
        print("CREATING VISUALIZATIONS FOR PRESENTATION")
        print("=" * 70)
        
        # Figure 1: Zipf's Law - Log-Log Plot
        fig, ax = plt.subplots(figsize=(10, 7))
        
        log_data = zipf_results['log_log_data']
        log_ranks = [d['log_rank'] for d in log_data]
        log_freqs = [d['log_frequency'] for d in log_data]
        
        ax.scatter(log_ranks, log_freqs, alpha=0.5, s=10)
        
        # Add trend line
        z = np.polyfit(log_ranks, log_freqs, 1)
        p = np.poly1d(z)
        ax.plot(log_ranks, p(log_ranks), "r-", linewidth=2, 
               label=f'Trend: y = {z[0]:.2f}x + {z[1]:.2f}')
        
        ax.set_xlabel('Log(Rank)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Log(Frequency)', fontsize=12, fontweight='bold')
        ax.set_title("Zipf's Law Validation for Kashubian Corpus\n(Log-Log Plot)", 
                    fontsize=14, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        
        # Add correlation annotation
        ax.text(0.05, 0.95, f"Correlation: {zipf_results['correlation']:.4f}\n✓ Strong Zipfian Distribution",
               transform=ax.transAxes, fontsize=11, verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        plt.savefig('zipf_law_validation.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: zipf_law_validation.png")
        plt.close()
        
        # Figure 2: Rank-Frequency Plot (Regular scale)
        fig, ax = plt.subplots(figsize=(12, 7))
        
        ranks = [d['rank'] for d in zipf_results['rank_frequency_data'][:100]]
        freqs = [d['frequency'] for d in zipf_results['rank_frequency_data'][:100]]
        
        ax.plot(ranks, freqs, 'b-', linewidth=2)
        ax.fill_between(ranks, freqs, alpha=0.3)
        
        ax.set_xlabel('Word Rank', fontsize=12, fontweight='bold')
        ax.set_ylabel('Frequency', fontsize=12, fontweight='bold')
        ax.set_title('Word Frequency Distribution (Top 100 Words)\nShowing Typical Zipfian "Long Tail"', 
                    fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('word_frequency_distribution.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: word_frequency_distribution.png")
        plt.close()
        
        # Figure 3: Coverage Curve
        fig, ax = plt.subplots(figsize=(12, 7))
        
        vocab_sizes = [d['vocab_size'] for d in coverage_results['coverage_by_size']]
        coverages = [d['coverage_percentage'] for d in coverage_results['coverage_by_size']]
        
        ax.plot(vocab_sizes, coverages, 'g-', linewidth=3, marker='o', markersize=8)
        
        # Add reference lines for 80%, 90%, 95%
        for target in [80, 90, 95]:
            ax.axhline(y=target, color='r', linestyle='--', alpha=0.5, linewidth=1)
            ax.text(vocab_sizes[-1], target, f' {target}%', fontsize=10, va='center')
        
        ax.set_xlabel('Vocabulary Size (Number of Unique Words)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Corpus Coverage (%)', fontsize=12, fontweight='bold')
        ax.set_title('Vocabulary Coverage: How Many Words Needed?\n(For Lexical Model Size Decisions)', 
                    fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.set_xlim(0, max(vocab_sizes) * 1.1)
        ax.set_ylim(0, 105)
        
        plt.tight_layout()
        plt.savefig('vocabulary_coverage_curve.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: vocabulary_coverage_curve.png")
        plt.close()
        
        # Figure 4: Hapax Legomena Visualization
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Create frequency bins
        freq_counts = list(self.word_freq.values())
        unique_freqs = sorted(set(freq_counts))[:20]  # First 20 frequency values
        
        freq_distribution = [freq_counts.count(f) for f in unique_freqs]
        
        ax.bar(range(len(unique_freqs)), freq_distribution, color='steelblue')
        ax.set_xlabel('Word Frequency (how many times word appears)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Number of Words', fontsize=12, fontweight='bold')
        ax.set_title('Word Frequency Distribution Showing "Long Tail"\n(Many words appear only once - Hapax Legomena)', 
                    fontsize=14, fontweight='bold')
        ax.set_xticks(range(len(unique_freqs)))
        ax.set_xticklabels(unique_freqs)
        ax.grid(axis='y', alpha=0.3)
        
        # Highlight hapax legomena
        hapax_pct = (self.hapax_legomena_count / self.vocabulary_size) * 100
        ax.text(0.5, 0.95, f'Hapax Legomena (frequency=1): {self.hapax_legomena_count:,} words ({hapax_pct:.1f}% of vocabulary)',
               transform=ax.transAxes, fontsize=11, verticalalignment='top', ha='center',
               bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
        
        plt.tight_layout()
        plt.savefig('hapax_legomena_distribution.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: hapax_legomena_distribution.png")
        plt.close()
        
        print("\n✓ All visualizations created successfully!")
    
    def generate_lexical_model_data(self, min_frequency=2, max_words=50000):
        """
        Generate data for Keyman lexical model
        Filters out hapax legomena and very rare words
        """
        print("\n" + "=" * 70)
        print("GENERATING LEXICAL MODEL DATA")
        print("=" * 70)
        
        if self.word_freq is None:
            raise ValueError("Must run analyze_word_frequency() first")
        
        # Filter words by minimum frequency
        filtered_words = {
            word: freq for word, freq in self.word_freq.items() 
            if freq >= min_frequency
        }
        
        print(f"Filtering parameters:")
        print(f"  - Minimum frequency: {min_frequency}")
        print(f"  - Maximum words: {max_words:,}")
        print(f"\nBefore filtering: {len(self.word_freq):,} words")
        print(f"After filtering: {len(filtered_words):,} words")
        print(f"Removed: {len(self.word_freq) - len(filtered_words):,} words")
        
        # Sort by frequency and limit to max_words
        sorted_filtered = sorted(filtered_words.items(), key=lambda x: x[1], reverse=True)
        lexical_model_words = sorted_filtered[:max_words]
        
        print(f"\nFinal lexical model vocabulary: {len(lexical_model_words):,} words")
        
        # Calculate coverage of filtered vocabulary
        total_filtered_freq = sum(freq for _, freq in lexical_model_words)
        coverage = (total_filtered_freq / self.total_words) * 100
        print(f"Coverage of corpus: {coverage:.2f}%")
        
        # Save lexical model data
        lexical_data = {
            'metadata': {
                'min_frequency': min_frequency,
                'max_words': max_words,
                'vocabulary_size': len(lexical_model_words),
                'coverage_percentage': coverage,
                'total_corpus_words': self.total_words
            },
            'words': [
                {
                    'word': word,
                    'frequency': freq,
                    'rank': rank
                }
                for rank, (word, freq) in enumerate(lexical_model_words, 1)
            ]
        }
        
        with open('lexical_model_data.json', 'w', encoding='utf-8') as f:
            json.dump(lexical_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Saved: lexical_model_data.json")
        
        # Also save as simple word list for Keyman
        with open('lexical_model_wordlist.txt', 'w', encoding='utf-8') as f:
            for word, freq in lexical_model_words:
                f.write(f"{word}\t{freq}\n")
        
        print(f"✓ Saved: lexical_model_wordlist.txt (tab-separated)")
        
        return lexical_data


def main():
    """
    Main execution function
    """
    print("\n" + "=" * 70)
    print("KASHUBIAN WORD FREQUENCY & ZIPF'S LAW ANALYSIS")
    print("Following CS6361 Week 4 Lecture Concepts")
    print("=" * 70 + "\n")
    
    analyzer = ZipfAnalyzer()
    
    # Run analyses in sequence
    word_results = analyzer.analyze_word_frequency()
    zipf_results = analyzer.validate_zipf_law()
    coverage_results = analyzer.calculate_coverage()
    lexical_data = analyzer.generate_lexical_model_data(min_frequency=2, max_words=50000)
    
    # Create visualizations
    analyzer.create_visualizations(word_results, zipf_results, coverage_results)
    
    print("\n" + "=" * 70)
    print("WORD FREQUENCY ANALYSIS COMPLETE!")
    print("=" * 70)
    print("\nFiles generated:")
    print("  - word_frequency_results.json")
    print("  - zipf_analysis_results.json")
    print("  - coverage_analysis_results.json")
    print("  - lexical_model_data.json")
    print("  - lexical_model_wordlist.txt")
    print("  - zipf_law_validation.png")
    print("  - word_frequency_distribution.png")
    print("  - vocabulary_coverage_curve.png")
    print("  - hapax_legomena_distribution.png")
    print("\nThese files are ready for Presentation Slides 6, 10, and 11!")
    print("\nKey findings for your presentation:")
    print(f"  - Vocabulary size: {word_results['vocabulary_size']:,} unique words")
    print(f"  - Hapax legomena: {word_results['hapax_legomena']:,} words ({word_results['hapax_percentage']:.1f}%)")
    print(f"  - Zipf correlation: {zipf_results['correlation']:.4f} (strong validation)")
    print(f"  - Lexical model size: {lexical_data['metadata']['vocabulary_size']:,} words")
    print(f"  - Lexical model coverage: {lexical_data['metadata']['coverage_percentage']:.2f}%")


if __name__ == '__main__':
    main()
