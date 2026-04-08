"""
Text Humanization Engine v2

Aggressively transforms AI-generated text to bypass detection by targeting
all 10 detection signals:
1. Perplexity → vary word choices, mix simple and complex
2. Burstiness → dramatically vary sentence lengths
3. Vocabulary → replace formal/moderate words with casual ones
4. Phrase detection → replace ALL AI phrases and hedging patterns
5. Structure → remove formal starters, break predictable patterns
6. Formality → add contractions, questions, informal words, first person
7. Cohesion → remove excessive connectives, break smooth flow
8. Repetition → vary repeated n-grams
9. Readability uniformity → mix complexity across paragraphs
10. Punctuation → add dashes, questions, exclamations, varied endings
"""
import re
import random


# ============================================================
# REPLACEMENT DATABASES
# ============================================================

# AI phrases → natural replacements
PHRASE_REPLACEMENTS = {
    # Multi-word phrases (matched first due to length sorting)
    "it's important to note that": ["thing is,", "look,", "honestly,"],
    "it is important to note that": ["thing is,", "look,", "honestly,"],
    "it's worth noting that": ["actually,", "turns out,", "interestingly enough,"],
    "it is worth noting that": ["actually,", "turns out,", "interestingly enough,"],
    "plays a crucial role in": ["really matters for", "is a big deal when it comes to", "is pretty key for"],
    "plays a vital role in": ["is super important for", "really helps with", "matters a lot for"],
    "plays a significant role in": ["has a big impact on", "really affects", "matters for"],
    "plays an important role in": ["really matters for", "is key to", "has a lot to do with"],
    "plays a key role in": ["is really central to", "matters a ton for", "drives a lot of"],
    "in today's digital age": ["these days,", "with how things are now,", "nowadays,"],
    "in today's world": ["these days,", "right now,", "the way things are,"],
    "in the realm of": ["when it comes to", "with", "talking about"],
    "in the context of": ["when we look at", "for", "thinking about"],
    "in order to": ["to", "so you can", "if you want to"],
    "first and foremost": ["first off,", "to start,", "right off the bat,"],
    "last but not least": ["oh, and", "one more thing —", "also,"],
    "it goes without saying": ["obviously,", "look,", "I mean,"],
    "needless to say": ["obviously,", "no surprise,", "clearly,"],
    "without a doubt": ["for sure,", "definitely,", "honestly,"],
    "one of the most": ["a really", "probably the most", "a seriously"],
    "a wide range of": ["lots of", "all kinds of", "a bunch of"],
    "a variety of": ["different", "all sorts of", "various"],
    "a number of": ["some", "a few", "several"],
    "the importance of": ["why", "how much", "how crucial"],
    "the impact of": ["how", "what effect", "the way"],
    "the benefits of": ["why", "what's good about", "the upside of"],
    "the ability to": ["being able to", "how you can", "the chance to"],
    "it is also": ["it's also", "and it's", "plus it's"],
    "it is often": ["it's often", "it's usually", "a lot of times it's"],
    "it has been": ["it's been", "people have found it's been", "turns out it's been"],
    "has been shown to": ["seems to", "tends to", "actually does"],
    "has been linked to": ["seems connected to", "tends to go hand in hand with", "apparently ties into"],
    "there are various": ["there are different", "you've got a bunch of", "there's no shortage of"],
    "there are many": ["there are tons of", "you'll find lots of", "there's no shortage of"],
    "there are several": ["there are a few", "you've got some", "a handful of"],
    "there are numerous": ["there are a ton of", "lots and lots of", "so many"],
    "this is because": ["that's because", "the reason?", "why?"],
    "this can lead to": ["which can cause", "and that might mean", "so you might end up with"],
    "this allows": ["which lets", "so you can", "meaning you get to"],
    "this enables": ["which lets", "so now you can", "opening the door to"],
    "this means that": ["so basically,", "which means", "in other words,"],
    "this is especially": ["this is really", "that's especially", "it's particularly"],
    "this is particularly": ["this is especially", "that's really", "it's notably"],
    "can also be": ["is also", "works as", "doubles as"],
    "is essential for": ["really matters for", "you need for", "is a must for"],
    "is crucial for": ["is super important for", "really matters for", "you can't skip for"],
    "is important for": ["matters for", "you need for", "really helps with"],
    "when it comes to": ["with", "for", "talking about"],
    "informed decisions": ["smart choices", "better calls", "good decisions"],
    "make informed": ["make smart", "make better", "figure out the best"],
    "in addition to": ["besides", "on top of", "along with"],
    "as well as": ["and", "plus", "along with"],
    "such as": ["like", "for example,", "think"],
    "serves as a": ["works as a", "is basically a", "acts as a"],
    "stands as a": ["is really a", "works as a", "acts as a"],
    "as mentioned earlier": ["like I said,", "going back to that,", "again,"],
    "in conclusion": ["so basically,", "all in all,", "at the end of the day,"],
    "in summary": ["basically,", "long story short,", "bottom line —"],
    "in essence": ["basically,", "really,", "at its core,"],
    "in addition": ["also,", "plus,", "and"],
    "in particular": ["especially", "specifically", "mainly"],
    "in general": ["usually,", "mostly,", "for the most part,"],
    "in fact": ["actually,", "really,", "truth is,"],
    # Single-word replacements
    "additionally": ["also,", "plus,", "and"],
    "furthermore": ["also,", "and honestly,", "besides,"],
    "moreover": ["plus,", "and really,", "also,"],
    "consequently": ["so", "because of that,", "which means"],
    "nevertheless": ["still,", "but", "even so,"],
    "nonetheless": ["still,", "but", "even so,"],
    "comprehensive": ["thorough", "complete", "full"],
    "utilize": ["use", "work with", "go with"],
    "facilitate": ["help with", "make easier", "support"],
    "implement": ["set up", "build", "put together"],
    "demonstrate": ["show", "prove", "make clear"],
    "establish": ["set up", "create", "build"],
    "significant": ["big", "major", "real"],
    "fundamental": ["basic", "core", "key"],
    "leverage": ["use", "tap into", "take advantage of"],
    "robust": ["strong", "solid", "reliable"],
    "seamless": ["smooth", "easy", "clean"],
    "cutting-edge": ["latest", "modern", "newest"],
    "groundbreaking": ["new", "fresh", "game-changing"],
    "navigate": ["deal with", "handle", "figure out"],
    "navigating": ["dealing with", "handling", "figuring out"],
    "streamline": ["simplify", "speed up", "clean up"],
    "optimize": ["improve", "tweak", "fine-tune"],
    "enhance": ["improve", "boost", "make better"],
    "delve": ["dig into", "look at", "get into"],
    "delving": ["digging into", "looking at", "getting into"],
    "tapestry": ["mix", "blend", "collection"],
    "multifaceted": ["complex", "varied", "layered"],
    "nuanced": ["subtle", "detailed", "layered"],
    "pivotal": ["key", "important", "critical"],
    "paramount": ["most important", "top priority", "critical"],
    "ever-evolving": ["always changing", "shifting", "dynamic"],
    "myriad": ["many", "tons of", "loads of"],
    "plethora": ["a lot", "plenty", "loads"],
    "testament": ["proof", "sign", "evidence"],
    "embark": ["start", "jump into", "kick off"],
    "embarking": ["starting", "jumping into", "kicking off"],
    "fostering": ["building", "growing", "encouraging"],
    "foster": ["build", "grow", "encourage"],
    "harnessing": ["using", "tapping into", "grabbing"],
    "harness": ["use", "tap into", "grab"],
    "spearheading": ["leading", "driving", "pushing"],
    "spearhead": ["lead", "drive", "push"],
    "underscores": ["shows", "highlights", "points out"],
    "elevate": ["boost", "raise", "improve"],
    "elevating": ["boosting", "raising", "improving"],
    "landscape": ["space", "world", "scene"],
    "paradigm": ["model", "approach", "way of thinking"],
    "essentially": ["basically,", "really,", "at its core,"],
    "ultimately": ["in the end,", "at the end of the day,", "really,"],
    "overall": ["all in all,", "when you look at it,", "on the whole,"],
    "specifically": ["to be exact,", "in particular,", "more precisely,"],
    "particularly": ["especially", "really", "notably"],
    "increasingly": ["more and more", "these days", "lately"],
    "numerous": ["tons of", "lots of", "a bunch of"],
    "diverse": ["different", "varied", "all kinds of"],
    "various": ["different", "all sorts of", "a bunch of"],
    "crucial": ["super important", "key", "critical"],
    "ensure": ["make sure", "guarantee", "see to it that"],
    "maintain": ["keep", "hold onto", "stick with"],
    "contribute": ["add to", "help with", "play a part in"],
    "integrate": ["combine", "mix in", "blend"],
    "approach": ["way", "method", "take on"],
    "aspects": ["parts", "pieces", "sides"],
    "effectively": ["well", "in a good way", "properly"],
    "conventional": ["traditional", "usual", "standard"],
    "associated": ["linked", "connected", "tied to"],
    "regarding": ["about", "when it comes to", "on the topic of"],
    "respective": ["their own", "each", "individual"],
    "relevant": ["related", "important", "useful"],
    "potential": ["possible", "would-be", "likely"],
}

