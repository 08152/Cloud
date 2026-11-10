
"""
====================================================
CLOUDE AI - GRAMMAR ENGINE
Version: 0.1.0
====================================================

Eigene Grammatik- und Satzanalyse.

Funktionen:
- Satztypen erkennen
- Subjekte erkennen
- Prädikate erkennen
- Objekte erkennen
- Verneinungen erkennen
- Zeitformen vorbereiten
- Wortpositionen analysieren
- Satzstrukturen speichern

Nur Python-Standardbibliothek.
"""

import re

from dataclasses import dataclass, field
from typing import List, Optional


# ==================================================
# 1. GRAMMATICAL CONSTANTS
# ==================================================

SENTENCE_STATEMENT = "statement"
SENTENCE_QUESTION = "question"
SENTENCE_COMMAND = "command"
SENTENCE_EXCLAMATION = "exclamation"
SENTENCE_UNKNOWN = "unknown"


# ==================================================
# 2. GRAMMATICAL DATA STRUCTURE
# ==================================================

@dataclass
class WordAnalysis:

    word: str

    position: int

    word_type: str = "unknown"

    grammatical_role: str = "unknown"

    features: dict = field(default_factory=dict)


@dataclass
class SentenceAnalysis:

    original: str

    sentence_type: str

    words: List[WordAnalysis]

    subject: Optional[str] = None

    predicate: Optional[str] = None

    object: Optional[str] = None

    negated: bool = False

    tense: str = "unknown"

    confidence: float = 0.0


# ==================================================
# 3. GRAMMAR ENGINE
# ==================================================

