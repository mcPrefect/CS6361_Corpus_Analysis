#!/usr/bin/env python3
"""
Kashubian Character Frequency Analysis
For Presentation Slides 5 & 8

This script analyzes character-level frequencies in the preprocessed corpus,
identifying the most common characters and Kashubian-specific diacritics.

Critical for keyboard design decisions.
"""

import json
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

class CharacterFrequencyAnalyzer:
    """
    Analyze character frequencies in Kashubian corpus
    """
    
    def __init__(self):
        # Kashubian-specific diacritics
        self.kashubian_diacritics = {
            'ą': 'a with ogonek',
            'ã': 'a with tilde', 
            'é': 'e with acute',
            'ë': 'e with diaeresis',
            'ń': 'n with acute',
            'ò': 'o with grave',
            'ó': 'o with acute',
            'ô': 'o with circumflex',
            'ù': 'u with grave',
            'ł': 'l with stroke',
            'ż': 'z with dot above'
        }
        
        # Important digraphs
        self.digraphs = ['ch', 'cz', 'dz', 'dż', 'rz', 'sz']
    
    def analyze_character_frequency(self, character_file='characters_preprocessed.txt'):
        """
        Analyze individual character frequencies
        """
        print("=" * 60)
        print("CHARACTER FREQUENCY ANALYSIS")
        print("=" * 60)
        
        # Load preprocessed characters
        with open(character_file, 'r', encoding='utf-8') as f:
            text = f.read()
        
        total_chars = len(text)
        print(f"Total characters in corpus: {total_chars:,}\n")
        
        # Count character frequencies
        char_freq = Counter(text)
        
        # Calculate percentages
        char_percentages = {
            char: (count / total_chars) * 100 
            for char, count in char_freq.items()
        }
        
        # Sort by frequency
        sorted_chars = sorted(char_percentages.items(), 
                            key=lambda x: x[1], reverse=True)
        
        # Display top characters
        print("TOP 20 CHARACTERS (by frequency):")
        print("-" * 60)
        print(f"{'Rank':<6} {'Char':<8} {'Frequency':<12} {'Percentage':<12} {'Description'}")
        print("-" * 60)
        
        for rank, (char, percentage) in enumerate(sorted_chars[:20], 1):
            count = char_freq[char]
            if char == ' ':
                description = 'SPACE'
            elif char in self.kashubian_diacritics:
                description = f'★ {self.kashubian_diacritics[char]}'
            else:
                description = 'standard letter'
            
            print(f"{rank:<6} {repr(char):<8} {count:<12,} {percentage:<12.4f}% {description}")
        
        # Highlight Kashubian-specific diacritics
        print("\n" + "=" * 60)
        print("KASHUBIAN-SPECIFIC DIACRITICS (Critical for keyboard design)")
        print("=" * 60)
        
        diacritic_data = []
        for char, description in self.kashubian_diacritics.items():
            if char in char_freq:
                count = char_freq[char]
                percentage = char_percentages[char]
                rank = [c for c, _ in sorted_chars].index(char) + 1
                diacritic_data.append({
                    'char': char,
                    'description': description,
                    'count': count,
                    'percentage': percentage,
                    'rank': rank
                })
        
        # Sort diacritics by frequency
        diacritic_data.sort(key=lambda x: x['percentage'], reverse=True)
        
        print(f"{'Char':<6} {'Description':<20} {'Count':<12} {'Percentage':<12} {'Rank'}")
        print("-" * 70)
        for data in diacritic_data:
            print(f"{data['char']:<6} {data['description']:<20} {data['count']:<12,} "
                  f"{data['percentage']:<12.4f}% #{data['rank']}")
        
        # Save results
        results = {
            'total_characters': total_chars,
            'top_20_characters': [
                {
                    'char': char,
                    'count': char_freq[char],
                    'percentage': percentage,
                    'rank': rank
                }
                for rank, (char, percentage) in enumerate(sorted_chars[:20], 1)
            ],
            'kashubian_diacritics': diacritic_data
        }
        
        with open('character_frequency_results.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Saved: character_frequency_results.json")
        
        return results
    
    def analyze_digraph_frequency(self, character_file='characters_preprocessed.txt'):
        """
        Analyze digraph (two-character combination) frequencies
        Important for understanding character sequences and keyboard ergonomics
        """
        print("\n" + "=" * 60)
        print("DIGRAPH FREQUENCY ANALYSIS")
        print("=" * 60)
        
        # Load preprocessed characters
        with open(character_file, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Extract all digraphs
        digraph_counts = Counter()
        for i in range(len(text) - 1):
            digraph = text[i:i+2]
            if digraph[0] != ' ' and digraph[1] != ' ':  # Skip space-containing digraphs
                digraph_counts[digraph] += 1
        
        total_digraphs = sum(digraph_counts.values())
        
        # Calculate percentages for important digraphs
        print("\nIMPORTANT KASHUBIAN DIGRAPHS:")
        print("-" * 60)
        print(f"{'Digraph':<10} {'Count':<12} {'Percentage':<12} {'Status'}")
        print("-" * 60)
        
        important_digraphs = []
        for digraph in self.digraphs:
            count = digraph_counts[digraph]
            percentage = (count / total_digraphs) * 100
            important_digraphs.append({
                'digraph': digraph,
                'count': count,
                'percentage': percentage
            })
            print(f"{digraph:<10} {count:<12,} {percentage:<12.4f}% ★ Phonemic digraph")
        
        # Top 20 most frequent digraphs overall
        print("\nTOP 20 MOST FREQUENT DIGRAPHS (all):")
        print("-" * 60)
        print(f"{'Rank':<6} {'Digraph':<10} {'Count':<12} {'Percentage'}")
        print("-" * 60)
        
        top_digraphs = []
        for rank, (digraph, count) in enumerate(digraph_counts.most_common(20), 1):
            percentage = (count / total_digraphs) * 100
            marker = '★' if digraph in self.digraphs else ''
            top_digraphs.append({
                'rank': rank,
                'digraph': digraph,
                'count': count,
                'percentage': percentage
            })
            print(f"{rank:<6} {digraph:<10} {count:<12,} {percentage:<12.4f}% {marker}")
        
        # Save results
        results = {
            'total_digraphs': total_digraphs,
            'important_kashubian_digraphs': important_digraphs,
            'top_20_digraphs': top_digraphs
        }
        
        with open('digraph_frequency_results.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Saved: digraph_frequency_results.json")
        
        return results
    
    def analyze_trigraphs(self, character_file='characters_preprocessed.txt'):
        """
        Analyze trigraph (three-character combination) frequencies
        Following N-gram concepts from Week 4 lectures
        """
        print("\n" + "=" * 60)
        print("TRIGRAPH FREQUENCY ANALYSIS (N-gram Analysis)")
        print("=" * 60)
        
        # Load preprocessed characters
        with open(character_file, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Extract all trigraphs
        trigraph_counts = Counter()
        for i in range(len(text) - 2):
            trigraph = text[i:i+3]
            # Skip if contains spaces
            if ' ' not in trigraph:
                trigraph_counts[trigraph] += 1
        
        total_trigraphs = sum(trigraph_counts.values())
        
        # Top 20 most frequent trigraphs
        print("\nTOP 20 MOST FREQUENT TRIGRAPHS:")
        print("-" * 60)
        print(f"{'Rank':<6} {'Trigraph':<12} {'Count':<12} {'Percentage'}")
        print("-" * 60)
        
        top_trigraphs = []
        for rank, (trigraph, count) in enumerate(trigraph_counts.most_common(20), 1):
            percentage = (count / total_trigraphs) * 100
            top_trigraphs.append({
                'rank': rank,
                'trigraph': trigraph,
                'count': count,
                'percentage': percentage
            })
            print(f"{rank:<6} {trigraph:<12} {count:<12,} {percentage:<12.4f}%")
        
        # Save results
        results = {
            'total_trigraphs': total_trigraphs,
            'top_20_trigraphs': top_trigraphs
        }
        
        with open('trigraph_frequency_results.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Saved: trigraph_frequency_results.json")
        
        return results
    
    def create_visualizations(self, char_results, digraph_results):
        """
        Create visualizations for presentation slides
        """
        print("\n" + "=" * 60)
        print("CREATING VISUALIZATIONS FOR PRESENTATION")
        print("=" * 60)
        
        # Figure 1: Top 20 Character Frequencies
        fig, ax = plt.subplots(figsize=(12, 6))
        
        chars = [item['char'] if item['char'] != ' ' else 'SPACE' 
                for item in char_results['top_20_characters']]
        percentages = [item['percentage'] for item in char_results['top_20_characters']]
        
        # Color Kashubian diacritics differently
        kashubian_chars = set(self.kashubian_diacritics.keys())
        colors = ['#d62728' if (item['char'] in kashubian_chars) else '#1f77b4' 
                 for item in char_results['top_20_characters']]
        
        bars = ax.bar(range(len(chars)), percentages, color=colors)
        ax.set_xlabel('Character', fontsize=12, fontweight='bold')
        ax.set_ylabel('Frequency (%)', fontsize=12, fontweight='bold')
        ax.set_title('Top 20 Character Frequencies in Kashubian Corpus\n(Red = Kashubian-specific diacritics)', 
                    fontsize=14, fontweight='bold')
        ax.set_xticks(range(len(chars)))
        ax.set_xticklabels(chars, fontsize=10)
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('character_frequency_chart.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: character_frequency_chart.png")
        plt.close()
        
        # Figure 2: Kashubian Diacritics Only
        fig, ax = plt.subplots(figsize=(10, 6))
        
        diacritic_data = char_results['kashubian_diacritics']
        chars = [item['char'] for item in diacritic_data]
        percentages = [item['percentage'] for item in diacritic_data]
        
        bars = ax.bar(range(len(chars)), percentages, color='#d62728')
        ax.set_xlabel('Kashubian Diacritic', fontsize=12, fontweight='bold')
        ax.set_ylabel('Frequency (%)', fontsize=12, fontweight='bold')
        ax.set_title('Kashubian-Specific Diacritic Frequencies\n(Critical for Keyboard Design)', 
                    fontsize=14, fontweight='bold')
        ax.set_xticks(range(len(chars)))
        ax.set_xticklabels(chars, fontsize=14)
        ax.grid(axis='y', alpha=0.3)
        
        # Add percentage labels on bars
        for i, (bar, pct) in enumerate(zip(bars, percentages)):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{pct:.2f}%',
                   ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('kashubian_diacritics_frequency.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: kashubian_diacritics_frequency.png")
        plt.close()
        
        # Figure 3: Important Digraphs
        fig, ax = plt.subplots(figsize=(10, 6))
        
        digraphs = [item['digraph'] for item in digraph_results['important_kashubian_digraphs']]
        percentages = [item['percentage'] for item in digraph_results['important_kashubian_digraphs']]
        
        bars = ax.bar(range(len(digraphs)), percentages, color='#2ca02c')
        ax.set_xlabel('Digraph', fontsize=12, fontweight='bold')
        ax.set_ylabel('Frequency (%)', fontsize=12, fontweight='bold')
        ax.set_title('Kashubian Phonemic Digraph Frequencies', 
                    fontsize=14, fontweight='bold')
        ax.set_xticks(range(len(digraphs)))
        ax.set_xticklabels(digraphs, fontsize=12, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        # Add percentage labels
        for bar, pct in zip(bars, percentages):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{pct:.2f}%',
                   ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('digraph_frequency_chart.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: digraph_frequency_chart.png")
        plt.close()
        
        print("\n✓ All visualizations created successfully!")
    
    def generate_latex_table(self, char_results):
        """
        Generate LaTeX table for presentation slides
        """
        print("\n" + "=" * 60)
        print("GENERATING LATEX TABLE")
        print("=" * 60)
        
        latex_code = r"""
\begin{table}[h]
\centering
\caption{Top 20 Character Frequencies in Kashubian Corpus}
\begin{tabular}{|c|c|c|c|l|}
\hline
\textbf{Rank} & \textbf{Character} & \textbf{Count} & \textbf{Percentage} & \textbf{Description} \\
\hline
"""
        
        for item in char_results['top_20_characters']:
            char_display = 'SPACE' if item['char'] == ' ' else item['char']
            desc = 'Kashubian diacritic' if item['char'] in self.kashubian_diacritics else 'Standard'
            latex_code += f"{item['rank']} & {char_display} & {item['count']:,} & {item['percentage']:.2f}\\% & {desc} \\\\\n\\hline\n"
        
        latex_code += r"""
\end{tabular}
\end{table}
"""
        
        with open('character_frequency_table.tex', 'w', encoding='utf-8') as f:
            f.write(latex_code)
        
        print("✓ Saved: character_frequency_table.tex")


def main():
    """
    Main execution function
    """
    analyzer = CharacterFrequencyAnalyzer()
    
    # Run analyses
    char_results = analyzer.analyze_character_frequency()
    digraph_results = analyzer.analyze_digraph_frequency()
    trigraph_results = analyzer.analyze_trigraphs()
    
    # Create visualizations
    analyzer.create_visualizations(char_results, digraph_results)
    
    # Generate LaTeX table
    analyzer.generate_latex_table(char_results)
    
    print("\n" + "=" * 60)
    print("CHARACTER FREQUENCY ANALYSIS COMPLETE!")
    print("=" * 60)
    print("\nFiles generated:")
    print("  - character_frequency_results.json")
    print("  - digraph_frequency_results.json")
    print("  - trigraph_frequency_results.json")
    print("  - character_frequency_chart.png")
    print("  - kashubian_diacritics_frequency.png")
    print("  - digraph_frequency_chart.png")
    print("  - character_frequency_table.tex")
    print("\nThese files are ready for Presentation Slides 5, 6, and 8!")


if __name__ == '__main__':
    main()