CONTRACTION_MAP = {
    "it is": "it's", "it has": "it's", "that is": "that's",
    "there is": "there's",
    "they are": "they're", "they have": "they've",
    "we are": "we're", "we have": "we've",
    "you are": "you're", "you have": "you've",
    "do not": "don't", "does not": "doesn't",
    "did not": "didn't", "is not": "isn't",
    "are not": "aren't", "was not": "wasn't",
    "were not": "weren't", "will not": "won't",
    "would not": "wouldn't", "could not": "couldn't",
    "should not": "shouldn't", "cannot": "can't",
    "can not": "can't", "have not": "haven't",
    "has not": "hasn't", "had not": "hadn't",
    "it will": "it'll", "that will": "that'll",
    "who is": "who's", "what is": "what's",
    "where is": "where's", "how is": "how's",
    "let us": "let's",
}

# Formal transitions → casual replacements
FORMAL_TRANSITIONS = [
    (r'\bHowever,\s', ["But ", "Then again, ", "That said, ", "Still, ", "On the flip side, "]),
    (r'\bTherefore,\s', ["So ", "Because of this, ", "That means ", "Which is why "]),
    (r'\bConsequently,\s', ["So ", "This means ", "Because of that, ", "End result? "]),
    (r'\bNevertheless,\s', ["Still, ", "Even so, ", "But honestly, ", "That said, "]),
    (r'\bNonetheless,\s', ["Still, ", "Even so, ", "But ", "That said, "]),
    (r'\bFurthermore,\s', ["Plus, ", "Also, ", "And ", "On top of that, "]),
    (r'\bMoreover,\s', ["Plus, ", "And really, ", "Also, ", "What's more, "]),
    (r'\bAdditionally,\s', ["Also, ", "Plus, ", "And ", "Oh, and "]),
    (r'\bIn addition,\s', ["Also, ", "Plus, ", "And ", "Another thing — "]),
    (r'\bFor instance,\s', ["Like, ", "Say, ", "Take this — ", "Example: "]),
    (r'\bFor example,\s', ["Like, ", "Say, ", "Take this: ", "Here's one — "]),
    (r'\bSpecifically,\s', ["Basically, ", "To be exact, ", "Meaning ", "So like, "]),
    (r'\bThus,\s', ["So ", "That's why ", "Which means ", "And so "]),
    (r'\bHence,\s', ["So ", "That's why ", "Which is why ", "And that's how "]),
    (r'\bAccordingly,\s', ["So ", "Because of that, ", "Which means ", "And so "]),
    (r'\bSimilarly,\s', ["Same goes for ", "Along those lines, ", "In the same way, ", "Kinda like that, "]),
    (r'\bMeanwhile,\s', ["At the same time, ", "While that's happening, ", "On another note, "]),
    (r'\bIn particular,\s', ["Especially ", "Mainly ", "Specifically, ", "One big thing — "]),
    (r'\bIn fact,\s', ["Actually, ", "Really, ", "Truth is, ", "Honestly, "]),
    (r'\bAs a result,\s', ["So ", "Because of this, ", "Which means ", "End result: "]),
    (r'\bOn the other hand,\s', ["But then, ", "Flip side? ", "Then again, ", "But "]),
    (r'\bOverall,\s', ["All in all, ", "Big picture? ", "When you look at it, ", "Bottom line, "]),
    (r'\bUltimately,\s', ["At the end of the day, ", "Really, ", "When it's all said and done, "]),
    (r'\bEssentially,\s', ["Basically, ", "Really, ", "At its core, ", "When you boil it down, "]),
]