class GrammarEngine:

    def __init__(self):

        self.articles = {

            "der", "die", "das",
            "ein", "eine", "einen",
            "einem", "einer",
            "den", "dem", "des"

        }

        self.pronouns = {

            "ich", "du", "er", "sie",
            "es", "wir", "ihr",
            "mich", "dich", "ihn",
            "uns", "euch", "mir",
            "dir", "ihm", "ihnen"

        }

        self.negations = {

            "nicht", "kein", "keine",
            "keinen", "keinem",
            "keiner", "keines",
            "nie", "niemals"

        }

        self.question_words = {

            "wer", "was", "wann",
            "wo", "warum", "wie",
            "welche", "welcher",
            "wessen", "wem", "wen"

        }

        self.common_verbs = {

            "sein", "haben", "werden",
            "gehen", "kommen", "machen",
            "wissen", "denken", "sagen",
            "sprechen", "lernen",
            "arbeiten", "spielen",
            "schreiben", "lesen",
            "sehen", "hören",
            "mögen", "lieben",
            "brauchen", "können",
            "müssen", "wollen",
            "sollen", "dürfen"

        }

        self.past_indicators = {

            "gestern", "früher",
            "damals", "vorhin"

        }

        self.future_indicators = {

            "morgen", "später",
            "bald", "zukünftig"

        }

    # ==============================================
    # 4. NORMALIZE
    # ==============================================

    def normalize(self, text):

        if not isinstance(text, str):

            raise TypeError(
                "Sentence must be a string."
            )

        return text.strip()

    # ==============================================
    # 5. SPLIT WORDS
    # ==============================================

    def tokenize(self, text):

        return re.findall(
            r"[A-Za-zÄÖÜäöüß]+(?:['’][A-Za-zÄÖÜäöüß]+)*|[^\w\s]",
            text,
            re.UNICODE
        )

    # ==============================================
    # 6. DETECT SENTENCE TYPE
    # ==============================================

    def detect_sentence_type(self, text, words):

        if not words:

            return SENTENCE_UNKNOWN

        if text.endswith("?"):

            return SENTENCE_QUESTION

        if text.endswith("!"):

            return SENTENCE_EXCLAMATION

        if words[0].lower() in self.question_words:

            return SENTENCE_QUESTION

        if words[0].lower() in {

            "bitte", "mach", "geh",
            "komm", "schreib", "lies"

        }:

            return SENTENCE_COMMAND

        return SENTENCE_STATEMENT

    # ==============================================
    # 7. DETECT NEGATION
    # ==============================================

    def detect_negation(self, words):

        return any(

            word.lower() in self.negations

            for word in words

        )

    # ==============================================
    # 8. DETECT TENSE
    # ==============================================

    def detect_tense(self, words):

        normalized = [

            word.lower()

            for word in words

        ]

        if any(

            word in self.future_indicators

            for word in normalized

        ):

            return "future"

        if any(

            word in self.past_indicators

            for word in normalized

        ):

            return "past"

        return "present_or_unknown"

    # ==============================================
    # 9. IDENTIFY VERBS
    # ==============================================

    def identify_verbs(self, words):

        verbs = []

        for index, word in enumerate(words):

            normalized = word.lower()

            if normalized in self.common_verbs:

                verbs.append((index, word))

                continue

            if normalized.endswith(

                ("e", "st", "t", "en")

            ):

                if normalized in {

                    "bin", "bist", "ist",
                    "sind", "seid",
                    "habe", "hast",
                    "hat", "haben",
                    "habt", "hatte",
                    "hatten", "war",
                    "waren", "wird",
                    "werden", "wurde",
                    "wollen", "will",
                    "kann", "können",
                    "muss", "müssen"

                }:

                    verbs.append((index, word))

        return verbs

    # ==============================================
    # 10. IDENTIFY SUBJECT
    # ==============================================

    def identify_subject(self, words, verb_positions):

        if not words:

            return None

        if not verb_positions:

            return None

        first_verb_position = verb_positions[0][0]

        candidates = words[:first_verb_position]

        if not candidates:

            return None

        for word in reversed(candidates):

            if word.lower() in self.pronouns:

                return word

        for word in reversed(candidates):

            if word.lower() not in self.articles:

                return word

        return None

    # ==============================================
    # 11. IDENTIFY PREDICATE
    # ==============================================

    def identify_predicate(self, verb_positions):

        if not verb_positions:

            return None

        return verb_positions[0][1]

    # ==============================================
    # 12. IDENTIFY OBJECT
    # ==============================================

    def identify_object(
        self,
        words,
        verb_positions
    ):

        if not verb_positions:

            return None

        verb_position = verb_positions[0][0]

        candidates = words[verb_position + 1:]

        if not candidates:

            return None

        for word in candidates:

            if word.lower() not in self.articles:

                if word.lower() not in self.negations:

                    return word

        return None

    # ==============================================
    # 13. WORD CLASSIFICATION
    # ==============================================

    def classify_word(self, word):

        normalized = word.lower()

        if normalized in self.articles:

            return "article"

        if normalized in self.pronouns:

            return "pronoun"

        if normalized in self.negations:

            return "negation"

        if normalized in self.question_words:

            return "question_word"

        if normalized in self.common_verbs:

            return "verb"

        if normalized.isdigit():

            return "number"

        if re.fullmatch(r"[^\w\s]", word):

            return "punctuation"

        return "unknown"

    # ==============================================
    # 14. COMPLETE SENTENCE ANALYSIS
    # ==============================================

    def analyze(self, text):

        text = self.normalize(text)

        words = self.tokenize(text)

        normalized_words = [

            word.lower()

            for word in words

        ]

        sentence_type = self.detect_sentence_type(
            text,
            words
        )

        verb_positions = self.identify_verbs(
            words
        )

        subject = self.identify_subject(
            words,
            verb_positions
        )

        predicate = self.identify_predicate(
            verb_positions
        )

        object_value = self.identify_object(
            words,
            verb_positions
        )

        negated = self.detect_negation(
            words
        )

        tense = self.detect_tense(
            words
        )

        word_analyses = []

        for index, word in enumerate(words):

            word_analyses.append(

                WordAnalysis(

                    word=word,

                    position=index,

                    word_type=self.classify_word(
                        word
                    )

                )

            )

        confidence = 0.0

        if words:

            confidence += 0.2

        if predicate:

            confidence += 0.3

        if subject:

            confidence += 0.3

        if sentence_type != SENTENCE_UNKNOWN:

            confidence += 0.2

        return SentenceAnalysis(

            original=text,

            sentence_type=sentence_type,

            words=word_analyses,

            subject=subject,

            predicate=predicate,

            object=object_value,

            negated=negated,

            tense=tense,

            confidence=confidence

        )

    # ==============================================
    # 15. ANALYZE MULTIPLE SENTENCES
    # ==============================================

    def analyze_text(self, text):

        sentences = re.split(

            r"(?<=[.!?])\s+",

            text.strip()

        )

        return [

            self.analyze(sentence)

            for sentence in sentences

            if sentence.strip()

        ]

    # ==============================================
    # 16. EXPORT ANALYSIS
    # ==============================================

    def to_dict(self, analysis):

        return {

            "original": analysis.original,

            "sentence_type": analysis.sentence_type,

            "subject": analysis.subject,

            "predicate": analysis.predicate,

            "object": analysis.object,

            "negated": analysis.negated,

            "tense": analysis.tense,

            "confidence": analysis.confidence,

            "words": [

                {

                    "word": word.word,

                    "position": word.position,

                    "type": word.word_type,

                    "role": word.grammatical_role

                }

                for word in analysis.words

            ]

        }
