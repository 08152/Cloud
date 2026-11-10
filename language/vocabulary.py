
"""
====================================================
CLOUDE AI - VOCABULARY ENGINE
Version: 0.1.0
====================================================

Eigenständiges Vokabularsystem.

Verantwortlichkeiten:
- Wörter speichern
- Wörter identifizieren
- Wortarten verwalten
- Wortfrequenzen erfassen
- Bedeutungen speichern
- Synonyme verwalten
- Wortbeziehungen verwalten
- Unbekannte Wörter erkennen
- Vokabular exportieren und importieren

Nur Python-Standardbibliothek.
"""

import json
import re

from pathlib import Path
from collections import Counter


class VocabularyEngine:

    def __init__(self):

        self.words = {}

        self.word_frequencies = Counter()

        self.synonyms = {}

        self.relationships = {}

        self.unknown_words = set()

        self.total_words_processed = 0

    # ==============================================
    # 1. WORD NORMALIZATION
    # ==============================================

    def normalize(self, word):

        if not isinstance(word, str):
            return ""

        word = word.strip().lower()

        word = re.sub(r"\s+", " ", word)

        return word

    # ==============================================
    # 2. REGISTER WORD
    # ==============================================

    def register_word(
        self,
        word,
        word_type="unknown",
        meaning=None
    ):

        word = self.normalize(word)

        if not word:
            return False

        if word not in self.words:

            self.words[word] = {

                "word": word,

                "type": word_type,

                "meanings": [],

                "attributes": {},

                "frequency": 0,

                "known": True

            }

        if meaning:

            if meaning not in self.words[word]["meanings"]:

                self.words[word]["meanings"].append(
                    meaning
                )

        if word_type != "unknown":

            self.words[word]["type"] = word_type

        return True

    # ==============================================
    # 3. CHECK WORD
    # ==============================================

    def contains(self, word):

        word = self.normalize(word)

        return word in self.words

    # ==============================================
    # 4. GET WORD INFORMATION
    # ==============================================

    def get_word(self, word):

        word = self.normalize(word)

        return self.words.get(word)

    # ==============================================
    # 5. PROCESS WORD
    # ==============================================

    def process_word(self, word):

        word = self.normalize(word)

        if not word:
            return None

        self.total_words_processed += 1

        self.word_frequencies[word] += 1

        if word in self.words:

            self.words[word]["frequency"] += 1

        else:

            self.unknown_words.add(word)

        return self.get_word(word)

    # ==============================================
    # 6. PROCESS TEXT
    # ==============================================

    def process_text(self, text):

        if not isinstance(text, str):
            raise TypeError("Text must be a string.")

        words = re.findall(
            r"[A-Za-zÄÖÜäöüß]+",
            text.lower()
        )

        results = []

        for word in words:

            results.append(
                self.process_word(word)
            )

        return results

    # ==============================================
    # 7. ADD WORD MEANING
    # ==============================================

    def add_meaning(self, word, meaning):

        word = self.normalize(word)

        if not meaning:
            return False

        if not self.contains(word):

            self.register_word(word)

        meanings = self.words[word]["meanings"]

        if meaning not in meanings:

            meanings.append(meaning)

        return True

    # ==============================================
    # 8. ADD WORD ATTRIBUTES
    # ==============================================

    def add_attribute(self, word, name, value):

        word = self.normalize(word)

        if not self.contains(word):

            self.register_word(word)

        self.words[word]["attributes"][name] = value

        return True

    # ==============================================
    # 9. ADD SYNONYM
    # ==============================================

    def add_synonym(self, word, synonym):

        word = self.normalize(word)

        synonym = self.normalize(synonym)

        if not word or not synonym:
            return False

        self.synonyms.setdefault(
            word,
            set()
        ).add(synonym)

        self.synonyms.setdefault(
            synonym,
            set()
        ).add(word)

        return True

    # ==============================================
    # 10. GET SYNONYMS
    # ==============================================

    def get_synonyms(self, word):

        word = self.normalize(word)

        return sorted(
            self.synonyms.get(word, set())
        )

    # ==============================================
    # 11. WORD RELATIONSHIPS
    # ==============================================

    def add_relationship(
        self,
        word,
        related_word,
        relationship_type
    ):

        word = self.normalize(word)

        related_word = self.normalize(related_word)

        if not word or not related_word:
            return False

        self.relationships.setdefault(
            word,
            []
        ).append({

            "target": related_word,

            "type": relationship_type

        })

        return True

    # ==============================================
    # 12. GET RELATIONSHIPS
    # ==============================================

    def get_relationships(self, word):

        word = self.normalize(word)

        return self.relationships.get(
            word,
            []
        )

    # ==============================================
    # 13. GET UNKNOWN WORDS
    # ==============================================

    def get_unknown_words(self):

        return sorted(self.unknown_words)

    # ==============================================
    # 14. LEARN WORD
    # ==============================================

    def learn_word(
        self,
        word,
        word_type="unknown",
        meaning=None
    ):

        word = self.normalize(word)

        if not word:
            return False

        result = self.register_word(
            word,
            word_type,
            meaning
        )

        self.unknown_words.discard(word)

        return result

    # ==============================================
    # 15. SEARCH VOCABULARY
    # ==============================================

    def search(self, query):

        query = self.normalize(query)

        results = []

        for word, information in self.words.items():

            if query in word:

                results.append(information)

        return results

    # ==============================================
    # 16. MOST FREQUENT WORDS
    # ==============================================

    def get_most_frequent(self, limit=20):

        return self.word_frequencies.most_common(
            max(0, limit)
        )

    # ==============================================
    # 17. STATISTICS
    # ==============================================

    def get_statistics(self):

        return {

            "vocabulary_size": len(self.words),

            "processed_words": self.total_words_processed,

            "unknown_words": len(self.unknown_words),

            "synonym_groups": len(self.synonyms),

            "relationships": sum(
                len(items)
                for items in self.relationships.values()
            )

        }

    # ==============================================
    # 18. EXPORT VOCABULARY
    # ==============================================

    def export_data(self, path):

        path = Path(path)

        data = {

            "words": self.words,

            "frequencies": dict(
                self.word_frequencies
            ),

            "synonyms": {

                word: sorted(values)

                for word, values in self.synonyms.items()

            },

            "relationships": self.relationships,

            "unknown_words": sorted(
                self.unknown_words
            ),

            "total_words_processed": self.total_words_processed

        }

        path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with path.open(
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4
            )

    # ==============================================
    # 19. IMPORT VOCABULARY
    # ==============================================

    def import_data(self, path):

        path = Path(path)

        if not path.exists():
            return False

        with path.open(
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if not isinstance(data, dict):
            raise ValueError("Invalid vocabulary data.")

        self.words = data.get("words", {})

        self.word_frequencies = Counter(
            data.get("frequencies", {})
        )

        self.synonyms = {

            word: set(values)

            for word, values in data.get(
                "synonyms", {}
            ).items()

        }

        self.relationships = data.get(
            "relationships", {}
        )

        self.unknown_words = set(
            data.get("unknown_words", [])
        )

        self.total_words_processed = data.get(
            "total_words_processed",
            0
        )

        return True
