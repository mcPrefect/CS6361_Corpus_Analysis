#!/usr/bin/env python3
"""
KASHUBIAN PURE VOCABULARY BLACKLIST
====================================

Purpose: Create a clean Kashubian vocabulary list (lexicon) free from:
- HTML/CSS/Web markup
- English and other foreign languages
- Proper nouns (personal names, places, brands)
- Technical abbreviations and codes
- Numbers and measurements
- Single letters (except valid Kashubian function words)

This is optimized for linguistic research and vocabulary building.

Date: November 26, 2024
Version: 2.0 - Pure Vocabulary Edition
"""

# ============================================================================
# CATEGORY 1: HTML/CSS/WEB MARKUP (Always remove)
# ============================================================================

BLACKLIST_WEB_MARKUP = {
    # HTML tags and attributes
    'html', 'div', 'span', 'class', 'style', 'href', 'alt', 'src',
    'table', 'tbody', 'thead', 'tr', 'td', 'th',
    
    # CSS properties
    'left', 'right', 'center', 'top', 'bottom', 'width', 'height',
    'padding', 'margin', 'border', 'background', 'bgcolor', 'solid',
    'align', 'valign',
    
    # CSS measurements
    'px', 'pt', 'em', 'rem',
    
    # Table-specific
    'cellpadding', 'cellspacing', 'colspan', 'rowspan',
    
    # Web protocols and domains
    'http', 'https', 'www', 'com', 'org', 'net', 'edu', 'gov',
    'text-align', 'font-size', 'border-bottom', 'border-collapse', 'gainsboro',
    
    # File formats
    'html', 'htm', 'php', 'asp', 'jpg', 'jpeg', 'png', 'gif', 'svg',
    'pdf', 'doc', 'docx', 'txt', 'xml', 'json',
    
    # Wiki-specific markup
    'wikitable', 'thumb', 'thumbnail', 'frame', 'frameless', 'upright',
    'caption', 'file', 'image', 'link', 'collapse',
    
    # Special characters/entities
    'nbsp', 'amp', 'lt', 'gt', 'quot',
    
    # Hex colors
    'ffffff', 'efefef', 'cccccc', '000000',
}

# ============================================================================
# CATEGORY 2: ENGLISH WORDS (Always remove)
# ============================================================================

BLACKLIST_ENGLISH = {
    # Common function words
    # Note: 'i', 'to', 'do', 'we' removed - they're valid Kashubian words
    'the', 'of', 'and', 'or', 'in', 'on', 'at', 'for', 'from',
    'with', 'about', 'by', 'as', 'is', 'was', 'are', 'be', 'been',
    'have', 'has', 'had', 'does', 'did', 'will', 'would', 'could',
    'should', 'may', 'might', 'can', 'must',
    
    # Pronouns
    'he', 'she', 'it', 'they', 'me', 'him', 'her',
    'us', 'them', 'my', 'your', 'his', 'its', 'our', 'their',
    
    # Common content words that appeared in corpus
    'new', 'world', 'live', 'best', 'central', 'history', 'archive',
    'records', 'image', 'gray', 'grey', 'red', 'blue', 'green', 'black',
    'white', 'per', 'iron', 'stone', 'web', 'european', 'kashubs', 'love', 'bad', 'art',
    
    # Publishing/academic English
    'publishing', 'academic', 'imprint', 'press', 'university',
    'journal', 'volume', 'page', 'edition', 'published', 'edited',
    
    # Proper nouns (English-origin names that appeared)
    'bloomsbury', 'maiden', 'alfred', 'toyota', 'linux',
}

# ============================================================================
# CATEGORY 3: OTHER FOREIGN LANGUAGES
# ============================================================================

