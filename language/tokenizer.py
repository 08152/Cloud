
"""
====================================================
CLOUDE AI - TOKENIZER
Version: 0.1.0
====================================================

Eigene Tokenisierung für die Sprachverarbeitung.

Aufgaben:
- Texte zerlegen
- Wörter erkennen
- Satzzeichen erkennen
- Zahlen erkennen
- Satzgrenzen erkennen
- Tokenpositionen speichern
- Wortarten vorbereiten

Nur Python-Standardbibliothek.
"""

import re
from dataclasses import dataclass
from typing import List


# ==================================================
# 1. TOKEN TYPES
# ==================================================

TOKEN_WORD = "WORD"
TOKEN_NUMBER = "NUMBER"
TOKEN_PUNCTUATION = "PUNCTUATION"
TOKEN_WHITESPACE = "WHITESPACE"
TOKEN_SYMBOL = "SYMBOL"


# ==================================================
# 2. TOKEN DATA STRUCTURE
# ==================================================

@dataclass
class Token:

    value: str

    token_type: str

    position: int

    start: int

    end: int

    sentence_id: int = 0


# ==================================================
# 3. TOKENIZER
# ==================================================

class Tokenizer:

    def __init__(self):

        self.pattern = re.compile(
            r"\s+"
            r"|[A-Za-zÄÖÜäöüß]+(?:['’][A-Za-zÄÖÜäöüß]+)*"
            r"|\d+(?:[.,]\d+)*"
            r"|[^\w\s]",
            re.UNICODE
        )

        self.abbreviations = {
            "z.B.",
            "bzw.",
            "usw.",
            "etc.",
            "Dr.",
            "Prof.",
            "Mr.",
            "Mrs."
        }

    # ==============================================
    # 4. DETECT TOKEN TYPE
    # ==============================================

    def detect_type(self, value):

        if value.isspace():
            return TOKEN_WHITESPACE

        if value.isdigit() or re.fullmatch(
            r"\d+(?:[.,]\d+)*",
            value
        ):
            return TOKEN_NUMBER

        if re.fullmatch(
            r"[A-Za-zÄÖÜäöüß]+(?:['’][A-Za-zÄÖÜäöüß]+)*",
            value
        ):
            return TOKEN_WORD

        if re.fullmatch(r"[^\w\s]", value):
            return TOKEN_PUNCTUATION

        return TOKEN_SYMBOL

    # ==============================================
    # 5. TOKENIZE TEXT
    # ==============================================

    def tokenize(self, text):

        if not isinstance(text, str):
            raise TypeError("Input must be a string.")

        matches = list(self.pattern.finditer(text))

        tokens = []

        sentence_id = 0

        for position, match in enumerate(matches):

            value = match.group()

            token_type = self.detect_type(value)

            token = Token(
                value=value,
                token_type=token_type,
                position=position,
                start=match.start(),
                end=match.end(),
                sentence_id=sentence_id
            )

            tokens.append(token)

            if value in [".", "!", "?"]:
                sentence_id += 1

        return tokens

    # ==============================================
    # 6. REMOVE WHITESPACE
    # ==============================================

    def remove_whitespace(self, tokens):

        return [
            token
            for token in tokens
            if token.token_type != TOKEN_WHITESPACE
        ]

    # ==============================================
    # 7. EXTRACT WORDS
    # ==============================================

    def extract_words(self, tokens):

        return [
            token.value
            for token in tokens
            if token.token_type == TOKEN_WORD
        ]

    # ==============================================
    # 8. EXTRACT NUMBERS
    # ==============================================

    def extract_numbers(self, tokens):

        return [
            token.value
            for token in tokens
            if token.token_type == TOKEN_NUMBER
        ]

    # ==============================================
    # 9. EXTRACT SENTENCES
    # ==============================================

    def extract_sentences(self, tokens):

        sentences = []

        current_sentence = []

        for token in tokens:

            if token.token_type == TOKEN_WHITESPACE:
                continue

            current_sentence.append(token.value)

            if token.value in [".", "!", "?"]:

                sentences.append(
                    " ".join(current_sentence)
                )

                current_sentence = []

        if current_sentence:

            sentences.append(
                " ".join(current_sentence)
            )

        return sentences

    # ==============================================
    # 10. TOKEN STATISTICS
    # ==============================================

    def analyze(self, tokens):

        statistics = {

            "total_tokens": len(tokens),

            "words": 0,

            "numbers": 0,

            "punctuation": 0,

            "symbols": 0,

            "whitespace": 0

        }

        for token in tokens:

            if token.token_type == TOKEN_WORD:
                statistics["words"] += 1

            elif token.token_type == TOKEN_NUMBER:
                statistics["numbers"] += 1

            elif token.token_type == TOKEN_PUNCTUATION:
                statistics["punctuation"] += 1

            elif token.token_type == TOKEN_SYMBOL:
                statistics["symbols"] += 1

            elif token.token_type == TOKEN_WHITESPACE:
                statistics["whitespace"] += 1

        return statistics
