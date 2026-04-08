"""
AI Content Detection Engine v2

Detects AI-generated text using 10 analysis signals tuned for modern LLM output
(ChatGPT, Claude, Gemini, etc). Modern AI avoids obvious phrases but still exhibits:
- Perfect grammar with zero errors
- No contractions (formal tone throughout)
- Uniform sentence lengths (low burstiness)
- Predictable sentence openings
- Hedging / qualifying language
- Balanced paragraph structure
- Lack of personal voice / opinions
- Excessive cohesion (every sentence connects smoothly)
- Moderate vocabulary (not too simple, not too complex)
- Clean punctuation patterns
"""
import re
import math
import string
from collections import Counter


# ============================================================
# PHRASE & PATTERN DATABASES
# ============================================================

# Obvious AI phrases (still worth checking)
AI_MARKER_PHRASES = [
    "it's important to note", "it is important to note",
    "it's worth noting", "it is worth noting",
    "in conclusion", "in summary",
    "additionally", "furthermore", "moreover",
    "plays a crucial role", "plays a vital role",
    "in today's world", "in today's digital age",
    "in the realm of", "in the context of",
    "landscape", "paradigm", "leverage",
    "delve", "delving", "tapestry",
    "multifaceted", "nuanced", "comprehensive",
    "robust", "seamless", "cutting-edge", "groundbreaking",
    "foster", "fostering", "navigate", "navigating",
    "unlock", "unlocking", "harness", "harnessing",
    "streamline", "streamlining", "spearhead",
    "elevate", "elevating", "underscores",
    "pivotal", "paramount", "ever-evolving",
    "a myriad of", "myriad", "plethora", "testament",
    "embark", "embarking", "first and foremost",
    "last but not least", "it goes without saying",
    "needless to say", "without a doubt",
    "serves as a", "stands as a",
    "in essence", "essentially", "ultimately",
]

# Subtle AI patterns — hedging and qualifying phrases
AI_HEDGING_PHRASES = [
    "it can be", "it may be", "this can lead to",
    "this allows", "this enables", "this helps",
    "this means that", "this is because",
    "this is especially", "this is particularly",
    "one of the most", "one of the key",
    "there are many", "there are several",
    "there are various", "there are numerous",
    "it is also", "it is often",
    "it is generally", "it is widely",
    "it is commonly", "it is typically",
    "can also be", "may also be",
    "tends to be", "is known for",
    "is considered", "is often seen",
    "plays an important", "plays a key",
    "plays a significant", "has become",
    "has been", "have become",
    "whether it's", "whether it is",
    "not only", "but also",
    "as well as", "in order to",
    "is essential for", "is crucial for",
    "is important for", "is necessary for",
    "when it comes to", "it comes to",
    "the ability to", "the importance of",
    "the impact of", "the role of",
    "the benefits of", "the potential of",
    "the power of", "the need for",
    "the way we", "the world of",
    "a wide range of", "a variety of",
    "a number of", "a great deal of",
    "make informed", "informed decisions",
    "in various", "across various",
    "can help", "can provide",
    "can improve", "can enhance",
    "can lead to", "can result in",
    "is designed to", "are designed to",
]

# Formal sentence starters that AI overuses
AI_SENTENCE_STARTERS = [
    "this", "these", "those", "such",
    "however", "therefore", "consequently",
    "nevertheless", "furthermore", "additionally",
    "moreover", "meanwhile", "similarly",
    "in addition", "in fact", "in particular",
    "for example", "for instance",
    "as a result", "on the other hand",
    "by understanding", "by leveraging", "by using",
    "by focusing", "by incorporating",
    "with the", "with its", "with this",
    "from the", "from a",
    "through the", "through its",
    "while the", "while it", "while this",
    "although", "despite",
    "overall", "ultimately", "essentially",
]

