
import re
import unicodedata


class TextNormalizer:

    def __init__(self):
        self.replacements = {
            "ß": "ß",
            "’": "'",
            "‘": "'",
            "“": '"',
            "”": '"',
            "–": "-",
            "—": "-",
            "\u00a0": " "
        }

    def normalize(self, text):
        if not isinstance(text, str):
            return ""

        text = unicodedata.normalize("NFC", text)

        text = self._replace_characters(text)
        text = self._remove_control_characters(text)
        text = self._normalize_whitespace(text)
        text = self._normalize_punctuation(text)

        return text.strip()

    def _replace_characters(self, text):
        for old, new in self.replacements.items():
            text = text.replace(old, new)

        return text

    def _remove_control_characters(self, text):
        return "".join(
            char for char in text
            if char in "\n\t" or not unicodedata.category(char).startswith("C")
        )

    def _normalize_whitespace(self, text):
        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text

    def _normalize_punctuation(self, text):
        text = re.sub(r"([!?.,])\1{2,}", r"\1\1", text)
        text = re.sub(r"\s+([,.;:!?])", r"\1", text)

        return text

    def normalize_for_search(self, text):
        text = self.normalize(text)
        text = text.casefold()

        return text

    def normalize_word(self, word):
        if not isinstance(word, str):
            return ""

        word = self.normalize(word)
        word = word.casefold()

        return word.strip()

    def normalize_words(self, words):
        if not isinstance(words, (list, tuple)):
            return []

        return [
            self.normalize_word(word)
            for word in words
            if isinstance(word, str) and word.strip()
        ]

    def remove_accents(self, text):
        if not isinstance(text, str):
            return ""

        normalized = unicodedata.normalize("NFD", text)

        return "".join(
            char for char in normalized
            if unicodedata.category(char) != "Mn"
        )

    def clean_for_comparison(self, text):
        text = self.normalize_for_search(text)
        text = self.remove_accents(text)

        return text

    def is_empty(self, text):
        return not self.normalize(text)

    def get_statistics(self, text):
        normalized = self.normalize(text)

        return {
            "characters": len(normalized),
            "words": len(normalized.split()),
            "sentences": len(
                re.findall(r"[.!?]+", normalized)
            ),
            "lines": len(normalized.splitlines())
        }