# Sentences to inject for burstiness and human feel
SHORT_INJECTIONS = [
    "That's huge.", "Seriously.", "Makes sense, right?",
    "Think about that.", "Pretty wild.", "Not bad.",
    "Worth knowing.", "Big deal.", "True story.",
    "Simple as that.", "No joke.", "Fair enough.",
    "And that matters.", "Key point here.", "Real talk.",
    "Good stuff.", "Can't argue with that.", "It adds up.",
]

QUESTION_INJECTIONS = [
    "But why does this matter?", "So what does that mean?",
    "Sounds good, right?", "Makes you think, doesn't it?",
    "But here's the thing — what about the downsides?",
    "You might be wondering why.", "Ever thought about that?",
    "See where I'm going with this?", "Know what I mean?",
]


# ============================================================
# TRANSFORMATION FUNCTIONS
# ============================================================

def replace_ai_phrases(text):
    """Replace ALL AI phrases — obvious and subtle — with natural alternatives."""
    result = text
    sorted_phrases = sorted(PHRASE_REPLACEMENTS.items(), key=lambda x: len(x[0]), reverse=True)
    for ai_phrase, replacements in sorted_phrases:
        escaped = re.escape(ai_phrase)
        if ' ' not in ai_phrase:
            pattern = re.compile(r'\b' + escaped + r'\b', re.IGNORECASE)
        else:
            pattern = re.compile(escaped, re.IGNORECASE)
        matches = list(pattern.finditer(result))
        for match in reversed(matches):
            replacement = random.choice(replacements)
            if match.group()[0].isupper():
                replacement = replacement[0].upper() + replacement[1:]
            result = result[:match.start()] + replacement + result[match.end():]

    result = re.sub(r',\s*,', ',', result)
    result = re.sub(r'\.\s*\.', '.', result)
    return result


