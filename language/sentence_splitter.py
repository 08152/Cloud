
import re


class SentenceSplitter:

    def __init__(self):
        self.abbreviations = {
            "z.b.",
            "bzw.",
            "usw.",
            "etc.",
            "u.a.",
            "d.h.",
            "vgl.",
            "ca.",
            "evtl.",
            "inkl.",
            "exkl.",
            "prof.",
            "dr.",
            "b.a.",
            "mio.",
            "mrd.",
            "nr.",
            "str."
        }

        self.terminal_marks = {".", "!", "?"}

    def split(self, text):
        if not isinstance(text, str):
            return []

        text = text.strip()

        if not text:
            return []

        sentences = []
        current = []

        for index, char in enumerate(text):

            current.append(char)

            if char not in self.terminal_marks:
                continue

            if self._is_decimal_point(text, index):
                continue

            if self._is_abbreviation(text, index):
                continue

            if not self._is_sentence_end(text, index):
                continue

            sentence = "".join(current).strip()

            if sentence:
                sentences.append(sentence)

            current = []

        remaining = "".join(current).strip()

        if remaining:
            sentences.append(remaining)

        return sentences

    def _is_decimal_point(self, text, index):
        if text[index] != ".":
            return False

        if index == 0 or index >= len(text) - 1:
            return False

        return (
            text[index - 1].isdigit()
            and text[index + 1].isdigit()
        )

    def _is_abbreviation(self, text, index):
        if text[index] != ".":
            return False

        start = index

        while start > 0 and (
            text[start - 1].isalpha()
            or text[start - 1] == "."
        ):
            start -= 1

        word = text[start:index + 1].lower()

        return word in self.abbreviations

    def _is_sentence_end(self, text, index):
        if index == len(text) - 1:
            return True

        next_char = text[index + 1]

        if next_char.isspace():
            return True

        if next_char in '"\'»)]}':
            return True

        return False

    def split_lines(self, text):
        if not isinstance(text, str):
            return []

        results = []

        for line in text.splitlines():
            line = line.strip()

            if line:
                results.extend(self.split(line))

        return results

    def count_sentences(self, text):
        return len(self.split(text))

    def get_sentence(self, text, index):
        sentences = self.split(text)

        if not isinstance(index, int):
            return None

        if index < 0 or index >= len(sentences):
            return None

        return sentences[index]

    def get_statistics(self, text):
        sentences = self.split(text)

        return {
            "sentence_count": len(sentences),
            "average_length": (
                sum(len(s) for s in sentences) / len(sentences)
                if sentences else 0
            ),
            "longest_sentence": max(
                sentences,
                key=len,
                default=""
            ),
            "shortest_sentence": min(
                sentences,
                key=len,
                default=""
            )
        }