AI_TRANSITION_PATTERNS = [
    r"^(however|therefore|consequently|nevertheless|nonetheless|thus|hence|accordingly)[,\s]",
    r"^(first|second|third|finally|lastly|additionally|furthermore|moreover)[,\s]",
    r"^in (addition|contrast|comparison|particular|general|fact)[,\s]",
    r"^(for (example|instance)|such as|specifically)[,\s]",
    r"^(as a result|on the (other|one) hand|in other words)[,\s]",
    r"^(to (begin|start|conclude|summarize)|overall|ultimately|essentially)[,\s]",
    r"^(while|although|despite|regardless)[,\s]",
    r"^(by|through|with) (the|this|its|a|understanding|leveraging|using|focusing)\b",
    r"^(this|these|those|such) (is|are|was|were|has|have|can|could|may|might|will|would|should)\b",
]


# ============================================================
# TOKENIZERS
# ============================================================

def tokenize_sentences(text):
    """Split text into sentences."""
    text = re.sub(r'\s+', ' ', text.strip())
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', text)
    return [s.strip() for s in sentences if len(s.strip()) > 5]


def tokenize_words(text):
    """Split text into words."""
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation.replace("'", "")))
    words = text.split()
    return [w for w in words if len(w) > 0]


# ============================================================
# ANALYSIS SIGNALS
# ============================================================

def calculate_perplexity_score(text):
    """
    AI text uses common, predictable word patterns -> lower entropy.
    Also checks for word frequency distribution flatness.
    """
    words = tokenize_words(text)
    if len(words) < 20:
        return 50.0

    freq = Counter(words)
    total = len(words)
    probabilities = [count / total for count in freq.values()]
    entropy = -sum(p * math.log2(p) for p in probabilities if p > 0)
    max_entropy = math.log2(len(freq)) if len(freq) > 1 else 1
    normalized = entropy / max_entropy if max_entropy > 0 else 0

    # AI text: high normalized entropy (uses many words roughly equally)
    # Human text: more skewed distribution (favorites + rare words)
    # AI typically falls in 0.88-0.96 range for normalized entropy
    if normalized > 0.92:
        score = 75 + (normalized - 0.92) * 300
    elif normalized > 0.85:
        score = 55 + (normalized - 0.85) * 285
    elif normalized > 0.78:
        score = 40 + (normalized - 0.78) * 214
    else:
        score = max(10, normalized * 51)

    return min(100, max(0, score))


def calculate_burstiness_score(text):
    """
    Sentence length variation. AI text has very uniform sentence lengths.
    Human writing naturally bursts between short and long sentences.
    """
    sentences = tokenize_sentences(text)
    if len(sentences) < 3:
        return 60.0

    lengths = [len(tokenize_words(s)) for s in sentences]
    mean_len = sum(lengths) / len(lengths)

    if mean_len == 0:
        return 50.0

    variance = sum((l - mean_len) ** 2 for l in lengths) / len(lengths)
    std_dev = math.sqrt(variance)
    cv = std_dev / mean_len

    # AI text CV typically 0.15-0.35. Human text CV typically 0.40-0.80+
    if cv < 0.20:
        score = 95
    elif cv < 0.30:
        score = 80 + (0.30 - cv) * 150
    elif cv < 0.40:
        score = 65 + (0.40 - cv) * 150
    elif cv < 0.55:
        score = 40 + (0.55 - cv) * 167
    else:
        score = max(5, 40 - (cv - 0.55) * 70)

    # Bonus: check if ALL sentences are in a narrow range (AI pattern)
    if lengths:
        range_ratio = (max(lengths) - min(lengths)) / mean_len if mean_len > 0 else 0
        if range_ratio < 0.8:
            score += 10
        elif range_ratio < 0.5:
            score += 15

    return min(100, max(0, score))