def add_contractions(text):
    """Aggressively convert formal phrases to contractions (90% rate)."""
    result = text
    for formal, contraction in CONTRACTION_MAP.items():
        pattern = re.compile(r'\b' + re.escape(formal) + r'\b', re.IGNORECASE)
        matches = list(pattern.finditer(result))
        for match in reversed(matches):
            if random.random() < 0.92:
                replacement = contraction
                if match.group()[0].isupper():
                    replacement = replacement[0].upper() + replacement[1:]
                result = result[:match.start()] + replacement + result[match.end():]
    return result


def reduce_formality(text):
    """Replace formal transition words with casual alternatives."""
    result = text
    for pattern, options in FORMAL_TRANSITIONS:
        matches = list(re.finditer(pattern, result))
        for match in reversed(matches):
            if random.random() < 0.85:
                replacement = random.choice(options)
                result = result[:match.start()] + replacement + result[match.end():]
    return result


def remove_hedging(text):
    """Remove or simplify hedging/qualifying language that AI overuses."""
    hedging_simplifications = [
        (r'\bIt can be\b', ["It's", "That's", "This is"]),
        (r'\bIt may be\b', ["It's probably", "It's likely", "It might be"]),
        (r'\bcan help\b', ["helps", "does help", "actually helps"]),
        (r'\bcan provide\b', ["gives you", "provides", "offers"]),
        (r'\bcan improve\b', ["improves", "boosts", "does improve"]),
        (r'\bcan enhance\b', ["improves", "boosts", "upgrades"]),
        (r'\bcan lead to\b', ["leads to", "causes", "often means"]),
        (r'\bcan result in\b', ["results in", "causes", "means"]),
        (r'\bis designed to\b', ["is built to", "is meant to", "aims to"]),
        (r'\bare designed to\b', ["are built to", "are meant to", "aim to"]),
        (r'\btends to be\b', ["is usually", "is often", "is generally"]),
        (r'\bis known for\b', ["is famous for", "is well-known for", "stands out for"]),
        (r'\bis considered\b', ["is seen as", "counts as", "is thought of as"]),
        (r'\bis often seen\b', ["shows up", "pops up", "appears"]),
        (r'\bis widely\b', ["is pretty", "is really", "is super"]),
        (r'\bis commonly\b', ["is usually", "is often", "is typically"]),
        (r'\bis generally\b', ["is usually", "is mostly", "is typically"]),
        (r'\bis typically\b', ["is usually", "is often", "is normally"]),
    ]

    result = text
    for pattern, options in hedging_simplifications:
        matches = list(re.finditer(pattern, result, re.IGNORECASE))
        for match in reversed(matches):
            if random.random() < 0.80:
                replacement = random.choice(options)
                if match.group()[0].isupper():
                    replacement = replacement[0].upper() + replacement[1:]
                result = result[:match.start()] + replacement + result[match.end():]
    return result