BLACKLIST_FOREIGN = {
    # German words
    'und', 'der', 'die', 'das', 'von', 'zu', 'im', 'am', 'ist',
    'wird', 'werden', 'wurde', 'wurden',
    
    # Polish words commonly appearing in mixed content
    'jest', 'się', 'został', 'została', 'były', 'miał',
    
    # Historical terms (English/German origins)
    'wends', 'sorbs', 'outposts',
    'cantharellus', 'cibarius', 'slav', 'też', 'pawła',
}

# ============================================================================
# CATEGORY 4: PROPER NOUNS (Personal names, places, brands)
# ============================================================================

BLACKLIST_PROPER_NOUNS = {
    # Personal names - Polish/European origin
    'piotr', 'paweł', 'józef', 'jan', 'jana', 'anna', 'maria', 'ewa',
    'adam', 'marian', 'jerzy', 'katarzyna', 'katarzëna', 'dorothee',
    'wilhelm', 'bernard', 'aleksander', 'aleksandra', 'stanisław', 'stanisłôw',
    'władisłôw', 'ryszard', 'andrzej', 'alojzy', 'henrik', 'dominik', 'franciszka',
    
    # Surnames / derived forms
    'zimmer', 'eisenreich', 'rachańska', 'kreyser', 'lorentz', 'labùda',
    'borzyszkowski', 'susk',
    
    # Brand names
    'toyota', 'linux',
    
    # Publishing houses
    'pwn', 'plc', 'ossolineum', 'multico', 'legia',
    
    # Note: Place names should be evaluated individually as some may be
    # legitimately Kashubian (like Gduńsk). Add specific ones as discovered.
}

# ============================================================================
# CATEGORY 5: ABBREVIATIONS & TECHNICAL CODES
# ============================================================================

BLACKLIST_ABBREVIATIONS = {
    # Measurements
    'km', 'cm', 'mm', 'm', 'dm', 'kg', 'g', 'mg', 'l', 'ml',
    
    # Academic/bibliographic
    'isbn', 'issn', 'doi', 'ed', 'eds', 'vol', 'pp', 'p',
    
    # Titles and honorifics
    'dr', 'prof', 'mgr', 'inż', 'hab',
    
    # Common abbreviations
    'nr', 'np', 'tzw', 'itd', 'itp', 'ok',
    
    # Linguistic/grammatical
    'sg', 'pl', 'nom', 'gen', 'dat', 'acc', 'loc', 'inst',
    
    # Other technical
    'wst', 'rkj', 'ss', 'st',
}

# ============================================================================
# CATEGORY 6: NUMBERS & ROMAN NUMERALS
# ============================================================================

BLACKLIST_NUMBERS = {
    # Roman numerals (used in citations, not vocabulary)
    # Note: 'i' removed - it's a valid Kashubian conjunction
    'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x',
    'xi', 'xii', 'xiii', 'xiv', 'xv', 'xvi', 'xvii', 'xviii', 'xix', 'xx',
    'xxi', 'xxx', 'xl', 'l', 'lx', 'lxx', 'lxxx', 'xc', 'c',
}

# ============================================================================
# CATEGORY 7: LANGUAGE & COUNTRY CODES
# ============================================================================

BLACKLIST_CODES = {
    # ISO language codes
    'en', 'de', 'pl', 'fr', 'es', 'it', 'ru', 'cs', 'sk', 'uk',
    'csb',  # Even Kashubian code itself in markup
    
    # Country codes (excluding 'cz' which is also a Kashubian digraph)
    'usa', 'gb', 'fr', 'ru',
}

# ============================================================================
# CATEGORY 8: SINGLE LETTERS & FRAGMENTS (Not vocabulary)
# ============================================================================

BLACKLIST_SINGLE_CHARS = {
    # Single Latin letters (not function words)
    # Note: Kashubian function words (w, i, z, s, a, etc.) are NOT here
    # because they're protected by the whitelist
    'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'l', 'm', 'n',
    'o', 'p', 'q', 'r', 't', 'u', 'v', 'x', 'y',
    
    # Mathematical/Greek
    'pi', 'mu', 'sigma', 'alpha', 'beta', 'gamma', 'delta',
}