def calculate_vocabulary_score(text):
    """
    AI has moderate, consistent vocabulary — not too simple, not too complex.
    Checks TTR, average word length, and sophistication patterns.
    """
    words = tokenize_words(text)
    if len(words) < 20:
        return 50.0

    unique_words = set(words)
    ttr = len(unique_words) / len(words)

    # Average word length — AI tends toward 4.5-5.5 chars
    avg_word_len = sum(len(w) for w in words) / len(words)

    score = 0

    # TTR in AI's typical range
    if 0.45 <= ttr <= 0.65:
        score += 45
    elif 0.38 <= ttr <= 0.72:
        score += 30
    else:
        score += 10

    # Average word length in AI's typical range
    if 4.2 <= avg_word_len <= 5.8:
        score += 30
    elif 3.8 <= avg_word_len <= 6.2:
        score += 20
    else:
        score += 5

    # Check for sophisticated AI vocabulary
    sophisticated_words = [
        'utilize', 'facilitate', 'implement', 'comprehensive',
        'significant', 'fundamental', 'demonstrate', 'establish',
        'contribute', 'enhance', 'optimize', 'integrate',
        'approach', 'aspects', 'effectively', 'specifically',
        'particularly', 'increasingly', 'essential', 'potential',
        'various', 'crucial', 'numerous', 'diverse',
        'respective', 'relevant', 'maintain', 'ensure',
        'regarding', 'associated', 'traditional', 'conventional',
    ]
    text_lower = text.lower()
    hits = sum(1 for w in sophisticated_words if w in text_lower)
    score += min(25, hits * 4)

    return min(100, max(0, score))


def calculate_phrase_score(text):
    """
    Detect both obvious and subtle AI phrases.
    """
    text_lower = text.lower()
    words = tokenize_words(text)
    word_count = len(words)

    if word_count < 10:
        return 50.0, []

    # Count obvious AI marker phrases
    phrase_hits = 0
    matched_phrases = []
    for phrase in AI_MARKER_PHRASES:
        count = text_lower.count(phrase)
        if count > 0:
            phrase_hits += count
            matched_phrases.append(phrase)

    # Count subtle AI hedging phrases
    hedge_hits = 0
    for phrase in AI_HEDGING_PHRASES:
        count = text_lower.count(phrase)
        if count > 0:
            hedge_hits += count

    # Density per 100 words
    obvious_density = (phrase_hits / word_count) * 100
    hedge_density = (hedge_hits / word_count) * 100
    total_density = obvious_density + hedge_density

    # Score based on combined density
    if total_density > 8:
        score = 98
    elif total_density > 5:
        score = 85 + (total_density - 5) * 4.3
    elif total_density > 3:
        score = 70 + (total_density - 3) * 7.5
    elif total_density > 1.5:
        score = 50 + (total_density - 1.5) * 13.3
    elif total_density > 0.5:
        score = 30 + (total_density - 0.5) * 20
    else:
        score = max(5, total_density * 60)

    return min(100, max(0, score)), matched_phrases


def calculate_structure_score(text):
    """
    AI text follows predictable structural patterns:
    - Formal sentence starters
    - Transition words at beginnings
    - Parallel structures
    """
    sentences = tokenize_sentences(text)
    if len(sentences) < 3:
        return 55.0

    # Check transition patterns
    transition_count = 0
    for sentence in sentences:
        sentence_lower = sentence.lower().strip()
        for pattern in AI_TRANSITION_PATTERNS:
            if re.match(pattern, sentence_lower):
                transition_count += 1
                break

    transition_ratio = transition_count / len(sentences)

    # Check formal sentence starters
    formal_start_count = 0
    for sentence in sentences:
        first_word = tokenize_words(sentence)[0] if tokenize_words(sentence) else ''
        first_two = ' '.join(tokenize_words(sentence)[:2]) if len(tokenize_words(sentence)) >= 2 else ''
        for starter in AI_SENTENCE_STARTERS:
            if first_word == starter or first_two.startswith(starter):
                formal_start_count += 1
                break

    formal_ratio = formal_start_count / len(sentences)

    # Combined score
    score = 0
    # Transition patterns
    score += min(50, transition_ratio * 120)
    # Formal starters
    score += min(50, formal_ratio * 90)

    # Parallel structure bonus
    starts = [tokenize_words(s)[0] for s in sentences if tokenize_words(s)]
    start_counts = Counter(starts)
    most_common_ratio = start_counts.most_common(1)[0][1] / len(sentences) if starts else 0
    if most_common_ratio > 0.3:
        score += 10

    return min(100, max(0, score))


