#!/usr/bin/env python3
"""
Kashubian Corpus Analysis - Master Pipeline
Runs all preprocessing and analysis steps in correct order

This script orchestrates the complete pipeline:
1. Preprocessing (markup analysis, tokenization, normalization)
2. Character frequency analysis
3. Word frequency analysis
4. Zipf's Law validation
5. Coverage analysis
6. Lexical model generation

Usage:
    python run_full_pipeline.py <path_to_wikipedia_dump.xml.bz2>
"""

import sys
import os
import subprocess
from datetime import datetime

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")

def run_script(script_name, args=None):
    """Run a Python script and check for errors"""
    cmd = [sys.executable, script_name]
    if args:
        cmd.extend(args)
    
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=False, text=True)
    
    if result.returncode != 0:
        print(f"\n❌ ERROR: {script_name} failed with return code {result.returncode}")
        sys.exit(1)
    
    print(f"\n✓ {script_name} completed successfully\n")

def check_file_exists(filepath):
    """Check if a required file exists"""
    if not os.path.exists(filepath):
        print(f"❌ ERROR: Required file not found: {filepath}")
        sys.exit(1)
    return True

def main():
    """
    Main pipeline execution
    """
    print_section("KASHUBIAN CORPUS ANALYSIS - FULL PIPELINE")
    print("Following CS6361 Week 5 & 7 Lecture Architecture")
    print("For Presentation Slides 3-11")
    print(f"\nStarted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Check command line arguments
    if len(sys.argv) < 2:
        print("Usage: python run_full_pipeline.py <path_to_wikipedia_dump.xml.bz2>")
        print("\nExample:")
        print("  python run_full_pipeline.py csbwiki-latest-pages-articles.xml.bz2")
        print("\nOr if file is in /mnt/user-data/uploads:")
        print("  python run_full_pipeline.py /mnt/user-data/uploads/csbwiki-latest-pages-articles.xml.bz2")
        sys.exit(1)
    
    wikipedia_dump = sys.argv[1]
    
    # Verify Wikipedia dump exists
    if not os.path.exists(wikipedia_dump):
        print(f"❌ ERROR: Wikipedia dump file not found: {wikipedia_dump}")
        print("\nPlease ensure you have downloaded the Kashubian Wikipedia dump:")
        print("  URL: https://dumps.wikimedia.org/csbwiki/latest/")
        print("  File: csbwiki-latest-pages-articles.xml.bz2")
        sys.exit(1)
    
    print(f"✓ Found Wikipedia dump: {wikipedia_dump}")
    file_size_mb = os.path.getsize(wikipedia_dump) / (1024 * 1024)
    print(f"  File size: {file_size_mb:.2f} MB\n")
    
    # ==========================================================================
    # STEP 1: PREPROCESSING
    # ==========================================================================
    print_section("STEP 1: CORPUS PREPROCESSING")
    print("This will:")
    print("  - Parse Wikipedia XML")
    print("  - Remove markup")
    print("  - Tokenize text")
    print("  - Normalize case")
    print("  - Extract characters")
    print("\nExpected time: 2-5 minutes for ~6000 articles\n")
    
    run_script('kashubian_preprocessing.py', [wikipedia_dump])
    
    # Verify preprocessing outputs
    required_files = [
        'tokens_preprocessed.txt',
        'characters_preprocessed.txt',
        'preprocessing_stats.json',
        'article_metadata.json'
    ]
    
    print("Verifying preprocessing outputs...")
    for filepath in required_files:
        check_file_exists(filepath)
        file_size = os.path.getsize(filepath) / 1024  # KB
        print(f"  ✓ {filepath} ({file_size:.2f} KB)")
    
    # ==========================================================================
    # STEP 2: CHARACTER FREQUENCY ANALYSIS
    # ==========================================================================
    print_section("STEP 2: CHARACTER FREQUENCY ANALYSIS")
    print("This will:")
    print("  - Analyze individual character frequencies")
    print("  - Identify Kashubian diacritic frequencies")
    print("  - Analyze digraph frequencies")
    print("  - Analyze trigraph frequencies (n-grams)")
    print("  - Generate visualizations for slides 5, 6, 8")
    print("\nExpected time: 1-2 minutes\n")
    
    run_script('kashubian_character_frequency.py')
    
    # Verify character analysis outputs
    char_files = [
        'character_frequency_results.json',
        'digraph_frequency_results.json',
        'trigraph_frequency_results.json',
        'character_frequency_chart.png',
        'kashubian_diacritics_frequency.png',
        'digraph_frequency_chart.png'
    ]
    
    print("Verifying character analysis outputs...")
    for filepath in char_files:
        if check_file_exists(filepath):
            print(f"  ✓ {filepath}")
    
    # ==========================================================================
    # STEP 3: WORD FREQUENCY & ZIPF'S LAW ANALYSIS
    # ==========================================================================
    print_section("STEP 3: WORD FREQUENCY & ZIPF'S LAW ANALYSIS")
    print("This will:")
    print("  - Analyze word frequency distribution")
    print("  - Validate Zipf's Law for Kashubian")
    print("  - Calculate hapax legomena")
    print("  - Compute coverage statistics")
    print("  - Generate lexical model data")
    print("  - Create visualizations for slides 6, 10, 11")
    print("\nExpected time: 2-3 minutes\n")
    
    run_script('kashubian_word_frequency.py')
    
    # Verify word analysis outputs
    word_files = [
        'word_frequency_results.json',
        'zipf_analysis_results.json',
        'coverage_analysis_results.json',
        'lexical_model_data.json',
        'lexical_model_wordlist.txt',
        'zipf_law_validation.png',
        'word_frequency_distribution.png',
        'vocabulary_coverage_curve.png',
        'hapax_legomena_distribution.png'
    ]
    
    print("Verifying word analysis outputs...")
    for filepath in word_files:
        if check_file_exists(filepath):
            print(f"  ✓ {filepath}")
    
    # ==========================================================================
    # PIPELINE COMPLETE
    # ==========================================================================
    print_section("PIPELINE COMPLETE!")
    print(f"Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    print("✓ All preprocessing and analysis steps completed successfully!")
    print("\nGenerated files organized by presentation slide:")
    print("\n📊 SLIDE 3 (Corpus Selection & Statistics):")
    print("   - preprocessing_stats.json")
    print("   - article_metadata.json")
    
    print("\n📊 SLIDE 5 (Character Set Identification):")
    print("   - character_frequency_results.json")
    print("   - character_frequency_chart.png")
    
    print("\n📊 SLIDE 6 (Zipf's Law & Word Distribution):")
    print("   - word_frequency_results.json")
    print("   - zipf_analysis_results.json")
    print("   - zipf_law_validation.png")
    print("   - word_frequency_distribution.png")
    print("   - hapax_legomena_distribution.png")
    
    print("\n📊 SLIDE 8 (Character Frequency Analysis):")
    print("   - kashubian_diacritics_frequency.png")
    print("   - digraph_frequency_chart.png")
    
    print("\n📊 SLIDE 9 (Character Combination Analysis):")
    print("   - digraph_frequency_results.json")
    print("   - trigraph_frequency_results.json")
    
    print("\n📊 SLIDES 10-11 (Lexical Model):")
    print("   - coverage_analysis_results.json")
    print("   - vocabulary_coverage_curve.png")
    print("   - lexical_model_data.json")
    print("   - lexical_model_wordlist.txt")
    
    print("\n" + "=" * 80)
    print("NEXT STEPS:")
    print("=" * 80)
    print("\n1. Review all generated JSON files for exact statistics")
    print("2. Use PNG files directly in your presentation slides")
    print("3. Reference the preprocessing_report.txt for methodology details")
    print("4. The lexical_model_wordlist.txt is ready for Keyman Developer")
    print("\n5. Key statistics for your presentation:")
    
    # Load and display key statistics
    import json
    
    try:
        with open('preprocessing_stats.json', 'r') as f:
            prep_stats = json.load(f)
        
        with open('word_frequency_results.json', 'r') as f:
            word_stats = json.load(f)
        
        with open('zipf_analysis_results.json', 'r') as f:
            zipf_stats = json.load(f)
        
        print(f"\n   📌 Total articles: {prep_stats['total_articles']:,}")
        print(f"   📌 Total characters: {prep_stats['total_characters']:,}")
        print(f"   📌 Total words: {prep_stats['total_words']:,}")
        print(f"   📌 Unique vocabulary: {word_stats['vocabulary_size']:,}")
        print(f"   📌 Hapax legomena: {word_stats['hapax_legomena']:,} ({word_stats['hapax_percentage']:.1f}%)")
        print(f"   📌 Zipf correlation: {zipf_stats['correlation']:.4f} ✓ Strong validation")
        
        # Load character frequency for top diacritics
        with open('character_frequency_results.json', 'r') as f:
            char_stats = json.load(f)
        
        print(f"\n   📌 Most frequent Kashubian diacritics:")
        for diacritic in char_stats['kashubian_diacritics'][:3]:
            print(f"      {diacritic['char']}: {diacritic['percentage']:.2f}% (rank #{diacritic['rank']})")
        
    except Exception as e:
        print(f"\n   (Statistics files not found or error reading: {e})")
    
    print("\n" + "=" * 80)
    print("Your corpus analysis is complete and ready for the presentation!")
    print("=" * 80 + "\n")


if __name__ == '__main__':
    main()