# ============================================================================
# FINAL COMBINED BLACKLIST
# ============================================================================

FINAL_BLACKLIST = (
    BLACKLIST_WEB_MARKUP |
    BLACKLIST_ENGLISH |
    BLACKLIST_FOREIGN |
    BLACKLIST_PROPER_NOUNS |
    BLACKLIST_ABBREVIATIONS |
    BLACKLIST_NUMBERS |
    BLACKLIST_CODES |
    BLACKLIST_SINGLE_CHARS
)

# ============================================================================
# WHITELIST - PROTECTED KASHUBIAN WORDS
# ============================================================================
# These words are NEVER removed, even if they appear in blacklist categories

WHITELIST = {
    # ========================================================================
    # KASHUBIAN FUNCTION WORDS (Core grammar words - very high frequency)
    # ========================================================================
    
    # Prepositions (single letter)
    'w',        # "in" (w jizbje = in the room)
    'z',        # "from/with" (z domu = from home)
    's',        # "with" (alternate form)
    'k',        # "to/toward"
    'ò',        # "about" (Kashubian preposition)
    
    # Conjunctions
    'i',        # "and" (identical to Polish but valid Kashubian)
    'a',        # "and/but" (different nuance from 'i')
    
    # Pronouns and determiners
    'to',       # "this/that/it" - demonstrative (to je = it is)
    'të',       # "you" (sg, familiar)
    'më',       # "we"
    'òn',       # "he"
    'òna',      # "she"
    'òno',      # "it"
    'le',       # article-like particle
    
    # Common verbs (very short forms)
    'je',       # "is" (3rd person singular of "to be")
    'są',       # "are" (plural of "to be")
    'ma',       # "has"
    'mô',       # "has" (alternate spelling)
    
    # Particles and discourse markers
    'të',       # emphatic particle
    'no',       # particle (like "well", "so")
    'ja',       # "I" or emphatic particle
    'co',       # "what"
    'to',       # "this" (already listed but important)
    
    # ========================================================================
    # KASHUBIAN LETTERS & DIACRITICS (Never remove these!)
    # ========================================================================
    
    # Special vowels with diacritics
    'ã',        # nasal a (a with tilde)
    'é',        # e-acute
    'ë',        # e with diaeresis (schwa sound)
    'ó',        # o-acute
    'ô',        # o with circumflex
    'ù',        # u with grave
    
    # Special consonants
    'ł',        # l with stroke (CRITICAL - very common!)
    'ń',        # n with acute
    'ż',        # z with dot above
    'ź',        # z with acute
    
    # ========================================================================
    # KASHUBIAN DIGRAPHS (If appearing as standalone in tokenization)
    # ========================================================================
    # Note: These should appear as part of words, but protect just in case
    
    'ch',       # like English "ch" in "church"
    'cz',       # like English "ch"
    'dz',       # voiced "ts"
    'dż',       # like English "j"
    'rz',       # like "zh"
    'sz',       # like English "sh"
    
    # ========================================================================
    # TWO-LETTER FUNCTION WORDS
    # ========================================================================
    
    'na',       # "on/to"
    'òd',       # "from"
    'do',       # "to/into"
    'pò',       # "after/for"
    'ni',       # "not/than"
    'të',       # "you" (already listed)
    'so',       # "are" (auxiliary)
    'we',       # "in" (with loc)
    
    # ========================================================================
    # THREE-LETTER FUNCTION WORDS
    # ========================================================================
    
    'bez',      # "without"
    'ale',      # "but"
    'neg',      # negation particle
    'òle',      # "about"
    'dlô',      # "for"
    'jak',      # "how/as"
    'czi',      # "if/whether"
    'ani',      # "neither/nor"
    'abò',      # "or"
    
    # ========================================================================
    # COMMON SHORT WORDS (High frequency, definitely Kashubian)
    # ========================================================================
    
    'òni',      # "they"
    'jich',     # "their"
    'jim',      # "to them"
    'tej',      # "this" (fem)
    'ten',      # "this" (masc)
    'tom',      # "this" (fem, different case)
    'tak',      # "so/yes"
    'nie',      # "no/not"
    'më',       # "we" (already listed)
    'më',       # possessive "our"
    'bëc',      # "to be" (infinitive)
    'był',      # "was"
    'bëła',     # "was" (fem)
    'są',       # "are" (already listed)
}