def break_cohesion(text):
    """Remove excessive connectives that make text flow too smoothly."""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    if len(sentences) < 3:
        return text

    result = []
    for i, sentence in enumerate(sentences):
        # Remove "This/These/Those" sentence starters sometimes
        if random.random() < 0.5:
            sentence = re.sub(
                r'^(This|These|Those) (is|are|was|were|has|have|can|could|may|might|will|would|should) ',
                lambda m: random.choice(["It's ", "That's ", "They're ", "You'll find it's ", ""]),
                sentence
            )

        # Remove "By + gerund" starters
        sentence = re.sub(
            r'^By (understanding|leveraging|using|focusing|incorporating|embracing) ',
            lambda m: random.choice(["If you ", "When you ", "Once you start ", "Just by "]),
            sentence
        )

        # Simplify "With the/this/its" starters
        sentence = re.sub(
            r'^(With the|With this|With its) ',
            lambda m: random.choice(["Thanks to ", "Given ", "Because of "]),
            sentence
        )

        result.append(sentence)

    return ' '.join(result)


def vary_sentence_lengths(text):
    """Dramatically vary sentence lengths — split long ones, combine short ones, inject fragments."""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    if len(sentences) < 3:
        return text

    result = []
    i = 0
    while i < len(sentences):
        sentence = sentences[i].strip()
        words = sentence.split()

        # Long sentence (>20 words): split aggressively
        if len(words) > 20 and random.random() < 0.6:
            split_patterns = [
                r',\s*(and|but|so|which|where|while|although|because)\s',
                r',\s*(as|since|though)\s',
                r';\s',
                r',\s*(?=\w)',
            ]
            split_done = False
            for pattern in split_patterns:
                match = re.search(pattern, sentence)
                if match and 6 < match.start() < len(sentence) - 6:
                    part1 = sentence[:match.start()].strip()
                    part2 = sentence[match.end():].strip()
                    if not part1.endswith(('.', '!', '?')):
                        part1 += '.'
                    if part2:
                        part2 = part2[0].upper() + part2[1:]
                    result.append(part1)
                    result.append(part2)
                    split_done = True
                    break
            if not split_done:
                result.append(sentence)

        # Short sentences: sometimes combine
        elif len(words) < 8 and i + 1 < len(sentences) and random.random() < 0.35:
            next_sentence = sentences[i + 1].strip()
            next_words = next_sentence.split()
            if len(next_words) < 15:
                connector = random.choice([" — ", " and ", ", plus ", " — and honestly, "])
                combined = sentence.rstrip('.!?') + connector + next_sentence[0].lower() + next_sentence[1:]
                result.append(combined)
                i += 2
                continue
            else:
                result.append(sentence)
        else:
            result.append(sentence)
        i += 1

    # Inject short fragments and questions for burstiness
    if len(result) >= 4:
        # Add 1-2 short injections
        num_injections = random.randint(1, min(3, len(result) // 3))
        for _ in range(num_injections):
            pos = random.randint(1, len(result) - 1)
            if random.random() < 0.6:
                injection = random.choice(SHORT_INJECTIONS)
            else:
                injection = random.choice(QUESTION_INJECTIONS)
            result.insert(pos, injection)

    return ' '.join(result)


def add_personal_voice(text):
    """Add first-person perspective, opinions, and personal touches."""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    if len(sentences) < 4:
        return text

    result = []
    personal_added = 0
    max_personal = max(2, len(sentences) // 4)

    for i, sentence in enumerate(sentences):
        # Add casual starters to some sentences (15% chance)
        if 1 < i < len(sentences) - 1 and random.random() < 0.15 and personal_added < max_personal:
            starters = [
                "Honestly, ", "I think ", "If you ask me, ",
                "Look, ", "The way I see it, ", "Here's the thing — ",
                "From what I've seen, ", "Real talk, ", "Gotta say, ",
            ]
            starter = random.choice(starters)
            sentence = starter + sentence[0].lower() + sentence[1:]
            personal_added += 1

        # Occasionally end with a question (8% chance)
        if random.random() < 0.08 and sentence.endswith('.') and len(sentence.split()) > 8:
            question_tags = [
                ", right?", ", you know?", ", don't you think?",
                " — wouldn't you say?", ", yeah?",
            ]
            sentence = sentence.rstrip('.') + random.choice(question_tags)

        # Very occasionally add an exclamation (5% chance)
        if random.random() < 0.05 and sentence.endswith('.'):
            sentence = sentence.rstrip('.') + '!'

        result.append(sentence)

    return ' '.join(result)


def add_creative_punctuation(text):
    """Replace boring period-only punctuation with varied human punctuation."""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    result = []

    for i, sentence in enumerate(sentences):
        # Add em-dashes within sentences (replace some commas)
        if random.random() < 0.15 and ',' in sentence:
            commas = [(m.start(), m.end()) for m in re.finditer(r',\s', sentence)]
            if commas:
                idx = random.choice(range(len(commas)))
                start, end = commas[idx]
                sentence = sentence[:start] + ' — ' + sentence[end:]

        # Add parenthetical asides
        if random.random() < 0.06 and len(sentence.split()) > 12:
            asides = [
                " (seriously)", " (no kidding)", " (which is pretty cool)",
                " (and that's a good thing)", " (trust me on this)",
                " (worth remembering)", " (at least in my experience)",
            ]
            # Insert before the last few words
            words = sentence.split()
            insert_point = max(3, len(words) - random.randint(2, 4))
            words.insert(insert_point, random.choice(asides))
            sentence = ' '.join(words)

        result.append(sentence)

    return ' '.join(result)


def vary_paragraph_structure(text):
    """Restructure paragraphs for varied complexity."""
    paragraphs = text.split('\n\n')
    if len(paragraphs) <= 1:
        paragraphs = text.split('\n')

    if len(paragraphs) <= 1:
        return text

    result = []
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        sentences = re.split(r'(?<=[.!?])\s+', para)

        # Split long paragraphs
        if len(sentences) > 5 and random.random() < 0.5:
            split = len(sentences) // 2 + random.randint(-1, 1)
            split = max(2, min(split, len(sentences) - 2))
            result.append(' '.join(sentences[:split]))
            result.append(' '.join(sentences[split:]))
        # Merge very short adjacent paragraphs
        elif len(sentences) <= 2 and result and len(re.split(r'(?<=[.!?])\s+', result[-1])) <= 3:
            result[-1] = result[-1] + ' ' + para
        else:
            result.append(para)

    return '\n\n'.join(result)


def final_cleanup(text):
    """Clean up artifacts from all transformations."""
    # Fix double punctuation
    text = re.sub(r',\s*,', ',', text)
    text = re.sub(r'\.\s*\.', '.', text)
    text = re.sub(r'!\s*!', '!', text)
    text = re.sub(r'\?\s*\?', '?', text)
    # Fix double spaces
    text = re.sub(r'  +', ' ', text)
    # Fix space before punctuation
    text = re.sub(r'\s+([.,!?;:])', r'\1', text)
    # Fix capitalization after sentence ends
    text = re.sub(r'([.!?])\s+([a-z])', lambda m: m.group(1) + ' ' + m.group(2).upper(), text)
    # Remove empty parentheses
    text = re.sub(r'\(\s*\)', '', text)
    return text.strip()


# ============================================================
# MAIN FUNCTION
# ============================================================

def humanize_text(text, intensity='medium'):
    """
    Main humanization function. Applies transformations based on intensity.

    light: phrase replacement + contractions + formality reduction
    medium: + sentence variation + cohesion breaking + hedging removal + personal voice
    heavy: + paragraph restructuring + creative punctuation + maximum injections
    """
    if not text or len(text.strip()) < 20:
        return {
            'humanized_text': text,
            'changes_made': [],
            'message': 'Text too short to humanize effectively.',
        }

    original = text
    changes = []

    # === ALL INTENSITIES ===

    # Step 1: Replace AI phrases (both obvious and subtle)
    text = replace_ai_phrases(text)
    if text != original:
        changes.append('Replaced AI phrases with natural alternatives')

    # Step 2: Aggressive contractions
    before = text
    text = add_contractions(text)
    if text != before:
        changes.append('Added contractions throughout')

    # Step 3: Replace formal transitions
    before = text
    text = reduce_formality(text)
    if text != before:
        changes.append('Replaced formal transitions with casual ones')

    # Step 4: Remove hedging language
    before = text
    text = remove_hedging(text)
    if text != before:
        changes.append('Simplified hedging and qualifying language')

    # === MEDIUM + HEAVY ===
    if intensity in ('medium', 'heavy'):

        # Step 5: Break cohesion patterns
        before = text
        text = break_cohesion(text)
        if text != before:
            changes.append('Broke up predictable cohesion patterns')

        # Step 6: Vary sentence lengths dramatically
        before = text
        text = vary_sentence_lengths(text)
        if text != before:
            changes.append('Varied sentence lengths and added fragments')

        # Step 7: Add personal voice
        before = text
        text = add_personal_voice(text)
        if text != before:
            changes.append('Added personal voice and opinions')

    # === HEAVY ONLY ===
    if intensity == 'heavy':

        # Step 8: Creative punctuation
        before = text
        text = add_creative_punctuation(text)
        if text != before:
            changes.append('Added varied punctuation (dashes, parentheticals)')

        # Step 9: Paragraph restructuring
        before = text
        text = vary_paragraph_structure(text)
        if text != before:
            changes.append('Restructured paragraphs for variation')

    # Final cleanup
    text = final_cleanup(text)

    return {
        'humanized_text': text,
        'original_length': len(original),
        'humanized_length': len(text),
        'changes_made': changes,
        'intensity': intensity,
        'message': f'Text humanized with {len(changes)} types of modifications applied.',
    }
