#!/usr/bin/env python3
"""
Kashubian Corpus Preprocessing Pipeline
Following CS6361 Week 5 & 7 Lecture Architecture

This script implements the text pre-processing steps covered in lectures:
1. Markup Analysis (XML parsing)
2. Tokenization (with diacritic handling)
3. Case normalization
4. Punctuation handling
5. Stopword decisions
6. Term recognition (multi-word expressions)

Input: csbwiki-latest-pages-articles.xml.bz2 (Wikipedia dump)
Output: Cleaned, tokenized corpus ready for frequency analysis
"""

import re
import bz2
import json
from xml.etree import ElementTree as ET
from collections import Counter, defaultdict
import unicodedata

class KashubianPreprocessor:
    """
    Comprehensive preprocessing for Kashubian Wikipedia corpus
    """
    
    def __init__(self):
        # Kashubian alphabet - 34 letters including diacritics
        self.kashubian_letters = set('aąãbcćdeęéëfghijklłmnńoòóôprsśtuùvwyzźż')
        self.kashubian_letters_upper = set('AĄÃBCĆDEĘÉËFGHIJKLŁMNŃOÒÓÔPRSŚTUÙVWYZŹŻ')
        
        # Important Kashubian digraphs (two-letter combinations representing single phonemes)
        self.digraphs = ['ch', 'cz', 'dz', 'dż', 'rz', 'sz']
        
        # Common Kashubian stopwords (function words with little semantic content)
        # Based on West Slavic language patterns, similar to Polish
        self.stopwords = set([
            'w', 'i', 'na', 'z', 'do', 'o', 'a', 'je', 'to', 'że', 'się',
            'ale', 'jak', 'co', 'ten', 'być', 'przez', 'dla', 'są', 'był',
            'jako', 'oraz', 'jego', 'jej', 'nich', 'też', 'tylko', 'już'
        ])
        
        # Statistics tracking
        self.stats = {
            'total_articles': 0,
            'total_characters': 0,
            'total_words': 0,
            'xml_elements_processed': 0,
            'markup_removed_chars': 0
        }
    
    def markup_analysis(self, xml_file_path):
        """
        Step 1: Markup Analysis
        Extract text from Wikipedia XML dump, removing all markup
        
        Following Week 5 lecture: "Taking a document marked up and extracting 
        the text and markup in a form suitable for further processing"
        """
        print("=" * 60)
        print("STEP 1: MARKUP ANALYSIS")
        print("=" * 60)
        
        articles = []
        
        # Use iterparse for memory-efficient processing of large XML files
        # This is crucial for the compressed Wikipedia dump
        with bz2.open(xml_file_path, 'rt', encoding='utf-8') as f:
            context = ET.iterparse(f, events=('start', 'end'))
            context = iter(context)
            
            current_title = None
            current_text = None
            in_page = False
            
            for event, elem in context:
                # Track namespace for proper XML handling
                tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
                
                if event == 'start' and tag == 'page':
                    in_page = True
                    current_title = None
                    current_text = None
                    self.stats['xml_elements_processed'] += 1
                
                elif event == 'end' and in_page:
                    if tag == 'title':
                        current_title = elem.text
                    
                    elif tag == 'text':
                        # Extract only article text, excluding:
                        # - Talk pages
                        # - User pages
                        # - Wikipedia meta pages
                        if current_title and elem.text:
                            if not any(prefix in current_title.lower() for prefix in 
                                     ['wikipedia:', 'talk:', 'user:', 'file:', 'template:']):
                                current_text = elem.text
                    
                    elif tag == 'page':
                        if current_title and current_text:
                            # Remove Wikipedia-specific markup
                            cleaned_text = self._remove_wiki_markup(current_text)
                            
                            if cleaned_text.strip():
                                articles.append({
                                    'title': current_title,
                                    'text': cleaned_text
                                })
                                self.stats['total_articles'] += 1
                        
                        # Clear element to save memory
                        elem.clear()
                        in_page = False
                        
                        # Progress indicator
                        if self.stats['total_articles'] % 100 == 0:
                            print(f"Processed {self.stats['total_articles']} articles...", end='\r')
        
        print(f"\nMarkup analysis complete: {self.stats['total_articles']} articles extracted")
        return articles
    
    def _remove_wiki_markup(self, text):
        """
        Remove Wikipedia-specific markup patterns
        Including: templates, references, categories, etc.
        """
        original_length = len(text)
        
        # Remove templates: {{template}}
        text = re.sub(r'\{\{[^}]*\}\}', '', text)
        
        # Remove references: <ref>...</ref> or <ref name="..." />
        text = re.sub(r'<ref[^>]*>[^<]*</ref>', '', text)
        text = re.sub(r'<ref[^>]*\/>', '', text)
        
        # Remove file/image links: [[File:...]] or [[Image:...]]
        text = re.sub(r'\[\[(File|Image|Òbrôzk):[^\]]*\]\]', '', text, flags=re.IGNORECASE)
        
        # Remove category tags: [[Category:...]]
        text = re.sub(r'\[\[Kategòrëjô:[^\]]*\]\]', '', text)
        
        # Remove internal link markup but keep text: [[link|text]] -> text
        text = re.sub(r'\[\[[^\]]*\|([^\]]+)\]\]', r'\1', text)
        text = re.sub(r'\[\[([^\]]+)\]\]', r'\1', text)
        
        # Remove external links: [http://... text]
        text = re.sub(r'\[http[^\]]*\]', '', text)
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Remove wiki formatting: ''italic'' and '''bold'''
        text = re.sub(r"'''([^']+)'''", r'\1', text)
        text = re.sub(r"''([^']+)''", r'\1', text)
        
        # Remove section markers: == Section ==
        text = re.sub(r'={2,}[^=]+={2,}', '', text)
        
        self.stats['markup_removed_chars'] += (original_length - len(text))
        
        return text
    
    def tokenize(self, text):
        """
        Step 2: Tokenization
        Split text into words, handling Kashubian diacritics properly
        
        Following Week 5 lecture: "The process of splitting up a text (seen as a 
        stream of characters) into a stream of words"
        
        Challenge: Must recognize Kashubian characters (ą, ã, é, ë, etc.) as 
        valid in-word characters
        """
        # Build regex pattern that includes all Kashubian letters
        # This ensures diacritics are treated as word characters, not punctuation
        kashubian_word_pattern = r'[' + ''.join(self.kashubian_letters | self.kashubian_letters_upper) + r']+'
        
        # Find all words (sequences of Kashubian letters)
        tokens = re.findall(kashubian_word_pattern, text)
        
        return tokens
    
    def normalize_case(self, tokens):
        """
        Step 3: Case Normalization
        Convert all tokens to lowercase for frequency counting
        
        Following Week 5 lecture: "Lowercasing" as a standard preprocessing step
        
        This ensures 'Kaszëbë' and 'kaszëbë' are counted as the same word
        """
        return [token.lower() for token in tokens]
    
    def remove_punctuation_tokens(self, tokens):
        """
        Step 4: Remove Pure Punctuation Tokens
        Filter out any tokens that are only punctuation
        
        Following Week 5 lecture: "Removing punctuation/extra spaces"
        """
        # Keep only tokens that contain at least one letter
        return [token for token in tokens if any(c.isalpha() for c in token)]
    
    def handle_stopwords(self, tokens, remove=False):
        """
        Step 5: Stopword Handling
        
        Following Week 5 lecture: "Stopwords have little or no significance"
        
        For this project, we KEEP stopwords because:
        1. They're essential for character frequency analysis
        2. They're critical for lexical model predictions
        3. They represent natural language usage patterns
        
        However, we provide the option to remove them if needed for other analyses
        """
        if remove:
            return [token for token in tokens if token not in self.stopwords]
        return tokens
    
    def identify_multiword_terms(self, text):
        """
        Step 6: Term Recognition (Optional)
        Identify multi-word expressions that should be treated as single units
        
        Following Week 5 lecture: "Term recogniser scans the text looking for 
        such terms and grouping each one into a single token"
        
        Examples for Kashubian:
        - Geographic names: Nová Wies, Òstrzë Seã
        - Compound terms specific to the language
        """
        # Common Kashubian multi-word terms (can be expanded)
        multiword_patterns = [
            r'Repùblika Polska',  # Republic of Poland
            r'kaszëbsczi jãzëk',  # Kashubian language
        ]
        
        terms_found = []
        for pattern in multiword_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            terms_found.extend(matches)
        
        return terms_found
    
    def preprocess_corpus(self, xml_file_path, output_dir='.'):
        """
        Complete preprocessing pipeline
        Implements the full architecture from Week 5 lecture
        """
        print("\n" + "=" * 60)
        print("KASHUBIAN CORPUS PREPROCESSING PIPELINE")
        print("Following CS6361 Week 5 & 7 Lecture Architecture")
        print("=" * 60 + "\n")
        
        # Step 1: Markup Analysis
        articles = self.markup_analysis(xml_file_path)
        
        # Combine all article text
        full_corpus_text = ' '.join([article['text'] for article in articles])
        
        print("\n" + "=" * 60)
        print("STEP 2-5: TOKENIZATION AND NORMALIZATION")
        print("=" * 60)
        
        all_tokens = []
        all_tokens_with_case = []
        character_sequence = []
        
        for article in articles:
            # Step 2: Tokenization
            tokens = self.tokenize(article['text'])
            all_tokens_with_case.extend(tokens)
            
            # Step 3: Case normalization
            tokens_normalized = self.normalize_case(tokens)
            
            # Step 4: Remove punctuation-only tokens
            tokens_clean = self.remove_punctuation_tokens(tokens_normalized)
            
            # Step 5: Stopword handling (we keep them)
            tokens_final = self.handle_stopwords(tokens_clean, remove=False)
            
            all_tokens.extend(tokens_final)
            
            # Extract all characters for character-level analysis
            for char in article['text']:
                if char.lower() in self.kashubian_letters or char == ' ':
                    character_sequence.append(char.lower())
        
        # Update statistics
        self.stats['total_words'] = len(all_tokens)
        self.stats['total_characters'] = len(character_sequence)
        
        print(f"Tokenization complete:")
        print(f"  - Total tokens: {len(all_tokens):,}")
        print(f"  - Total characters: {len(character_sequence):,}")
        
        # Save preprocessed data
        print("\n" + "=" * 60)
        print("SAVING PREPROCESSED DATA")
        print("=" * 60)
        
        # Save full token list
        with open(f'{output_dir}/tokens_preprocessed.txt', 'w', encoding='utf-8') as f:
            for token in all_tokens:
                f.write(token + '\n')
        print(f"✓ Saved: tokens_preprocessed.txt ({len(all_tokens):,} tokens)")
        
        # Save character sequence
        with open(f'{output_dir}/characters_preprocessed.txt', 'w', encoding='utf-8') as f:
            f.write(''.join(character_sequence))
        print(f"✓ Saved: characters_preprocessed.txt ({len(character_sequence):,} characters)")
        
        # Save preprocessing statistics
        with open(f'{output_dir}/preprocessing_stats.json', 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, indent=2, ensure_ascii=False)
        print(f"✓ Saved: preprocessing_stats.json")
        
        # Save article metadata
        article_metadata = [{
            'title': article['title'],
            'word_count': len(self.tokenize(article['text'])),
            'char_count': len(article['text'])
        } for article in articles]
        
        with open(f'{output_dir}/article_metadata.json', 'w', encoding='utf-8') as f:
            json.dump(article_metadata, f, indent=2, ensure_ascii=False)
        print(f"✓ Saved: article_metadata.json ({len(articles)} articles)")
        
        # Generate preprocessing report
        self._generate_report(output_dir)
        
        return {
            'tokens': all_tokens,
            'characters': character_sequence,
            'articles': articles,
            'stats': self.stats
        }
    
    def _generate_report(self, output_dir):
        """
        Generate a comprehensive preprocessing report
        """
        report = f"""
KASHUBIAN CORPUS PREPROCESSING REPORT
{'=' * 70}

Following CS6361 Week 5 & 7 Lecture Architecture:
- Markup Analysis (XML parsing)
- Tokenization (diacritic-aware)
- Case Normalization
- Punctuation Handling
- Stopword Decisions

CORPUS STATISTICS
{'=' * 70}

Input Processing:
  - XML elements processed: {self.stats['xml_elements_processed']:,}
  - Articles extracted: {self.stats['total_articles']:,}
  - Markup removed: {self.stats['markup_removed_chars']:,} characters

Output Statistics:
  - Total characters (cleaned): {self.stats['total_characters']:,}
  - Total words (tokens): {self.stats['total_words']:,}
  - Unique vocabulary: (calculated in frequency analysis)

PREPROCESSING DECISIONS
{'=' * 70}

1. MARKUP ANALYSIS:
   - Removed Wikipedia templates, references, categories
   - Extracted only article namespace content
   - Excluded talk pages, user pages, meta pages

2. TOKENIZATION:
   - Custom regex for Kashubian diacritics (ą, ã, é, ë, ń, ò, ó, ô, ù, ł, ż)
   - Ensures special characters treated as valid word components
   - Pattern: [aąãbcćdeęéëfghijklłmnńoòóôprsśtuùvwyzźż]+

3. CASE NORMALIZATION:
   - All tokens converted to lowercase
   - Ensures 'Kaszëbë' and 'kaszëbë' counted as same word

4. PUNCTUATION HANDLING:
   - Removed punctuation-only tokens
   - Preserved punctuation context during initial parsing

5. STOPWORD DECISION:
   - KEPT stopwords in corpus
   - Rationale: Essential for character frequency and lexical models
   - Stopwords include: {', '.join(sorted(list(self.stopwords)[:10]))} ...

ALIGNMENT WITH MODULE CONTENT
{'=' * 70}

Week 5 Lecture Concepts Applied:
✓ Markup Analysis - Wikipedia XML parsing
✓ Tokenization - Custom pattern for Kashubian diacritics
✓ Case normalization - Lowercase conversion
✓ Punctuation handling - Filtered punctuation-only tokens
✓ Stopword decisions - Kept for frequency analysis

Week 7 Lecture Concepts Applied:
✓ Language digitisation context - Kashubian ISO code: csb
✓ Unicode handling - Proper encoding for all diacritics
✓ Corpus quality - Wikipedia as authoritative source

FILES GENERATED
{'=' * 70}

1. tokens_preprocessed.txt
   - One token per line
   - Ready for word frequency analysis

2. characters_preprocessed.txt
   - Character sequence including spaces
   - Ready for character frequency analysis

3. preprocessing_stats.json
   - Detailed statistics from preprocessing pipeline

4. article_metadata.json
   - Per-article word and character counts
   - Useful for corpus quality assessment

5. preprocessing_report.txt (this file)
   - Complete documentation of preprocessing decisions

NEXT STEPS
{'=' * 70}

Run the frequency analysis scripts:
1. kashubian_character_frequency.py
2. kashubian_word_frequency.py
3. kashubian_zipf_analysis.py

These will generate the statistics needed for slides 5-8 of your presentation.
"""
        
        with open(f'{output_dir}/preprocessing_report.txt', 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"✓ Saved: preprocessing_report.txt")
        print("\n" + "=" * 60)
        print("PREPROCESSING COMPLETE!")
        print("=" * 60)


def main():
    """
    Main execution function
    """
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python kashubian_preprocessing.py <path_to_wikipedia_dump.xml.bz2>")
        print("\nExample:")
        print("  python kashubian_preprocessing.py csbwiki-latest-pages-articles.xml.bz2")
        sys.exit(1)
    
    xml_file_path = sys.argv[1]
    
    # Initialize preprocessor
    preprocessor = KashubianPreprocessor()
    
    # Run full preprocessing pipeline
    results = preprocessor.preprocess_corpus(xml_file_path)
    
    print(f"\n✓ All preprocessing complete!")
    print(f"✓ Generated files ready for frequency analysis")


if __name__ == '__main__':
    main()