# ============================================================================
# VALIDATION: Check for conflicts
# ============================================================================

def validate_lists():
    """Check for overlaps between blacklist and whitelist"""
    overlap = FINAL_BLACKLIST & WHITELIST
    if overlap:
        print(f"⚠️  WARNING: Overlap detected between blacklist and whitelist:")
        for word in sorted(overlap):
            print(f"   - '{word}'")
        print(f"\nWhitelist takes precedence, but you should review these conflicts.")
        return False
    return True

# ============================================================================
# CORE FUNCTIONS
# ============================================================================

def should_keep_word(word):
    """
    Determine if a word should be kept in a pure vocabulary list.
    
    Priority:
    1. Whitelist overrides everything (protected Kashubian)
    2. Blacklist removes pollution
    3. Keep everything else
    
    Args:
        word (str): Word to check
        
    Returns:
        bool: True if word should be kept, False if removed
    """
    word_lower = word.lower()
    
    # PRIORITY 1: Whitelist - always keep
    if word_lower in WHITELIST:
        return True
    
    # PRIORITY 2: Blacklist - remove
    if word_lower in FINAL_BLACKLIST:
        return False
    
    # PRIORITY 3: Default - keep
    # (Assumes everything else is potentially valid Kashubian)
    return True


def clean_corpus(words):
    """
    Clean a list of words for pure vocabulary extraction.
    
    Args:
        words (list): List of words from corpus
        
    Returns:
        tuple: (cleaned_words, statistics_dict)
    """
    original_count = len(words)
    
    # Track what was removed for analysis
    removed_by_category = {
        'web_markup': 0,
        'english': 0,
        'foreign': 0,
        'proper_nouns': 0,
        'abbreviations': 0,
        'numbers': 0,
        'codes': 0,
        'single_chars': 0,
        'protected_by_whitelist': 0,
    }
    
    # Filter words
    cleaned_words = []
    for word in words:
        word_lower = word.lower()
        
        # Check whitelist first
        if word_lower in WHITELIST:
            cleaned_words.append(word)
            removed_by_category['protected_by_whitelist'] += 1
            continue
        
        # Check each blacklist category
        if word_lower in BLACKLIST_WEB_MARKUP:
            removed_by_category['web_markup'] += 1
            continue
        if word_lower in BLACKLIST_ENGLISH:
            removed_by_category['english'] += 1
            continue
        if word_lower in BLACKLIST_FOREIGN:
            removed_by_category['foreign'] += 1
            continue
        if word_lower in BLACKLIST_PROPER_NOUNS:
            removed_by_category['proper_nouns'] += 1
            continue
        if word_lower in BLACKLIST_ABBREVIATIONS:
            removed_by_category['abbreviations'] += 1
            continue
        if word_lower in BLACKLIST_NUMBERS:
            removed_by_category['numbers'] += 1
            continue
        if word_lower in BLACKLIST_CODES:
            removed_by_category['codes'] += 1
            continue
        if word_lower in BLACKLIST_SINGLE_CHARS:
            removed_by_category['single_chars'] += 1
            continue
        
        # Keep if not blacklisted
        cleaned_words.append(word)
    
    # Calculate statistics
    removed_count = original_count - len(cleaned_words)
    
    stats = {
        'original_words': original_count,
        'cleaned_words': len(cleaned_words),
        'removed_words': removed_count,
        'percentage_removed': (removed_count / original_count * 100) if original_count > 0 else 0,
        'removed_by_category': removed_by_category,
        'blacklist_size': len(FINAL_BLACKLIST),
        'whitelist_size': len(WHITELIST),
    }
    
    return cleaned_words, stats