def calculate_formality_score(text):
    """
    AI text is uniformly formal. Humans mix formal/informal, use contractions,
    sentence fragments, exclamations, questions, etc.
    """
    words = tokenize_words(text)
    sentences = tokenize_sentences(text)
    if len(words) < 20:
        return 50.0

    score = 65  # Base assumption: text is somewhat formal (AI-like)

    text_lower = text.lower()

    # Check for contractions (human signal — LOWERS score)
    contractions = [
        "n't", "'m", "'re", "'ve", "'ll", "'d",
        "cant", "dont", "wont", "isnt", "arent", "wasnt",
        "didnt", "doesnt", "havent", "hasnt", "wouldnt",
        "shouldnt", "couldnt", "im ", "ive ", "youre",
        "theyre", "weve", "theyve",
    ]
    contraction_count = sum(1 for c in contractions if c in text_lower)
    score -= contraction_count * 10  # Contractions = more human

    # Check for questions and exclamations (human signal)
    question_count = text.count('?')
    exclamation_count = text.count('!')
    score -= question_count * 6
    score -= exclamation_count * 6

    # Check for first person casual usage (human signal)
    first_person = len(re.findall(r'\b(I|me|my|myself)\b', text))
    casual_ratio = first_person / len(words) * 100
    if casual_ratio > 2:
        score -= 18
    elif casual_ratio > 0.5:
        score -= 10

    # Check for informal words (human signal)
    informal_words = [
        'pretty', 'really', 'actually', 'basically',
        'honestly', 'stuff', 'things', 'kind of',
        'sort of', 'a lot', 'lots of', 'gonna',
        'wanna', 'gotta', 'kinda', 'yeah', 'okay',
        'ok ', 'cool', 'awesome', 'huge', 'totally',
        'super', 'literally', 'legit', 'lol', 'haha',
        'idk', 'tbh', 'imo', 'btw', 'ngl',
    ]
    informal_count = sum(1 for w in informal_words if w in text_lower)
    score -= informal_count * 7

    # Check for sentence fragments (human signal)
    short_sentences = [s for s in sentences if len(tokenize_words(s)) < 5]
    if short_sentences:
        score -= len(short_sentences) * 5

    # No contractions AND no questions AND no informal language = very AI
    if contraction_count == 0 and question_count == 0 and informal_count == 0:
        score += 25

    # Formal "it is" / "there are" patterns instead of contractions
    formal_constructs = len(re.findall(
        r'\b(it is|it has|there is|there are|do not|does not|did not|is not|are not|was not|cannot|will not|would not|should not|could not|have not|has not)\b',
        text_lower
    ))
    score += formal_constructs * 4

    return min(100, max(0, score))


def calculate_cohesion_score(text):
    """
    AI text has excessive cohesion — every sentence connects smoothly to the next.
    Checks for connective density and referencing patterns.
    """
    sentences = tokenize_sentences(text)
    if len(sentences) < 3:
        return 50.0

    text_lower = text.lower()

    # Connective words/phrases
    connectives = [
        'this', 'these', 'those', 'such', 'its', 'their',
        'also', 'however', 'therefore', 'thus', 'hence',
        'furthermore', 'moreover', 'additionally', 'meanwhile',
        'consequently', 'nevertheless', 'similarly', 'likewise',
        'in addition', 'as a result', 'on the other hand',
        'for example', 'for instance', 'in particular',
        'in fact', 'indeed', 'specifically', 'notably',
    ]

    connective_count = 0
    for conn in connectives:
        connective_count += len(re.findall(r'\b' + re.escape(conn) + r'\b', text_lower))

    words = tokenize_words(text)
    connective_density = (connective_count / len(words)) * 100 if words else 0

    # AI typically has 5-15% connective density
    if connective_density > 10:
        score = 90
    elif connective_density > 7:
        score = 70 + (connective_density - 7) * 6.7
    elif connective_density > 4:
        score = 50 + (connective_density - 4) * 6.7
    elif connective_density > 2:
        score = 30 + (connective_density - 2) * 10
    else:
        score = max(10, connective_density * 15)

    # Check for "this/these/those" starting sentences (AI loves back-referencing)
    backref_count = sum(1 for s in sentences if re.match(r'^(this|these|those|such)\b', s.lower()))
    backref_ratio = backref_count / len(sentences)
    score += backref_ratio * 30

    return min(100, max(0, score))