def print_statistics():
    """Print comprehensive blacklist/whitelist statistics"""
    print("=" * 70)
    print("KASHUBIAN PURE VOCABULARY BLACKLIST - STATISTICS")
    print("=" * 70)
    print()
    
    print("BLACKLIST BY CATEGORY:")
    print(f"  Web markup:        {len(BLACKLIST_WEB_MARKUP):>4} words")
    print(f"  English:           {len(BLACKLIST_ENGLISH):>4} words")
    print(f"  Foreign languages: {len(BLACKLIST_FOREIGN):>4} words")
    print(f"  Proper nouns:      {len(BLACKLIST_PROPER_NOUNS):>4} words")
    print(f"  Abbreviations:     {len(BLACKLIST_ABBREVIATIONS):>4} words")
    print(f"  Numbers/Numerals:  {len(BLACKLIST_NUMBERS):>4} words")
    print(f"  Language codes:    {len(BLACKLIST_CODES):>4} words")
    print(f"  Single chars:      {len(BLACKLIST_SINGLE_CHARS):>4} words")
    print(f"  " + "-" * 30)
    print(f"  TOTAL BLACKLIST:   {len(FINAL_BLACKLIST):>4} words")
    print()
    
    print(f"WHITELIST (Protected Kashubian): {len(WHITELIST)} words")
    print()
    
    # Check for overlaps
    overlap = FINAL_BLACKLIST & WHITELIST
    if overlap:
        print(f"⚠️  CONFLICTS: {len(overlap)} words in both lists")
        print("   (Whitelist takes precedence)")
    else:
        print("✅ No conflicts between blacklist and whitelist")
    print()
    
    print("=" * 70)


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    import sys
    
    # Ensure UTF-8 output
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    
    print_statistics()
    
    # Validate for conflicts
    print("\nVALIDATION:")
    if validate_lists():
        print("✅ All validation checks passed!\n")
    else:
        print("⚠️  Please review conflicts above\n")
    
    # Test with sample words
    print("=" * 70)
    print("TEST EXAMPLES")
    print("=" * 70)
    print()
    
    test_cases = [
        # Should KEEP (valid Kashubian)
        ('w', True, "Kashubian preposition 'in'"),
        ('i', True, "Kashubian conjunction 'and'"),
        ('to', True, "Kashubian demonstrative 'this/that'"),
        ('je', True, "Kashubian 'is'"),
        ('ł', True, "Kashubian letter"),
        ('bëc', True, "Kashubian 'to be'"),
        ('kaszëbsczi', True, "Kashubian 'Kashubian'"),
        ('gmina', True, "Valid word (municipality)"),
        
        # Should REMOVE (pollution)
        ('www', False, "Web markup"),
        ('html', False, "Web markup"),
        ('the', False, "English"),
        ('from', False, "English"),
        ('toyota', False, "Brand name"),
        ('piotr', False, "Personal name"),
        ('km', False, "Abbreviation"),
        ('isbn', False, "Code"),
        ('xiv', False, "Roman numeral"),
        ('pl', False, "Country code"),
        ('a', True, "Kashubian conjunction 'a'"),
        ('x', False, "Single letter"),
    ]
    
    print(f"{'Word':<20} {'Keep?':<10} {'Reason':<40}")
    print("-" * 70)
    
    for word, expected_keep, reason in test_cases:
        actual_keep = should_keep_word(word)
        status = "✅" if actual_keep == expected_keep else "❌"
        keep_str = "KEEP" if actual_keep else "REMOVE"
        
        print(f"{word:<20} {keep_str:<10} {reason:<40} {status}")
    
    print()
    print("=" * 70)
    print("✅ Blacklist ready for pure vocabulary extraction!")
    print("=" * 70)