def calculate_repetition_score(text):
    """
    Detect repetitive patterns in word choice and n-grams.
    """
    words = tokenize_words(text)
    if len(words) < 30:
        return 50.0

    # Bigram and trigram repetition
    bigrams = [tuple(words[i:i+2]) for i in range(len(words)-1)]
    trigrams = [tuple(words[i:i+3]) for i in range(len(words)-2)]

    bigram_counts = Counter(bigrams)
    trigram_counts = Counter(trigrams)

    repeated_bigrams = sum(c - 1 for c in bigram_counts.values() if c >= 2)
    repeated_trigrams = sum(c - 1 for c in trigram_counts.values() if c >= 2)

    bigram_repetition_rate = repeated_bigrams / len(bigrams) if bigrams else 0
    trigram_repetition_rate = repeated_trigrams / len(trigrams) if trigrams else 0

    score = min(100, (bigram_repetition_rate * 300 + trigram_repetition_rate * 500))
    return max(0, score)


def calculate_readability_uniformity(text):
    """
    AI maintains consistent complexity throughout. Humans vary.
    Splits text into chunks and compares readability metrics.
    """
    sentences = tokenize_sentences(text)
    if len(sentences) < 4:
        return 55.0

    # Split sentences into chunks of 3 and measure each chunk
    chunk_size = max(2, len(sentences) // 3)
    chunks = [sentences[i:i+chunk_size] for i in range(0, len(sentences), chunk_size)]
    chunks = [c for c in chunks if len(c) >= 2]

    if len(chunks) < 2:
        return 55.0

    # Measure avg word length per chunk
    chunk_metrics = []
    for chunk in chunks:
        all_words = []
        for s in chunk:
            all_words.extend(tokenize_words(s))
        if all_words:
            avg_wl = sum(len(w) for w in all_words) / len(all_words)
            avg_sl = sum(len(tokenize_words(s)) for s in chunk) / len(chunk)
            chunk_metrics.append((avg_wl, avg_sl))

    if len(chunk_metrics) < 2:
        return 55.0

    # Check variation in word length across chunks
    wl_values = [m[0] for m in chunk_metrics]
    sl_values = [m[1] for m in chunk_metrics]

    wl_range = max(wl_values) - min(wl_values)
    sl_range = max(sl_values) - min(sl_values)
    sl_mean = sum(sl_values) / len(sl_values)
    sl_cv = (sl_range / sl_mean) if sl_mean > 0 else 0

    # Low variation = AI
    score = 0
    if wl_range < 0.3:
        score += 50
    elif wl_range < 0.5:
        score += 35
    elif wl_range < 0.8:
        score += 20
    else:
        score += 5

    if sl_cv < 0.15:
        score += 50
    elif sl_cv < 0.30:
        score += 35
    elif sl_cv < 0.50:
        score += 20
    else:
        score += 5

    return min(100, max(0, score))


def calculate_punctuation_score(text):
    """
    AI text has clean, predictable punctuation:
    - Almost always ends with periods
    - Rarely uses dashes, semicolons, parentheses creatively
    - No ellipses, no double punctuation
    """
    sentences = tokenize_sentences(text)
    if len(sentences) < 3:
        return 50.0

    score = 50  # Neutral start

    # Period dominance — AI almost always ends with '.'
    period_endings = sum(1 for s in sentences if s.rstrip().endswith('.'))
    period_ratio = period_endings / len(sentences)
    if period_ratio > 0.9:
        score += 25
    elif period_ratio > 0.75:
        score += 15

    # Lack of creative punctuation (human signal reduces score)
    em_dashes = text.count('—') + text.count(' - ') + text.count('--')
    semicolons = text.count(';')
    colons = text.count(':')
    parentheses = text.count('(')
    ellipses = text.count('...')

    creative_punct = em_dashes + semicolons + parentheses + ellipses
    if creative_punct == 0:
        score += 20  # No creative punctuation = very AI
    elif creative_punct <= 1:
        score += 10
    else:
        score -= creative_punct * 3  # Creative punctuation = human

    # Comma density — AI uses commas very consistently
    comma_count = text.count(',')
    words = tokenize_words(text)
    comma_rate = (comma_count / len(words)) * 100 if words else 0
    if 3 <= comma_rate <= 7:
        score += 5  # AI's typical comma range

    return min(100, max(0, score))


# ============================================================
# MAIN ANALYSIS
# ============================================================

def analyze_text(text):
    """
    Combines all signals into a final AI probability score.
    """
    if not text or len(text.strip()) < 50:
        return {
            'ai_probability': 0,
            'verdict': 'insufficient_text',
            'message': 'Please provide at least 50 characters of text for analysis.',
            'details': {},
            'flagged_phrases': [],
        }

    # Calculate individual scores
    perplexity = calculate_perplexity_score(text)
    burstiness = calculate_burstiness_score(text)
    vocabulary = calculate_vocabulary_score(text)
    phrase_score, flagged_phrases = calculate_phrase_score(text)
    structure = calculate_structure_score(text)
    formality = calculate_formality_score(text)
    cohesion = calculate_cohesion_score(text)
    repetition = calculate_repetition_score(text)
    readability = calculate_readability_uniformity(text)
    punctuation = calculate_punctuation_score(text)

    # Weighted combination — tuned for modern AI detection
    weights = {
        'perplexity': 0.08,
        'burstiness': 0.14,
        'vocabulary': 0.08,
        'phrase_detection': 0.14,
        'structure': 0.12,
        'formality': 0.16,
        'cohesion': 0.10,
        'repetition': 0.04,
        'readability_uniformity': 0.08,
        'punctuation': 0.06,
    }

    scores = {
        'perplexity': round(perplexity, 1),
        'burstiness': round(burstiness, 1),
        'vocabulary': round(vocabulary, 1),
        'phrase_detection': round(phrase_score, 1),
        'structure': round(structure, 1),
        'formality': round(formality, 1),
        'cohesion': round(cohesion, 1),
        'repetition': round(repetition, 1),
        'readability_uniformity': round(readability, 1),
        'punctuation': round(punctuation, 1),
    }

    weighted_sum = sum(scores[k] * weights[k] for k in weights)

    # Confidence boost: if many signals agree, increase confidence
    high_signals = sum(1 for v in scores.values() if v >= 55)
    if high_signals >= 8:
        weighted_sum = weighted_sum * 1.20
    elif high_signals >= 6:
        weighted_sum = weighted_sum * 1.12
    elif high_signals >= 5:
        weighted_sum = weighted_sum * 1.06

    ai_probability = round(min(100, max(0, weighted_sum)), 1)

    # Determine verdict
    if ai_probability >= 80:
        verdict = 'ai_generated'
        message = 'This text is very likely AI-generated.'
    elif ai_probability >= 60:
        verdict = 'likely_ai'
        message = 'This text is likely AI-generated with some human elements.'
    elif ai_probability >= 40:
        verdict = 'mixed'
        message = 'This text appears to be a mix of AI and human writing.'
    elif ai_probability >= 20:
        verdict = 'likely_human'
        message = 'This text is likely human-written with minor AI-like patterns.'
    else:
        verdict = 'human'
        message = 'This text appears to be human-written.'

    words = tokenize_words(text)
    sentences = tokenize_sentences(text)

    return {
        'ai_probability': ai_probability,
        'verdict': verdict,
        'message': message,
        'details': scores,
        'weights': {k: round(v * 100) for k, v in weights.items()},
        'flagged_phrases': flagged_phrases[:15],
        'stats': {
            'word_count': len(words),
            'sentence_count': len(sentences),
            'character_count': len(text),
        }
    }
